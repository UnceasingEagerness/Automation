from collections import deque
from datetime import datetime

from automation.runner.runner import Runner
from automation.state.state_manager import StateManager
from automation.state.status import Status


class Scheduler:

    def __init__(
        self,
        runner: Runner,
        state_manager=None,
    ):

        self.runner = runner

        self.queue = deque()

        self.state_manager = (
            state_manager
            if state_manager
            else StateManager()
        )

    def enqueue(self, job):

        state = self.state_manager.load(job.project.name)

        #
        # Don't overwrite RUNNING status.
        #

        if state.status != Status.RUNNING:
            state.status = Status.QUEUED

        self.state_manager.save(state)

        self.queue.append(job)

    def has_pending(self):

        return len(self.queue) > 0

    def is_idle(self, project_name):

        state = self.state_manager.load(project_name)

        return state.status != Status.RUNNING

    def dispatch(self):

        if not self.queue:
            return None

        job = self.queue.popleft()

        state = self.state_manager.load(job.project.name)

        state.status = Status.RUNNING
        state.running_commit = job.commit
        state.last_started = datetime.now()

        self.state_manager.save(state)

        handle = self.runner.start(job)

        state.backend = handle.backend
        state.run_id = handle.run_id

        self.state_manager.save(state)

        return handle

    def tick(self, project):

        """
        Dispatch ONE job only if the project
        is currently idle.
        """

        if not self.has_pending():
            return None

        if not self.is_idle(project.name):
            return None

        return self.dispatch()

    def complete(self, project_name):

        state = self.state_manager.load(project_name)

        state.status = Status.COMPLETED
        state.last_finished = datetime.now()

        self.state_manager.save(state)

    def fail(self, project_name):

        state = self.state_manager.load(project_name)

        state.status = Status.FAILED
        state.last_finished = datetime.now()

        self.state_manager.save(state)