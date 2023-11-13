"""helpers"""
from os import path, makedirs, remove
from sys import stdout
import logging
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
    for dirname, subdirdict in dirdict.items():
        newsrcpath = path.join(srcpath, dirname)
        makedirs(newsrcpath, exist_ok=True)
        if len(subdirdict) > 0:
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


def config_log(file: str = "", level=logging.INFO):
    """Configure log file using logging module

    Parameters
    ----------
    file : str = ""
        Path to logfile to write
    level
        logging.level to pass to logger

    Returns
    -------
    logger object

    """
    logname = "pyprojectlib"
    logger = logging.getLogger(logname)
    if logger.hasHandlers():
        return logger
    logging.basicConfig()  # level=logging.WARN
    fs = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    dfs = "%d-%m-%y | %H:%M:%S"
    if len(file) > 0:
        if path.exists(file):
            remove(file)
        file_handler = logging.FileHandler(file)
        print(f"logfile path: {path.realpath(file)}\n")
        file_handler.setFormatter(logging.Formatter(fs, dfs, "%"))
        logger.addHandler(file_handler)
    stdout_handler = logging.StreamHandler(stdout)
    stdout_handler.setFormatter(logging.Formatter(fs, dfs, "%"))
    logger.addHandler(stdout_handler)
    logger.propagate = False
    logger.setLevel(level)
    return logger


def check_version_format(version: str):
    """check if version string abides by criteria"""
    versionsplit = version.split(".")
    errstr = (
        "Version string must be in format X.Y.Z where X, Y, "
        + f"and Z are integers.\n    version: {version}"
    )
    if len(versionsplit) != 3:
        raise SyntaxError(errstr)
    for splitnum in versionsplit:
        try:
            int(splitnum)
        except ValueError as error:
            raise SyntaxError(errstr) from error


def attrs_to_dict(obj, namelist: list[str]) -> dict:
    """create kwargs from list of arg names"""
    kwdict = {}
    for name in namelist:
        kwdict[name] = getattr(obj, name)
    return kwdict
