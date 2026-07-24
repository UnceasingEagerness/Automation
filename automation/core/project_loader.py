from pathlib import Path

from automation.core.project import Project
from automation.utils.yaml_utils import load_yaml


class ProjectLoader:

    @staticmethod
    def load(path: str | Path) -> Project:

        cfg = load_yaml(path)

        return Project(

            name=cfg["project"]["name"],

            repo_url=cfg["repository"]["url"],
            branch=cfg["repository"]["branch"],
            local_path=cfg["local"]["path"],

            training_command=cfg["training"]["command"],

            experiment_dir=cfg["outputs"]["experiments"],
            checkpoint_dir=cfg["outputs"]["checkpoints"],

            wandb=cfg["monitoring"]["wandb"],

            telegram=cfg["notifications"]["telegram"],

            google_drive=cfg["upload"]["google_drive"]
        )

    @staticmethod
    def load_all(project_folder="projects"):

        projects = []

        for yaml_file in sorted(Path(project_folder).glob("*.yaml")):

            projects.append(ProjectLoader.load(yaml_file))

        return projects