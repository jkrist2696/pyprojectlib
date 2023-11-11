"""pypackage"""
from os import path
import pipreqs.pipreqs as pr  # type: ignore # pylint: disable=E0401
from .helper import prompt_user
from .pyproject import Project
from .pyuser import User


TOMLSTR_START = """[project]
license = {{ file = "LICENSE.txt" }}
readme = "README.md"
classifiers = [
    "Programming Language :: Python :: 3",
    "OSI Approved :: GNU General Public License v3 (GPLv3)",
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix',
]

"""


class Package(Project):
    """package"""

    def __init__(
        self, pkgpath: str, clifxn: str = "", version: str = "", remote: bool = False
    ):
        """init"""
        self.clifxn = clifxn
        super().__init__(pkgpath, version=version, remote=remote)
        self.description = self.get_description()
        self.dep_pkgs: list[str] = []
        self.get_dep_pkgs()
        self.version = self.get_version()
        scriptpath = path.dirname(path.abspath(__file__))
        userconfig = path.join(scriptpath, ".users")
        self.author = User().get_config(userconfig)

    def get_dep_pkgs(self):
        """get dep pkgs"""
        # TODO: add logic to eliminate duplicates with set
        self._get_pipreqs()
        self._get_requirements()
        print(f"dependent packages: {self.dep_pkgs}")

    def save_toml(self):
        """save_toml"""
        depstr = ",".join([f'"{pkg}"' for pkg in self.dep_pkgs])
        toml_str = TOMLSTR_START + f'name = "{self.name}"\n'
        toml_str += f'name = "{self.name}"\n'
        toml_str += f'version = "{self.version}"\n'
        author = self.author
        toml_str += 'authors = [{{ name = "'
        toml_str += f'{author.name}", email = "{author.email}" }}]\n'
        toml_str += f'description = "{self.description}"\n'
        toml_str += f'requires-python = ">={self.pyversion}"\n'
        toml_str += f"dependencies = [{depstr}]\n"
        if len(self.clifxn) > 0:
            toml_str += '[project.scripts]\n"'
            toml_str += f'{self.name} = "{self.name}:{self.clifxn}"\n'
        if len(author.gituser) > 0:
            toml_str += '[project.urls]\n"Homepage" = "https://github.com/'
            toml_str += f'{author.gituser}/{self.name}"\n'
        tomlpath = path.join(self.path, "pyproject.toml")
        with open(tomlpath, "wb") as writer:
            writer.write(bytes(toml_str))

    def build(self):
        """build"""
        # SETUP PROCESS BELOW
        # python -m build
        # twine check dist/*
        # pip3 install .
        # twine upload dist/*
        print("monitor output of each step")

    def _prompt(self):
        """prompt"""
        self.clifxn = prompt_user("Command-Line Interface Function: ", self.clifxn)

    def _get_pipreqs(self):
        """Get Module Dependencies and their Versions with pipreqs"""
        imports = pr.get_all_imports(f"./src/{self.name}", encoding="utf-8")
        pkgnames = pr.get_pkg_names(imports)
        pkgdicts_all = pr.get_import_local(pkgnames, encoding="utf-8")
        pkgdicts: list = []
        for pkgdict_orig in pkgdicts_all:
            pkgdicts_names = [pkgdict["name"] for pkgdict in pkgdicts]
            if pkgdict_orig["name"] not in pkgdicts_names:
                pkgdicts.append(pkgdict_orig)
        pkglist = [pkgdict["name"] + ">=" + pkgdict["version"] for pkgdict in pkgdicts]
        self.dep_pkgs.extend(pkglist)

    def _get_requirements(self):
        """Get dependencies from requirements.txt"""
        reqfile = path.join(self.path, "requirements.txt")
        with open(reqfile, "r", encoding="utf-8") as reqreader:
            reqlines = reqreader.readlines()
        self.dep_pkgs.extend(reqlines)


# TOML EXTRAS BELOW:

# keywords = [""] add later?
# 'Operating System :: POSIX',
# 'Operating System :: MacOS',
# [tool.setuptools] need anything here?
# [tool.setuptools.packages.find]
# where = ["src"]
# [build-system] this is default right?
# requires = ["setuptools", "wheel"]
# build-backend = "setuptools.build_meta"


# I think below is covered automatically? I should test though
# ["pkg.assets"]
# pykwargs["package_data"] = ({f"{pkgname}": ["assets/*"]},)
# pykwargs["include_package_data"] = True
