"""
Written by Jason Krist

# to do list:
# check if config has changed and re-save it???
# Add better options for outputting logfile or not
# remote git pushing
# pull packages from local repo
# ADD VALIDATION FOR EMAIL AND VERSION?
# (LOW) update my docstrings
# DO SOME TESTING: WSL linux, test editors list, project exists, etc.

"""

from os import path
from shutil import copyfile
from requests import get

from git import Repo

from . import cli
from . import constants as CONS  # type: ignore # pylint: disable=E0611,E0401
from .helper import attrs_to_dict, config_log, create_dirs
from .pypackage import Package  # type: ignore # pylint: disable=E0401,C0413,E0611
from .pyrepo import Repository  # type: ignore # pylint: disable=E0401,C0413,E0611
from .pyuser import User


def init_project(dirpath: str):
    """wrapper for _init_project_dir"""
    dirpath = path.realpath(dirpath)
    if path.exists(dirpath):
        errstr = f"\nNew Project cannot be created because directory already exists:\n{dirpath}\n\n"
        raise FileExistsError(errstr)
    dirdict = {
        CONS.SRC_DIR: {path.basename(dirpath): {}},
        CONS.DOCS_DIR: {},
        CONS.TEST_DIR: {"examples": {}},
        CONS.VERSIONS_DIR: {},
    }
    logstr = f"Creating Empty Project: {dirpath}"
    CONS.log().info(logstr)
    create_dirs(dirpath, dirdict)
    # Initialize git repo
    git_repo = Repo.init(dirpath)
    git_repo.close()
    # Create .gitignore file
    with open(path.join(dirpath, ".gitignore"), "w", encoding="utf-8") as writer:
        for item in CONS.IGNORELIST:
            writer.write(f"{item}\n")
    # Create empty requirements.txt
    with open(path.join(dirpath, CONS.REQFILE), "wb") as writer:
        writer.write(b"")
    # create example readme and license
    scriptpath = path.dirname(path.realpath(__file__))
    newreadme = path.join(dirpath, CONS.READFILE)
    basereadme = path.join(scriptpath, "README.template")
    copyfile(basereadme, newreadme)
    newlicense = path.join(dirpath, CONS.LICFILE)
    baselicense = path.join(scriptpath, "LICENSE.template")
    copyfile(baselicense, newlicense)


def init_repo(dirpath: str, **kwargs):
    """wrapper for _init_repo_dir"""
    dirpath = path.realpath(dirpath)
    if path.exists(dirpath):
        errstr = f"New Repo cannot be created because directory already exists:\n{dirpath}\n\n"
        raise FileExistsError(errstr)
    logstr = f"Creating Empty Repository: {dirpath}"
    CONS.log().info(logstr)
    dirdict: dict[str, dict] = {
        CONS.USERS_DIR: {},
        CONS.PROJECTS_DIR: {},
    }
    create_dirs(dirpath, dirdict)
    user = User(**kwargs)
    Repository(dirpath, user)


def init_user(repopath: str, **kwargs):
    """add a new user to the repo and save their config"""
    user = User(**kwargs)
    # maybe check if repo exists here?
    repo = Repository(repopath, user)
    logstr = f'Added user "{repo.user.user}" to Repo: {repopath}'
    CONS.log().info(logstr)


def push_to_repo(repopath: str, projpath: str, **kwargs):
    """push new project version to existing repo"""
    name = kwargs.pop("name", "")
    email = kwargs.pop("email", "")
    gituser = kwargs.pop("gituser", "")
    user = User(name=name, email=email, gituser=gituser)
    repo = Repository(repopath, user)
    version = kwargs.pop("version", "")
    test = kwargs.pop("test", True)
    relpath = kwargs.pop("relpath", "")
    repo.push(projpath, version=version, test=test, relpath=relpath)


