"""pyproject"""
from os import path, listdir, mkdir
from re import findall
from platform import python_version
from getpass import getuser
from requests import get
import tomli
import tomli_w
from . import constants as CONS  # type: ignore # pylint: disable=E0611,E0401


class Project:
    """project"""

    def __init__(self, projpath: str, version: str = ""):
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
        self.config_keys = ["name", "path", "owner", "editors", "remote"]

    def get_config(self, dirpath: str):
        """get"""
        confpath = path.join(dirpath, f"{self.name}")
        if not path.exists(confpath):
            self._save_config(confpath)
        self._load_config(confpath)
        return self

    def get_description(self) -> str:
        """Get description from README"""
        readmefile = path.join(self.path, CONS.READFILE)
        with open(readmefile, "r", encoding="utf-8") as readmereader:
            readmestr = readmereader.read()
        result = findall(CONS.DESC_REGEX, readmestr)
        errstr = (
            f"Please include a Description section to your {CONS.READFILE} file."
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
        try:
            pkgpage = get(f"{CONS.PYPI}/{self.name}/", timeout=10).text
        except ConnectionError as _error:
            pkgpage = "page not found"
        notfoundcheck1 = "page not found" in pkgpage.lower()
        notfoundcheck2 = "error code 404" in pkgpage.lower()
        notfoundcheck3 = "couldn't find this page" in pkgpage.lower()
        if path.exists(versionspath):
            versions = listdir(versionspath)
            if len(versions) == 0:
                return "0.0.1"
            versions.sort(key=lambda v: [int(n) for n in v.split(".")])
            latest_version = versions[-1]
        elif not any([notfoundcheck1, notfoundcheck2, notfoundcheck3]):
            start_ind = pkgpage.find('<h1 class="package-header__name">') + 33
            latest_start = pkgpage[start_ind:]
            latest = latest_start[0 : latest_start.find("</h1>")]
            latest_version = latest.strip().split(" ")[1]
        else:
            CONS.log().debug("Version could not be found")
            mkdir(versionspath)
            return "0.0.1"
        latest_split = latest_version.split(".")
        latest_split[2] = str(int(latest_split[2]) + 1)
        version = ".".join(latest_split)
        logstr = f'Project "{self.name}" Version (old >> new) = {latest_version} >> {version}'
        CONS.log().info(logstr)
        return version

    def _prompt(self):
        """prompt"""
        CONS.log().debug("_prompt function is meant to be overwritten")

    def _save_config(self, confpath: str):
        """save"""
        self._prompt()
        classtype = type(self).__name__
        logstr = f"{classtype} config path: {confpath}"
        CONS.log().debug(logstr)
        items = vars(self).items()
        tomldict = {key: value for key, value in items if key in self.config_keys}
        with open(confpath, "wb") as writer:
            tomli_w.dump(tomldict, writer)

    def _load_config(self, confpath: str):
        """load"""
        with open(confpath, "rb") as reader:
            userdict = tomli.load(reader)
        for key, value in userdict.items():
            setattr(self, key, value)
        classtype = type(self).__name__
        logstr = f"{classtype} config data: {userdict}"
        CONS.log().debug(logstr)
