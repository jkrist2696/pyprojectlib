"""
Written by Jason Krist
"""

from os import path, listdir
from typing import Dict
from re import findall
from getpass import getuser
from requests import get
import tomli
import tomli_w

LANGUAGE = "python"
# USERFIELDS = ["Name", "Email"]  # if remote? , "Github Username"


def get_version_local(projpath: str, version: str = "") -> str:
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


def get_version_remote(projname: str, version: str = "") -> str:
    """_summary_
    Parameters
    ----------
    projname : str
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
    pkgpage = get(f"https://pypi.org/project/{projname}/", timeout=10).text
    if "page not found" in pkgpage or "404" in pkgpage:
        return "0.0.1"
    start_ind = pkgpage.find('<h1 class="package-header__name">') + 33
    latest_start = pkgpage[start_ind:]
    latest = latest_start[0 : latest_start.find("</h1>")]
    latest_version = latest.strip().split(" ")[1]
    print(f"previous version: {latest_version}")
    latest_split = latest_version.split(".")
    latest_split[2] = str(int(latest_split[2]) + 1)
    version = ".".join(latest_split)
    return version


def get_projdata(repopath: str, projname: str, env: str = ""):
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
    projfile = path.join(langpath, ".projects", f"{projname}")
    if path.exists(projfile):
        with open(projfile, "rb") as reader:
            projdata = tomli.load(reader)
    else:
        projdata = save_projdata(projfile, env=env)
    print(f"projdata: {projdata}")
    return projdata


def save_projdata(projfile: str, env: str = ""):
    """_summary_
    Parameters
    ----------
    projfile : str
        _description_
    env : str, optional
        _description_, by default ""
    """
    projdata = {}
    projdata["env"] = prompt_user("Environment Name: ", env)
    with open(projfile, "wb") as writer:
        tomli_w.dump(projdata, writer)
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
        with open(userfile, "rb") as reader:
            userdata = tomli.load(reader)
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
    # TODO: add other fields?
    userdata["name"] = prompt_user("Name: ", name)
    userdata["email"] = prompt_user("Email: ", email)
    userdata["username"] = prompt_user("Github Username", "")
    with open(userfile, "wb") as writer:
        tomli_w.dump(userdata, writer)
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


def get_config(pkgpath: str, entry: str = "") -> Dict[str, str]:
    # parser.add_argument("-version", "-v", default="", help=reh)
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
    conffile = path.join(pkgpath, ".py_conf")
    if path.exists(conffile):
        with open(conffile, "rb") as reader:
            confdict = tomli.load(reader)
    else:
        # Save Name and Email in users directory
        confdict = {}
        # confdict["python_version"] = prompt_user("Python Version: ", pyversion)
        confdict["entry_point"] = prompt_user(
            "Command-Line Interface Function: ", entry
        )
        with open(conffile, "rb") as writer:
            tomli_w.dump(confdict, writer)
    return confdict
