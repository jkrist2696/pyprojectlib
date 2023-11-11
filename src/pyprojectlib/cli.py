"""
Written by Jason Krist
"""

from argparse import ArgumentParser

# TODO: FINISH CMD LINE (THIS SCRIPT)
# TODO: make distinct commands for init project vs. repo
# TODO: make entry-point "myrepo"
# TODO: ADD IDEA TO HAVE ALLOWED EDITORS IN THE CONFIG FILE
# Should I allow a name input instead of dirname?


def _cli_checks(parser, args: dict):
    """Check that command line args are compatible

    Parameters
    ----------
    parser: ArgumentParser object
    args : dict
    """
    if len(args["file"]) > 0 and len(args["dir"]) > 0:
        parser.error("File and Directory were both specified. Only specify one.")
    if len(args["file"]) == 0 and len(args["dir"]) == 0:
        parser.error("Neither File or Directory were specified. Please specify one.")
    if len(args["file"]) > 0 and args["noclean"]:
        parser.error("File was specified with -noclean so nothing occured.")
    if args["noclean"] and args["nodoc"]:
        parser.error("-noclean and -nodoc options were specified so nothing occured")


def parse():
    """Run command line parsing"""
    desc = "Simple command-line tool for creating and adding to your local python repositories"
    cmdh = (
        'Command - ["init", "add"] init=initialize'
        + " new project, add=add completed project to repo"
    )
    dirh = "Directory where to execute command"
    pkgh = "Flag to package python project into a distributable module"
    installh = (
        "Flag to package project and install it into the current python environment"
    )
    nch = "Flag to prevent cleaning of py files"
    ndh = "Flag to prevent html doc creation"
    reh = "Version number of python project (X.Y.Z)"
    nth = "Flag to prevent pytest from running"

    parser = ArgumentParser(prog="pyrepo", description=desc)
    parser.add_argument("command", type=str, help=cmdh)
    parser.add_argument("-version", "-v", default="", help=reh)
    parser.add_argument("-dir", "-d", default=".", help=dirh)
    parser.add_argument("-package", "-p", action="store_true", help=pkgh)
    parser.add_argument("-install", "-i", action="store_true", help=installh)
    parser.add_argument("-noclean", "-nc", action="store_true", help=nch)
    parser.add_argument("-nodoc", "-nd", action="store_true", help=ndh)
    parser.add_argument("-notest", "-nt", action="store_true", help=nth)

    args = vars(parser.parse_args())
    print(f"\nCommand Line Args:\n{args}\n")
    _cli_checks(parser, args)
    return [args[key] for key in args.keys()]
