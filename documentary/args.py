import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("root",
                        nargs='?',
                        help="path to a root folder of a project (must contain 'documentary' folder and templates)",
                        default=os.getcwd(),
                        metavar="FILE")

    parser.add_argument("--template",
                        help="a subset of templates which will have its documentation generated",
                        metavar="FILE")

    return parser.parse_args()
