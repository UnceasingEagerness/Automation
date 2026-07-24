from datetime import datetime

from automation.history import HistoryManager
from automation.slurm.job_status import JobStatus
import automation.slurm.slurm_utils as slurm

from automation.state.status import Status


class Monitor:
    """
    Polls running jobs and updates project state.
    Automatically archives completed runs.
    """

    def __init__(self, state_manager):

        self.state_manager = state_manager
        self.history = HistoryManager()

    def _archive_run(self, project, state):

        self.history.record(
            project=project.name,
            commit=state.running_commit,
            branch=getattr(project, "branch", None),
            backend=state.backend,
            run_id=state.run_id,
            status=state.status.name,
            started=state.last_started,
            finished=state.last_finished,
        )

    def _clear_running_state(self, state):

        state.running_commit = None
        state.backend = None
        state.run_id = None

    def poll(self, project):

        state = self.state_manager.load(project.name)

        #
        # Nothing running.
        #

        if state.status != Status.RUNNING:
            return state.status

        if state.run_id is None:
            return state.status

        job_status = slurm.status(state.run_id)

        #
        # Job still executing.
        #

        if job_status in (
            JobStatus.RUNNING,
            JobStatus.PENDING,
        ):
            state.touch()
            self.state_manager.save(state)
            return state.status

        #
        # Terminal state reached.
        #

        state.last_finished = datetime.now()

        if job_status == JobStatus.COMPLETED:
            state.status = Status.COMPLETED

        elif job_status in (
            JobStatus.FAILED,
            JobStatus.CANCELLED,
            JobStatus.TIMEOUT,
        ):
            state.status = Status.FAILED

        else:
            #
            # Unknown state: don't archive yet.
            #

            state.touch()
            self.state_manager.save(state)
            return state.status

        #
        # Archive the finished experiment.
        #

        self._archive_run(project, state)

        #
        # Clear runtime fields.
        #

        self._clear_running_state(state)

        self.state_manager.save(state)

        return state.status