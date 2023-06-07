import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="This tool is used to analyze software metrics of any git repo. Currently supports only python"
    )
    parser.add_argument("repository_link", help="Remote Git repository URL")
    parser.add_argument("-d", "--directories", default=["src"], nargs="+", help="Repository directories to analyze")
    parser.add_argument("-e", "--extensions", default=[".py"], nargs="+", choices=[".py"], help="File extensions to analyze")
    return parser.parse_args()
