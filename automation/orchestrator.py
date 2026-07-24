"""
automation/orchestrator.py
"""

from time import sleep


class Orchestrator:

    def __init__(
        self,
        project,
        watcher,
        scheduler,
        monitor,
        poll_interval=30,
    ):

        self.project = project
        self.watcher = watcher
        self.scheduler = scheduler
        self.monitor = monitor

        self.poll_interval = poll_interval

    def step(self):

        #
        # Discover new commits.
        #

        jobs = self.watcher.discover(self.project)

        #
        # Queue them.
        #

        for job in jobs:
            self.scheduler.enqueue(job)

        #
        # Update currently running job.
        #

        self.monitor.poll(self.project)

        #
        # Launch the next job only if idle.
        #

        self.scheduler.tick(self.project)

    def run(self):

        while True:

            self.step()

            sleep(self.poll_interval)