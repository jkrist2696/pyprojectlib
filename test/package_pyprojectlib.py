"""
Written by Jason Krist
"""

from os import path
import sys
from cleandoc import cleandoc_all  # type: ignore # pylint: disable=E0401,C0413

testdir = path.dirname(path.realpath(__file__))
appendpath = path.join(testdir, "../src")
sys.path.insert(0, appendpath)

from pyprojectlib.pyuser import User  # type: ignore # pylint: disable=E0401,C0413
import pyprojectlib as ppl  # type: ignore # pylint: disable=E0401,C0413,E0611


def package(upload: bool):
    """function for packaging modules"""
    pkgpath = path.realpath(path.join(testdir, "../"))
    pkgname = path.basename(pkgpath)
    srcpath = path.join(pkgpath, "src", pkgname)
    # Get Release Number (plus 1) for Docs
    release, _found = ppl.pypi_version(pkgname, plus=True)
    # Run Cleandoc
    cleandoc_all(srcpath, release=release)
    # Package this project
    user = User(name="Jason Krist", email="jkrist2696@gmail.com", gituser="jkrist2696")
    ppl.Log.package_project(
        pkgpath,
        user,
        install=True,
        upload=upload,
        pyversion="3.6",
        filetypes="template",
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        UPLOAD = bool(sys.argv[1])
    else:
        UPLOAD = False
    print(f"\nUploading Package: {UPLOAD}")
    package(UPLOAD)
