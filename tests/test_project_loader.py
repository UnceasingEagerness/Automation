from automation.core.project_loader import ProjectLoader


def test_project_loader():

    projects = ProjectLoader.load_all()

    assert len(projects) > 0

    project = projects[0]

    assert project.name == "MARL"

    assert project.branch == "main"

    assert project.local_path != ""