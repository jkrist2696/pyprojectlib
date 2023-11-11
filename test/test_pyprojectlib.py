#!/data/vddv04/nbak/grp042/ASPEN_MDO_Working/Anaconda_Envs/spyder/bin/python3
"""
Written by Jason Krist
jason.krist@gm.com
"""

from os import path
import sys
from shutil import rmtree

testdir = path.dirname(path.abspath(__file__))
appendpath = path.join(testdir, "../src")
sys.path.insert(0, appendpath)
import setup_pyproject as sp  # type: ignore # pylint: disable=E0401,C0413


def test_setup_pyproject():
    """function for testing setup_pyproject"""
    dirpath = path.join(testdir, "../")
    repopath = path.join(testdir, "../../testrepo")
    version = "0.0.1"
    print("\n")
    if path.exists(repopath):
        rmtree(repopath)
    sp.init_repo(repopath)
    sp.get_userdata(repopath, name="Jason Krist", email="jason.krist@gm.com")
    sp.setup_project(dirpath, repopath, version=version, test=False, env="generic")
    print("\n")
    if path.exists(repopath):
        rmtree(repopath)
    sp.init_repo(repopath)
    sp.get_userdata(repopath)
    sp.setup_project(dirpath, repopath, version=version, test=False)
    print("\n")
    sp.get_userdata(repopath)
    sp.setup_project(dirpath, repopath, test=False)


if __name__ == "__main__":
    test_setup_pyproject()
