"""user"""
from os import path
from getpass import getuser
import tomli
import tomli_w
from .helper import prompt_user


class User:
    """user"""

    def __init__(self, name: str = "", email: str = "", gituser: str = ""):
        """init"""
        self.user = getuser()
        self.name = name
        self.email = email
        self.gituser = gituser

    def get_config(self, dirpath: str):
        """get"""
        confpath = path.join(dirpath, f"{self.user}")
        if not path.exists(confpath):
            self._save_config(confpath)
        self._load_config(confpath)
        return self

    def _prompt(self):
        """prompt"""
        self.name = prompt_user("Name: ", self.name)
        self.email = prompt_user("Email: ", self.email)
        self.gituser = prompt_user("Github Username", self.gituser)

    def _save_config(self, confpath: str):
        """save"""
        self._prompt()
        classtype = type(self).__name__
        print(f"{classtype} config path: {confpath}")
        with open(confpath, "wb") as writer:
            tomli_w.dump(vars(self), writer)

    def _load_config(self, confpath: str):
        """load"""
        with open(confpath, "rb") as reader:
            userdict = tomli.load(reader)
        for key, value in userdict.items():
            setattr(self, key, value)
        classtype = type(self).__name__
        print(f"{classtype} config data: {vars(self)}")
