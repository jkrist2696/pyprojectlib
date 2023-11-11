"""helpers"""
from os import path, mkdir, remove
from shutil import rmtree
from typing import Any, Tuple
from subprocess import run


def prompt_user(prompt: str, default: str):
    """Prompt user for input if default is empty string
    Parameters
    ----------
    prompt : str
        text prompt to display to user
    default : str
        value returned if it's length is > 0
    """
    if len(default) > 0:
        return default
    return input(prompt)


def create_dirs(srcpath: str, dirdict: dict[str, Any]):
    """_summary_
    Parameters
    ----------
    srcpath : str
        _description_
    dirdict : dict[dict]
        _description_
    """
    mkdir(srcpath)
    for dirname, subdirdict in dirdict.items():
        newsrcpath = path.join(srcpath, dirname)
        if len(subdirdict) == 0:
            mkdir(newsrcpath)
            return
        create_dirs(newsrcpath, subdirdict)


def remove_item(itempath: str):
    """remote item"""
    if not path.exists(itempath):
        return
    if path.isdir(itempath):
        rmtree(itempath)
    else:
        remove(itempath)


def run_capture_out(cmd: list[str], **kwargs) -> Tuple[str, str]:
    """Run subprocess command and return the stdout and stderr.

    Parameters
    ----------
    cmd : list[str]
        Pass list of shell commands to subprocess.run
    shell : bool
        Pass shell keyword argument to subprocess.run

    Returns
    -------
    stdout  : str
        Standard Output returned from shell
    stderr : str
        Standard Error returned from shell

    """
    proc = run(
        cmd,
        capture_output=True,
        encoding="utf-8",
        check=False,
        errors="ignore",
        **kwargs,
    )
    return proc.stdout, proc.stderr
