from dataclasses import dataclass


@dataclass(slots=True)
class Project:

    # Project Information
    name: str

    # Git
    repo_url: str
    branch: str
    local_path: str

    # Training
    training_command: str

    # Outputs
    experiment_dir: str
    checkpoint_dir: str

    # Features
    wandb: bool
    telegram: bool
    google_drive: bool