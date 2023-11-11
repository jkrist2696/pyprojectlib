"""
Written by Jason Krist
"""

from os import path, mkdir, makedirs
from shutil import copytree, copyfile
from re import findall
from git import Repo
import pytest  # pylint: disable=E0401
from cleandoc import clean_all, gen_docs  # type: ignore # pylint: disable=E0401
from .helper import create_dirs, remove_item
from .pyproject import Project

# projfile = path.join(langpath, ".projects", f"{projname}")
# userfile = path.join(repopath, ".users", f"{user}")


class Repository:
    """repo"""

    def __init__(self, repopath: str):
        """init"""
        self.path = path.abspath(repopath)
        self.name = path.basename(repopath)
        self.projects: list[str] = []
        self.projpath = path.join(repopath, ".projects")
        self.userpath = path.join(repopath, ".users")
        self.required = [
            "README.md",
            "requirements.txt",
            "test",
            f"src/{self.name}",
        ]

    def create(self):
        """create"""
        print(f"Creating Empty Repository: {self.path}")
        dirdict = {
            ".users": {},
            "python": {".projects": {"generic": {}}},
        }
        create_dirs(self.path, dirdict)


class RepoProject(Project):
    """repoproject"""

    def __init__(self, pkgpath: str, repo: Repository):
        """init"""
        self.repo = repo
        super().__init__(pkgpath)
        self._check_args()
        self.repoprojpath = path.join(repo.path, self.relpath, self.name)
        self.versionpath = path.join(self.repoprojpath, ".versions", self.version)

    def update(self, test=False):
        """update"""
        makedirs(self.repoprojpath, exist_ok=True)
        self._check_required()
        clean_all(path.join(self.path, "src", self.name), write=False)
        if test:
            pytest.main()  # Make sure this exits if there are errors!
        if not path.exists(self.repoprojpath):
            self.create(self.repoprojpath)
        self._remove_last_version()
        self._copy_and_backup()
        gen_docs(path.join(self.path, "src", self.name), release=self.version)
        repo_obj = Repo(self.repoprojpath)
        repo_obj.git.add(all=True)
        repo_obj.index.commit(self.version)

    def _check_args(self):
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
        for item in self.repo.required:
            if not path.exists(path.join(self.path, item)):
                raise FileNotFoundError(path.join(self.path, item))

    def _remove_last_version(self):
        """remove old files"""
        for item in self.repo.required:
            remove_item(path.join(self.repoprojpath, item))

    def _copy_and_backup(self):
        """copy backup"""
        mkdir(self.versionpath)
        for item in self.repo.required:
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
