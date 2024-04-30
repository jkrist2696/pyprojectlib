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

from os import path, listdir
from typing import Dict
from re import findall
from getpass import getuser
import yaml


LANGUAGE = "python"


def get_version(projpath: str, version: str = "") -> str:
    """_summary_
    Parameters
    ----------
    projpath : str
        _description_
    version : str, optional
        _description_, by default ""
    Returns
    -------
    version : str
        _description_
    """
    if len(version) > 0:
        return version
    versions = listdir(path.join(projpath, ".versions"))
    if len(versions) == 0:
        return "0.0.1"
    versions.sort(key=lambda v: [int(n) for n in v.split(".")])
    last_version = versions[-1].split(".")
    version = ".".join(last_version[0:2] + [str(int(last_version[2]) + 1)])
    return version


def get_env(repopath: str, projname: str, env: str = ""):
    """Get environment path of package in repo
    Parameters
    ----------
    repopath : str
        _description_
    pkgname : str
        _desc_
    env : str , optional
        _desc_
    """
    langpath = path.join(repopath, LANGUAGE)
    envfile = path.join(langpath, ".projects", f"{projname}")
    if path.exists(envfile):
        with open(envfile, "r", encoding="utf-8") as userreader:
            envfilestr = userreader.read()
            projdata = yaml.safe_load(envfilestr)
    else:
        projdata = save_env(envfile, env=env)
    print(f"projdata: {projdata}")
    return projdata["env"]


def save_env(envfile: str, env: str = ""):
    """_summary_
    Parameters
    ----------
    envfile : str
        _description_
    env : str, optional
        _description_, by default ""
    """
    projdata = {}
    projdata["env"] = prompt_user("Environment (ansa, meta, or generic): ", env)
    with open(envfile, "w", encoding="utf-8") as writer:
        writer.write(yaml.dump(projdata))
    return projdata


def get_userdata(repopath: str, name: str = "", email: str = ""):
    """Get user's name and email
    Parameters
    ----------
    repopath : str
        _description_
    """
    user = getuser()
    userfile = path.join(repopath, ".users", f"{user}")
    if path.exists(userfile):
        with open(userfile, "r", encoding="utf-8") as userreader:
            userfilestr = userreader.read()
            userdata = yaml.safe_load(userfilestr)
    else:
        userdata = save_userdata(userfile, name=name, email=email)
    print(f"userdata: {userdata}")
    return userdata


def save_userdata(userfile: str, name: str = "", email: str = ""):
    """Save Name and Email in users directory
    Parameters
    ----------
    userfile : str
        _description_
    name : str, optional
        _description_, by default ""
    email : str, optional
        _description_, by default ""
    """
    userdata = {}
    userdata["name"] = prompt_user("Your Name: ", name)
    userdata["email"] = prompt_user("GM Email: ", email)
    with open(userfile, "w", encoding="utf-8") as userwriter:
        userwriter.write(yaml.dump(userdata))
    return userdata


def get_description(pkgpath: str) -> str:
    """_summary_
    Parameters
    ----------
    pkgpath : str
        _description_
    Returns
    -------
    str
        _description_
    """
    # Get description from README
    readmefile = path.join(pkgpath, "README.md")
    with open(readmefile, "r", encoding="utf-8") as readmereader:
        readmestr = readmereader.read()
        result = findall("# Description(.*?)#", readmestr)
        if len(result) == 0:
            raise SyntaxWarning(
                "Please include a Description section to your README.md file."
            )
    description = result[0][1]
    return description


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


def get_config(pkgpath: str, pyversion: str = "", entry: str = "") -> Dict[str, str]:
    """_summary_
    Parameters
    ----------
    pkgpath : str
        _description_
    Returns
    -------
    dict[str,str]
        _description_
    """
    conffile = path.join(pkgpath, ".cae_conf")
    if path.exists(conffile):
        with open(conffile, "r", encoding="utf-8") as confreader:
            confstr = confreader.read()
            confdict = yaml.safe_load(confstr)
    else:
        # Save Name and Email in users directory
        confdict = {}
        confdict["python_version"] = prompt_user("Python Version: ", pyversion)
        confdict["entry_point"] = prompt_user("Entry Point Function: ", entry)
        with open(confdict, "r", encoding="utf-8") as confwriter:
            confwriter.write(yaml.dump(confdict))
    return confdict

