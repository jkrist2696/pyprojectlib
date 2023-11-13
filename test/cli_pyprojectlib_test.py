"""
Written by Jason Krist
"""

from os import path
import sys

testdir = path.dirname(path.realpath(__file__))
appendpath = path.join(testdir, "../src")
sys.path.insert(0, appendpath)
from pyprojectlib import cli_main  # type: ignore # pylint: disable=E0401,C0413,E0611

if __name__ == "__main__":
    cli_main()
