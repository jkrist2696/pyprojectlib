"""pyproject"""
from os import path, listdir
from re import findall
from platform import python_version
from shutil import copyfile
from getpass import getuser
from requests import get
import tomli
import tomli_w
from git import Repo
from .helper import create_dirs


IGNORELIST = [
    ".versions/",
    ".users/",
    ".git/",
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


class Project:
    """project"""

    def __init__(
        self,
        projpath: str,
        version: str = "",
        remote: bool = False,
    ):
        """init"""
        if not path.exists(projpath):
            raise FileNotFoundError(projpath)
        self.path = path.realpath(projpath)
        self.name = path.basename(self.path)
        self.version = version
        self.pyversion = python_version()
        user = getuser()
        self.owner = user
        self.editors = [user]
        self.remote = remote

    def get_config(self, dirpath: str):
        """get"""
        confpath = path.join(dirpath, f"{self.name}")
        if not path.exists(confpath):
            self._save_config(confpath)
        self._load_config(confpath)
        return self

    def get_description(self) -> str:
        """Get description from README"""
        readmefile = path.join(self.path, "README.md")
        with open(readmefile, "r", encoding="utf-8") as readmereader:
            readmestr = readmereader.read()
        result = findall(r"(?s)# Description(.*?)#", readmestr)
        errstr = (
            "Please include a Description section to your README.md file."
            + f"\nReadme Path: {readmefile}"
            + f"\nDesc Search Result: {result}"
        )
        if len(result) == 0:
            raise SyntaxWarning(errstr)
        if len(result[0]) < 2:
            raise SyntaxWarning(errstr)
        description = result[0][1]
        description = description.replace("\n", "")
        return description

    def get_version(self, versionspath: str) -> str:
        """get_version"""
        if len(self.version) > 0:
            return self.version
        pkgpage = get(f"https://pypi.org/project/{self.name}/", timeout=10).text
        if path.exists(versionspath):
            versions = listdir(versionspath)
            if len(versions) == 0:
                return "0.0.1"
            versions.sort(key=lambda v: [int(n) for n in v.split(".")])
            latest_version = versions[-1]
        elif "page not found" not in pkgpage and "404" not in pkgpage:
            start_ind = pkgpage.find('<h1 class="package-header__name">') + 33
            latest_start = pkgpage[start_ind:]
            latest = latest_start[0 : latest_start.find("</h1>")]
            latest_version = latest.strip().split(" ")[1]
        else:
            return "0.0.1"
            # raise FileNotFoundError(versionspath)
        latest_split = latest_version.split(".")
        latest_split[2] = str(int(latest_split[2]) + 1)
        version = ".".join(latest_split)
        print(f"version = {latest_version} >> {version}")
        return version

    def _prompt(self):
        """prompt"""
        print("_prompt function is meant to be overwritten")

    def _save_config(self, confpath: str):
        """save"""
        self._prompt()
        classtype = type(self).__name__
        print(f"{classtype} config path: {confpath}")
        config_keys = ["name", "path", "owner", "editors", "remote"]
        items = vars(self).items()
        tomldict = {key: value for key, value in items if key in config_keys}
        with open(confpath, "wb") as writer:
            tomli_w.dump(tomldict, writer)

    def _load_config(self, confpath: str):
        """load"""
        with open(confpath, "rb") as reader:
            userdict = tomli.load(reader)
        for key, value in userdict.items():
            setattr(self, key, value)
        classtype = type(self).__name__
        print(f"{classtype} config data: {userdict}")


def init_project_dir(dirpath: str = "."):
    """create"""
    dirpath = path.realpath(dirpath)
    dirdict = {
        "src": {path.basename(dirpath): {}},
        "docs": {},
        "test": {"examples": {}},
        ".versions": {},
    }
    print(f"\nCreating Empty Project: {dirdict}\n")
    create_dirs(dirpath, dirdict)
    Repo.init(dirpath)
    # Create .gitignore file
    with open(path.join(dirpath, ".gitignore"), "w", encoding="utf-8") as writer:
        for item in IGNORELIST:
            writer.write(f"{item}\n")
    # Create requirements.txt
    with open(path.join(dirpath, "requirements.txt"), "wb") as writer:
        writer.write(b"")
    # create readme and license
    scriptpath = path.dirname(path.realpath(__file__))
    newreadme = path.join(dirpath, "README.md")
    basereadme = path.join(scriptpath, "README.temp")
    copyfile(basereadme, newreadme)
    newlicense = path.join(dirpath, "LICENSE.txt")
    baselicense = path.join(scriptpath, "LICENSE.temp")
    copyfile(baselicense, newlicense)
