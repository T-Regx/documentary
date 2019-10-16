import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("template",
                        help="input file which will have its documentation generated",
                        metavar="FILE",
                        type=lambda x: __try_get_path(parser, x))
    return parser.parse_args()


def __try_get_path(p: argparse.ArgumentParser, file):
    if os.path.exists(file):
        return file
    p.error("The file '%s' does not exist!" % file)
