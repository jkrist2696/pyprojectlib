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
import setup_pyproject as setpy  # pylint: disable=E0401,C0413

# TODO: (HIGH) Complete the CLI
# TODO: (HIGH) complete the packaging automation and add to test
# TODO: (HIGH) Checkin with Brian and get feedback
# TODO: (HIGH) in cleandoc, fix issue with README format of top title area
# TODO: (MED) add user permissions in .projects file (list of usernames who can edit)
# TODO: (LOW) allow creation of sub-environments (i.e. "generic">"aero")
# TODO: (LOW) make all printouts logs instead

# Packaging? Allow pip install but users could just append path instead (clarity)


def test_setup_pyproject():
    """function for testing setup_pyproject"""
    dirpath = path.join(testdir, "../")
    repopath = path.join(testdir, "../../testrepo")
    version = "0.0.1"
    print("\n")
    if path.exists(repopath):
        rmtree(repopath)
    setpy.init_repo(repopath)
    setpy.get_userdata(repopath, name="Jason Krist", email="jason.krist@gm.com")
    setpy.setup_project(dirpath, repopath, version=version, test=False, env="generic")
    print("\n")
    if path.exists(repopath):
        rmtree(repopath)
    setpy.init_repo(repopath)
    setpy.get_userdata(repopath)
    setpy.setup_project(dirpath, repopath, version=version, test=False)
    print("\n")
    setpy.get_userdata(repopath)
    setpy.setup_project(dirpath, repopath, test=False)


if __name__ == "__main__":
    test_setup_pyproject()
