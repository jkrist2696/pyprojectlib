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

from os import path, mkdir
from typing import Dict, Any
from git import Repo


LANGUAGE = "python"


def init_project(srcpath: str, versionsdir: bool = False):
    """_summary_
    Parameters
    ----------
    srcpath : str
        _description_
    versionsdir : bool, optional
        _description_, by default False
    """
    dirdict = {
        "src": {path.basename(srcpath): {}},
        "docs": {},
        "test": {"examples": {}},
    }
    if versionsdir:
        # dirname = path.basename(srcpath)
        # dirdict = {"latest": {dirname: dirdict}}
        dirdict[".versions"] = {}
    print(f"\nInitializing Project Structure: {dirdict}\n")
    mkdir(srcpath)
    create_proj_dirs(srcpath, dirdict)
    Repo.init(srcpath)
    # Create .gitignore file
    ignorelist = [
        ".versions",
        ".mypy_cache/",
        ".vscode/",
        "build/",
        "dist/",
        "docs/conf.txt",  # "src/proj/__pycache__
        "test/__pycache__",
        "test/.mypy_cache/",
        "test/docs",
        "test/cleandoc_log.txt",
    ]
    with open(path.join(srcpath, ".gitignore"), "w", encoding="utf-8") as gitignore:
        for item in ignorelist:
            gitignore.write(f"{item}\n")
        if versionsdir:
            gitignore.write(".versions/\n")


def init_repo(repopath: str):
    """_summary_
    Parameters
    ----------
    repopath : str
        _description_
    """
    print(f"Initiating Repository: {repopath}")
    basepath, reponame = path.split(repopath)
    dirdict = {
        reponame: {
            ".users": {},
            LANGUAGE: {".projects": {}, "generic": {}, "meta": {}, "ansa": {}},
            "shell": {},
            "PowerShell": {},
        }
    }
    create_proj_dirs(basepath, dirdict)


def create_proj_dirs(srcpath: str, dirdict: Dict[str, Any]):
    """_summary_
    Parameters
    ----------
    srcpath : str
        _description_
    dirdict : dict[dict]
        _description_
    """
    for dirname, subdirdict in dirdict.items():
        newsrcpath = path.join(srcpath, dirname)
        mkdir(newsrcpath)
        if len(subdirdict) > 0:
            create_proj_dirs(newsrcpath, subdirdict)

