"""
Written by Jason Krist
"""

from os import path
import sys
from shutil import rmtree, copytree

testdir = path.dirname(path.realpath(__file__))
appendpath = path.join(testdir, "../src")
sys.path.insert(0, appendpath)

from pyprojectlib.pyuser import User  # type: ignore # pylint: disable=E0401,C0413
from pyprojectlib.pyrepo import Repository  # type: ignore # pylint: disable=E0401,C0413
import pyprojectlib as ppl  # type: ignore # pylint: disable=E0401,C0413,E0611


def test_setup_pyproject():
    """function for testing setup_pyproject"""

    version = "0.0.1"
    test = False
    git = True
    clean = True
    doc = True
    pkgpath = path.join(testdir, "../")
    initpath = path.join(testdir, "../../testproj1")
    initpathcopy = path.join(testdir, "examples", "testproj1")
    repopath1 = path.join(testdir, "../../testrepo1")
    repopathcopy1 = path.join(testdir, "./examples/testrepo1")
    repopath2 = path.join(testdir, "../../testrepo2")
    repopathcopy2 = path.join(testdir, "./examples/testrepo2")

    # Delete old tests
    deletelist = [
        initpath,
        initpathcopy,
        repopath1,
        repopathcopy1,
        repopath2,
        repopathcopy2,
    ]
    for dirpath in deletelist:
        if path.exists(dirpath):
            rmtree(dirpath)

    print("")
    # Create new project
    ppl.init_project(initpath)

    # Create a user object
    userargs = {
        "name": "Jason Krist",
        "email": "jkrist2696@gmail.com",
        "gituser": "jkrist2696",
    }
    user = User(**userargs)

    print("")
    # Create new repo and push this package
    ppl.init_repo(repopath1, **userargs)
    repo = Repository(repopath1, user)
    repo.push(
        pkgpath,
        version=version,
        test=test,
        relpath="python/generic",
        git=git,
        clean=clean,
        doc=doc,
    )

    print("")
    # Create a second repo and push this package
    ppl.init_repo(repopath2, **userargs)
    repo = Repository(repopath2, user)
    repo.push(
        pkgpath,
        version=version,
        test=test,
        relpath=".",
        git=git,
        clean=clean,
        doc=doc,
    )
    # push again to act as new version
    repo.push(pkgpath, test=test, git=git, clean=clean, doc=doc)

    # Move all to examples folder
    copytree(initpath, initpathcopy)
    rmtree(initpath)
    copytree(repopath1, repopathcopy1)
    rmtree(repopath1)
    copytree(repopath2, repopathcopy2)
    rmtree(repopath2)

    print("")
    # Package this project
    ppl.Log.package_project(pkgpath, user, install=True, upload=False)


if __name__ == "__main__":
    test_setup_pyproject()
