"""
Written by Jason Krist
jason.krist@gm.com

Notes:

python_project.py [init/add] [directory="."] [version+=0.0.1] [name=dirname] 

OPTIONS: 
    Create Sphinx docs with cleandoc 
    Package into python module to allow PIP install ?

# ADD IDEA TO HAVE ALLOWED EDITORS IN THE CONFIG FILE

"""

from os import path, mkdir, remove
from shutil import copytree, copyfile, rmtree
from re import findall
from cleandoc import clean_all, gen_docs
from git import Repo
import pytest
from .cli import parse
from .dirs import init_repo, init_project  # pylint: disable=W0611
from .get_save import get_userdata  # pylint: disable=W0611
from . import get_save as gs


LANGUAGE = "python"


def setup_project(
    srcpath: str, repopath: str, version: str = "", test: bool = True, env: str = ""
):
    """_summary_

    Parameters
    ----------
    srcpath : str
        _description_
    version : str
        _description_
    repopath : str
        _description_
    """
    srcpath = path.realpath(srcpath)
    projname = path.basename(srcpath)
    if len(findall(r"[^_a-z]", projname)):
        raise SyntaxWarning(
            "Project Folder name must contain only"
            + " lowercase letters or underscores. Directory Name: "
            + str(projname)
        )
    repopath = path.realpath(repopath)
    print(f"\nSource Path: {srcpath}\nRepo Path: {repopath}\n")
    if (srcpath in repopath) or (repopath in srcpath):
        raise RecursionError(
            "Source path and repo path overlap! This would result in a recursive copy tree."
        )
    env = gs.get_env(repopath, projname, env=env)
    print("\n")
    if env not in ["ansa", "meta", "generic"]:
        raise SyntaxWarning("Environment must be ansa, meta, or generic.")
    repoprojpath = path.join(repopath, LANGUAGE, env)
    projpath = path.join(repoprojpath, projname)
    version = gs.get_version(projpath, version)
    update_project(srcpath, projpath, version, test=test)


def update_project(srcpath: str, projpath: str, version: str, test: bool = True):
    """_summary_
    Parameters
    ----------
    srcpath : str
        _description_
    version : str
        _description_
    projpath : str
        _description_
    test : bool
        _description_
    """
    projname = path.basename(srcpath)
    # Check for README.md, requirements.txt, src & test folders
    required_items = ["README.md", "requirements.txt", "test", f"src/{projname}"]
    for item in required_items:
        if not path.exists(path.join(srcpath, item)):
            raise FileNotFoundError(path.join(srcpath, item))
    # Check all source files for docstrings, Black, pylint, and mypy
    clean_all(path.join(srcpath, "src", projname), write=False)
    # Run pytest in test folder
    if test:
        pytest.main()  # Make sure this exits if there are errors!
    # Init repo project if it doesnt exist
    if not path.exists(projpath):
        init_project(projpath, versionsdir=True)
    # Remove last version files
    for item in required_items:
        if not path.exists(path.join(projpath, item)):
            continue
        if path.isdir(path.join(projpath, item)):
            rmtree(path.join(projpath, item))
        else:
            remove(path.join(projpath, item))
    # Copy new files to repo and backup in .versions folder
    mkdir(path.join(projpath, ".versions", version))
    for item in required_items:
        if path.isdir(path.join(srcpath, item)):
            copytree(path.join(srcpath, item), path.join(projpath, item))
            copytree(
                path.join(srcpath, item),
                path.join(projpath, ".versions", version, item),
            )
        elif path.isfile(path.join(srcpath, item)):
            copyfile(path.join(srcpath, item), path.join(projpath, item))
            copyfile(
                path.join(srcpath, item),
                path.join(projpath, ".versions", version, item),
            )
        else:
            raise FileNotFoundError(path.join(srcpath, item))
    # Create Sphinx docs -- maybe add copy or none options?
    gen_docs(path.join(projpath, "src", projname), release=version)
    # Add all and commit with version as message
    repo_obj = Repo(projpath)
    repo_obj.git.add(all=True)
    repo_obj.index.commit(version)


def package_module(pkgpath: str, version: str, author: str, email: str):
    """_summary_
    Parameters
    ----------
    pkgpath : str
        _description_
    version : str
        _description_
    author : str
        _description_
    email : str
        _description_
    """
    confdict = gs.get_config(pkgpath)
    description = gs.get_description(pkgpath)
    # Get dependencies from requirements.txt
    reqfile = path.join(pkgpath, "requirements.txt")
    with open(reqfile, "r", encoding="utf-8") as reqreader:
        reqlines = reqreader.readlines()
    # Write params into setup file
    param_str = f"""
kwargs["version"] = "{version}"
kwargs["author"] = "{author}"
kwargs["author_email"] = "{email}"
kwargs["description"] = "{description}"
kwargs["python_requires"] = "{confdict["python_version"]}"
kwargs["install_requires"] = {reqlines}
"""
    param_str = (
        param_str
        + 'kwargs["entry_points"] = {"console_scripts": [f"{pkgname}={pkgname}:{'
        + confdict["entry_point"]
        + '}"]}'
    )
    return param_str  # remove this
    # Run setup.py file


def cli_main():
    """runs cli parser and setup_project fxn."""
    _args = parse()
    # run functions here depending on parse results

