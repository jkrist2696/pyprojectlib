"""pypackage"""
from os import path, mkdir
import sys
from re import split
import pipreqs.pipreqs as pr  # type: ignore # pylint: disable=E0401
from .helper import prompt_user, run_capture_out
from .pyuser import User
from .pyproject import Project


TOMLSTR_START = """[project]
license = { text = "GNU GPLv3" }
readme = "README.md"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix',
]

"""


class Package(Project):
    """package"""

    def __init__(self, pkgpath: str, user: User, clifxn: str = "", **kwargs):
        """init"""
        self.clifxn = clifxn
        super().__init__(pkgpath, **kwargs)
        self.description = self.get_description()
        self.dep_pkgs: list[str] = []
        self.get_dep_pkgs()
        self.version = self.get_version(path.join(self.path, ".versions"))
        scriptpath = path.dirname(path.realpath(__file__))
        userconfig = path.join(scriptpath, "..", "..", ".users")
        if not path.exists(userconfig):
            mkdir(userconfig)
        self.author = user
        self.author.get_config(userconfig)

    def get_dep_pkgs(self):
        """get dep pkgs"""
        self._get_pipreqs()
        self._get_requirements()
        self._remove_dep_dups()
        print(f"dependent packages: {self.dep_pkgs}")

    def save_toml(self):
        """save_toml"""
        depstr = ",".join([f'"{pkg}"' for pkg in self.dep_pkgs])
        toml_str = TOMLSTR_START + f'name = "{self.name}"\n'
        toml_str += f'version = "{self.version}"\n'
        author = self.author
        toml_str += 'authors = [{ name = "'
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
            writer.write(bytes(toml_str, encoding="utf-8"))

    def build(self):
        """build"""
        pyexe = sys.executable
        envpath = path.dirname(pyexe)
        pipexe = path.join(envpath, "Scripts", "pip3")
        twineexe = path.join(envpath, "Scripts", "twine")
        arglists = [
            [pyexe, "-m", "build"],
            [twineexe, "check", "dist/*"],
            [pipexe, "install", "."],
            # ["twine", "upload", "dist/*"], # twine upload dist/*
        ]
        for arglist in arglists:
            stdout, stderr = run_capture_out(arglist, cwd=self.path)
            print(f"exe: {arglist[0]}\n")
            print(f"stdout:\n{stdout}\n")
            if len(stderr.strip()) > 0:
                print(f"blderr:\n{stderr}\n")
                raise ChildProcessError(stderr)

    def _prompt(self):
        """prompt"""
        self.clifxn = prompt_user("Command-Line Interface Function: ", self.clifxn)

    def _get_pipreqs(self):
        """Get Module Dependencies and their Versions with pipreqs"""
        srcpath = path.join(self.path, "src", self.name)
        imports = pr.get_all_imports(srcpath, encoding="utf-8")
        pkgnames = pr.get_pkg_names(imports)
        pkgdicts_all = pr.get_import_local(pkgnames, encoding="utf-8")
        pkgdicts: list = []
        for pkgdict_orig in pkgdicts_all:
            pkgdicts_names = [pkgdict["name"] for pkgdict in pkgdicts]
            if pkgdict_orig["name"] not in pkgdicts_names:
                pkgdicts.append(pkgdict_orig)
        pkglist = [pkgdict["name"] + ">=" + pkgdict["version"] for pkgdict in pkgdicts]
        print(f"pipreqs packages: {pkglist}")
        self.dep_pkgs.extend(pkglist)

    def _get_requirements(self):
        """Get dependencies from requirements.txt"""
        reqfile = path.join(self.path, "requirements.txt")
        with open(reqfile, "r", encoding="utf-8") as reqreader:
            reqlines = reqreader.readlines()
        reqlines = [line.strip() for line in reqlines if len(line.strip()) > 0]
        print(f"requirements.txt packages: {reqlines}")
        self.dep_pkgs.extend(reqlines)

    def _remove_dep_dups(self):
        """remove duplicate packages"""
        new_dep_pkgs = []
        new_pkgnames = []
        for pkgstr in self.dep_pkgs:
            pkgname = split("~<>=", pkgstr)[0]
            if pkgname in new_pkgnames:
                continue
            new_dep_pkgs.append(pkgstr)
            new_pkgnames.append(pkgname)


def package_project(pkgpath: str, user: User, **kwargs):
    """package"""
    pkg = Package(path.realpath(pkgpath), user, **kwargs)
    pkg.save_toml()
    pkg.build()


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
