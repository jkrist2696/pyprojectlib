"""
Written by Jason Krist

# TODO: (HIGH) complete the packaging automation and add to test
# TODO: (MED) add user permissions in .projects file (list of usernames who can edit)
# TODO: (LOW) allow creation of sub-environments (i.e. "generic">"aero")
# TODO: (LOW) make all printouts logs instead
# TODO: use just specifies path to push pkg and repo is recognized there auto?


"""

from .cli import parse
from .pyproject import init_project_dir
from .pyrepo import Repository, init_repo_dir  # type: ignore # pylint: disable=E0401,C0413


def cli_main():
    """runs cli parser and setup_project fxn."""
    _args = parse()
    # run functions here depending on parse results
