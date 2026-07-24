from unittest.mock import MagicMock

from automation.orchestrator import Orchestrator


class DummyProject:
    name = "TEST"


def test_step():

    #
    # Create mocked subsystems.
    #

    watcher = MagicMock()
    scheduler = MagicMock()
    monitor = MagicMock()

    #
    # Simulate watcher discovering two jobs.
    #

    watcher.discover.return_value = [
        "job1",
        "job2",
    ]

    #
    # IMPORTANT:
    # Use ONE project instance.
    #

    project = DummyProject()

    orchestrator = Orchestrator(
        project=project,
        watcher=watcher,
        scheduler=scheduler,
        monitor=monitor,
        poll_interval=1,
    )

    orchestrator.step()

    #
    # Watcher called.
    #

    watcher.discover.assert_called_once_with(project)

    #
    # Both jobs enqueued.
    #

    assert scheduler.enqueue.call_count == 2

    scheduler.enqueue.assert_any_call("job1")
    scheduler.enqueue.assert_any_call("job2")

    #
    # Scheduler executed.
    #

    scheduler.tick.assert_called_once_with(project)

    #
    # Monitor executed.
    #

    monitor.poll.assert_called_once_with(project)


def test_empty_discovery():

    watcher = MagicMock()
    scheduler = MagicMock()
    monitor = MagicMock()

    watcher.discover.return_value = []

    project = DummyProject()

    orchestrator = Orchestrator(
        project=project,
        watcher=watcher,
        scheduler=scheduler,
        monitor=monitor,
    )

    orchestrator.step()

    scheduler.enqueue.assert_not_called()

    scheduler.tick.assert_called_once_with(project)

    monitor.poll.assert_called_once_with(project)