def package_project(pkgpath: str, user: User, **kwargs):
    """wrapper for _package_project"""
    logger = config_log()
    logstr = f"package_project kwargs: {kwargs}"
    CONS.log().info(logstr)
    upload = kwargs.pop("upload", False)
    install = kwargs.pop("install", False)
    pyversion = kwargs.pop("pyversion", "")
    filetypes = kwargs.pop("filetypes", "")
    pkg = Package(path.realpath(pkgpath), user, **kwargs)
    pkg.save_toml(pyversion=pyversion, filetypes=filetypes)
    pkg.build(upload=upload, install=install)
    for handle in logger.handlers:
        handle.close()
    return pkg


def cli_main():
    """run main cli function"""
    logger = config_log(file=f"{CONS.NAME}_log.txt")  # , level=logging.INFO
    args, helpdict = cli.cli_parse()
    command = getattr(args, cli.CMDNAME)
    if command is None:
        print(helpdict[cli.CMDNAME])
    if command == cli.NEWNAME:
        new = getattr(args, cli.NEWNAME)
        if new is None:
            print(helpdict[cli.NEWNAME])
        if new == cli.REPONAME:
            userargs = attrs_to_dict(args, [cli.NAMENAME, cli.EMNAME, cli.GUNAME])
            init_repo(getattr(args, cli.REPOPATHNAME), **userargs)
        if new == cli.PROJNAME:
            init_project(getattr(args, cli.PROJPATHNAME))
        if new == cli.USERNAME:
            repopath = getattr(args, cli.REPOPATHNAME)
            userargs = attrs_to_dict(args, [cli.NAMENAME, cli.EMNAME, cli.GUNAME])
            init_user(repopath, **userargs)
    if command == cli.PUSHNAME:
        repopath = getattr(args, cli.REPOPATHNAME)
        projpath = getattr(args, cli.PROJPATHNAME)
        kwnames = [
            cli.RELNAME,
            cli.NCNAME,
            cli.NDNAME,
            cli.NTNAME,
            cli.VERNAME,
            cli.NAMENAME,
            cli.EMNAME,
            cli.GUNAME,
        ]
        kwargs = attrs_to_dict(args, kwnames)
        push_to_repo(repopath, projpath, **kwargs)
    if command == cli.PACKNAME:
        projpath = getattr(args, cli.PROJPATHNAME)
        userargs = attrs_to_dict(args, [cli.NAMENAME, cli.EMNAME, cli.GUNAME])
        user = User(**userargs)
        kwnames = [cli.VERNAME, cli.UPNAME, cli.INNAME, cli.PYVERNAME, cli.FILETNAME]
        kwargs = attrs_to_dict(args, kwnames)
        package_project(projpath, user, **kwargs)
    for handle in logger.handlers:
        handle.close()


def pypi_version(pkgname: str, plus: bool = False) -> tuple[str, bool]:
    """get the latest version number of package from pypi"""
    try:
        pkgpage = get(f"{CONS.PYPI}/{pkgname}/", timeout=10).text
    except ConnectionError as _error:
        pkgpage = "page not found"
    notfoundcheck1 = "page not found" in pkgpage.lower()
    notfoundcheck2 = "error code 404" in pkgpage.lower()
    notfoundcheck3 = "couldn't find this page" in pkgpage.lower()
    if not any([notfoundcheck1, notfoundcheck2, notfoundcheck3]):
        start_ind = pkgpage.find('<h1 class="package-header__name">') + 33
        latest_start = pkgpage[start_ind:]
        latest = latest_start[0 : latest_start.find("</h1>")]
        release = latest.strip().split(" ")[1]
    else:
        return "0.0.1", False
    if not plus:
        return release, True
    release_split = release.split(".")
    release_split[2] = str(int(release_split[2]) + 1)
    release = ".".join(release_split)
    return release, True


def add_log(func):
    """add loggin wrapper to function"""

    def log_wrapper(*args, **kwargs):
        """log wrapper function"""
        logger = config_log(file=f"{CONS.NAME}_log.txt")
        func(*args, **kwargs)
        for handle in logger.handlers:
            handle.close()

    return log_wrapper


class Log:  # pylint: disable=R0903
    """add logging to functions"""

    init_project = add_log(init_project)
    init_repo = add_log(init_repo)
    init_user = add_log(init_user)
    push_to_repo = add_log(push_to_repo)
    package_project = add_log(package_project)
