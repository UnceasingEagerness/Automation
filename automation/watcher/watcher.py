from automation.job.job import Job
from automation.state.state_manager import StateManager
from automation.utils.git_utils import get_new_commits


class Watcher:

    def __init__(self, state_manager=None):

        if state_manager is None:
            state_manager = StateManager()

        self.state_manager = state_manager

    def discover(self, project) -> list[Job]:
        """
        Discover new commits for a project and convert them into Jobs.

        Returns
        -------
        list[Job]
            Jobs in chronological order.
        """

        state = self.state_manager.load(project.name)

        commits = get_new_commits(
            repo_path=project.local_path,
            branch=project.branch,
            last_seen_commit=state.last_seen_commit,
        )

        jobs = []

        for commit in commits:

            jobs.append(
                Job(
                    project=project,
                    commit=commit.sha,
                )
            )

        if commits:

            state.last_seen_commit = commits[-1].sha

            self.state_manager.save(state)

        return jobs