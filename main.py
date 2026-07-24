from automation.core.project_loader import ProjectLoader
from automation.monitor.monitor import Monitor
from automation.orchestrator import Orchestrator
from automation.runner.slurm_runner import SlurmRunner
from automation.scheduler.scheduler import Scheduler
from automation.state.state_manager import StateManager
from automation.watcher.watcher import Watcher


def main():

    projects = ProjectLoader.load_all()

    watcher = Watcher()

    runner = SlurmRunner()

    state_manager = StateManager()

    scheduler = Scheduler(
        runner=runner,
        state_manager=state_manager,
    )

    monitor = Monitor(state_manager)

    #
    # Run one orchestrator per project.
    #

    orchestrators = []

    for project in projects:

        orchestrators.append(
            Orchestrator(
                project=project,
                watcher=watcher,
                scheduler=scheduler,
                monitor=monitor,
            )
        )

    while True:

        for orchestrator in orchestrators:

            orchestrator.step()


if __name__ == "__main__":

    main()