from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


class ArtifactManager:
    """
    Organizes experiment outputs into a standard layout.

    artifacts/
        PROJECT/
            run_000001/
                config.yaml
                metrics.json
                stdout.log
                stderr.log
                checkpoints/
                tensorboard/
    """

    def __init__(self, root: str | Path = "artifacts"):

        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def create_run(
        self,
        project: str,
    ) -> Path:

        project_dir = self.root / project
        project_dir.mkdir(parents=True, exist_ok=True)

        existing = sorted(project_dir.glob("run_*"))

        run_number = len(existing) + 1

        run_dir = project_dir / f"run_{run_number:06d}"

        run_dir.mkdir()

        (run_dir / "checkpoints").mkdir()
        (run_dir / "tensorboard").mkdir()

        return run_dir

    def save_metrics(
        self,
        run_dir: Path,
        metrics: dict,
    ):

        with open(run_dir / "metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

    def save_config(
        self,
        run_dir: Path,
        config_path: Path,
    ):

        shutil.copy2(config_path, run_dir / config_path.name)

    def save_stdout(
        self,
        run_dir: Path,
        stdout_file: Path,
    ):

        shutil.copy2(stdout_file, run_dir / "stdout.log")

    def save_stderr(
        self,
        run_dir: Path,
        stderr_file: Path,
    ):

        shutil.copy2(stderr_file, run_dir / "stderr.log")

    def add_checkpoint(
        self,
        run_dir: Path,
        checkpoint: Path,
    ):

        destination = run_dir / "checkpoints" / checkpoint.name

        shutil.copy2(checkpoint, destination)

        return destination

    def add_tensorboard(
        self,
        run_dir: Path,
        tensorboard_directory: Path,
    ):

        destination = run_dir / "tensorboard"

        if destination.exists():
            shutil.rmtree(destination)

        shutil.copytree(
            tensorboard_directory,
            destination,
        )

    def finish(
        self,
        run_dir: Path,
    ):

        with open(run_dir / "completed.txt", "w") as f:
            f.write(datetime.now().isoformat())