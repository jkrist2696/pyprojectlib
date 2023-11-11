"""
Written by Jason Krist
"""

from os import path, mkdir
from shutil import copytree, copyfile
from re import findall
from git import Repo
import pytest  # pylint: disable=E0401
from cleandoc import clean_all, gen_docs  # type: ignore # pylint: disable=E0401
from .helper import create_dirs, remove_item, prompt_user
from .pyuser import User
from .pyproject import Project, init_project_dir
from .pypackage import package_project


class Repository:
    """local repo for saving code modules"""

    def __init__(self, repopath: str, user: User):
        """init"""
        self.path = path.realpath(repopath)
        self.name = path.basename(repopath)
        self.projects: list[RepoProject] = []
        self.projpath = path.join(repopath, ".projects")
        self.userpath = path.join(repopath, ".users")
        self.user = user
        self.user.get_config(self.userpath)

    def push(
        self, pkgpath: str, relpath: str = "", test: bool = True, version: str = ""
    ):
        """add project"""
        project = RepoProject(pkgpath, self, relpath, version=version)
        project.update(test)
        self.projects.append(project)
        return project

    def pull(self, pkgname: str, version: str = ""):
        """get project version"""
        print(f"add pulling here {pkgname} {version}")


class RepoProject(Project):
    """repoproject"""

    def __init__(self, pkgpath: str, repo: Repository, relpath: str, **kwargs):
        """init"""
        super().__init__(pkgpath, **kwargs)
        self.repo = repo
        self._check_args()
        self.relpath = relpath
        self.repoprojpath = path.join(repo.path, self.relpath, self.name)
        self.version = self.get_version(path.join(self.repoprojpath, ".versions"))
        self.versionpath = path.join(self.repoprojpath, ".versions", self.version)
        self.required = [
            "README.md",
            "requirements.txt",
            "test",
            f"src/{self.name}",
        ]

    def update(self, test: bool):
        """check code quality, then copy over new version"""
        self._check_required()
        clean_all(path.join(self.path, "src", self.name), write=False, skip=True)
        if test:
            pytest.main()  # Make sure this exits if there are errors!
        if not path.exists(self.repoprojpath):
            init_project_dir(self.repoprojpath)
        self.get_config(self.repo.projpath)
        self._remove_last_version()
        self._copy_and_backup()
        gen_docs(path.join(self.repoprojpath, "src", self.name), release=self.version)
        git_repo = Repo(self.repoprojpath)
        git_repo.git.add(all=True)
        git_repo.index.commit(self.version)
        git_repo.close()

    def package(self, **kwargs):
        """build project into package"""
        package_project(self.repoprojpath, self.repo.user, **kwargs)

    def _prompt(self):
        """prompt"""
        self.relpath = prompt_user("Relative Path in Repo: ", self.relpath)

    def _check_args(self):
        """check args"""
        if len(findall(r"[^_a-z]", self.name)):
            raise SyntaxWarning(
                "Project Folder name must contain only"
                + " lowercase letters or underscores. Directory Name: "
                + str(self.name)
            )
        print(f"\nSource Path: {self.path}\nRepo Path: {self.repo.path}\n")
        if (self.path in self.repo.path) or (self.repo.path in self.path):
            raise RecursionError(
                "Source path and repo path overlap! This would result in a recursive copy tree."
            )

    def _check_required(self):
        """check"""
        for item in self.required:
            if not path.exists(path.join(self.path, item)):
                raise FileNotFoundError(path.join(self.path, item))

    def _remove_last_version(self):
        """remove old files"""
        for item in self.required:
            remove_item(path.join(self.repoprojpath, item))

    def _copy_and_backup(self):
        """copy backup"""
        mkdir(self.versionpath)
        for item in self.required:
            srcpath = path.join(self.path, item)
            repopath = path.join(self.repoprojpath, item)
            backuppath = path.join(self.versionpath, item)
            if path.isdir(srcpath):
                copytree(srcpath, repopath)
                copytree(srcpath, backuppath)
            elif path.isfile(srcpath):
                copyfile(srcpath, repopath)
                copyfile(srcpath, backuppath)
            else:
                raise FileNotFoundError(path.join(srcpath, item))


def init_repo_dir(dirpath: str):
    """create"""
    print(f"Creating Empty Repository: {dirpath}")
    dirdict: dict[str, dict] = {
        ".users": {},
        ".projects": {},
    }
    create_dirs(dirpath, dirdict)
