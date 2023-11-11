"""
Written by Jason Krist
"""

from os import path
import sys
from shutil import rmtree

testdir = path.dirname(path.realpath(__file__))
appendpath = path.join(testdir, "../src")
sys.path.insert(0, appendpath)

from pyprojectlib.pyuser import User  # type: ignore # pylint: disable=E0401,C0413
from pyprojectlib.pyproject import init_project_dir  # type: ignore # pylint: disable=E0401,C0413
from pyprojectlib.pypackage import package_project  # type: ignore # pylint: disable=E0401,C0413
from pyprojectlib.pyrepo import Repository, init_repo_dir  # type: ignore # pylint: disable=E0401,C0413


def test_setup_pyproject():
    """function for testing setup_pyproject"""
    # create new project dir
    initpath = path.join(testdir, "initpkgtest")
    if path.exists(initpath):
        rmtree(initpath)
    init_project_dir(initpath)
    rmtree(initpath)
    # Create new repo and push this package
    pkgpath = path.join(testdir, "../")
    repopath1 = path.join(testdir, "../../testrepo1")
    repopath2 = path.join(testdir, "../../testrepo2")
    version = "0.0.1"
    print("\n")
    if path.exists(repopath1):
        rmtree(repopath1)
    if path.exists(repopath2):
        rmtree(repopath2)
    init_repo_dir(repopath1)
    user = User(name="Jason Krist", email="jkrist2696@gmail.com", gituser="jkrist2696")
    repo = Repository(repopath1, user)
    repo.push(pkgpath, version=version, test=False, relpath="python/generic")
    print("\n")
    # relpath should be recognized based on project name
    init_repo_dir(repopath2)
    repo = Repository(repopath2, user)
    repo.push(pkgpath, version=version, test=False, relpath=".")
    print("\n")
    # push again to act as new version
    repo.push(pkgpath, test=False)
    # package current code
    package_project(pkgpath, user)


if __name__ == "__main__":
    test_setup_pyproject()
