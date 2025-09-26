import argparse
from core import run, generate


class CliParser:

    parser: argparse.ArgumentParser

    def __init__(self):

        self.parser = argparse.ArgumentParser(
            prog="whirl",
            description="Whirl is simple orchestration tool that can work with ipynb files",
            epilog="If you find any issues report them to the github. Or create a PR :)",
        )

        subparsers = self.parser.add_subparsers(dest="command", required=True)

        parser_run = subparsers.add_parser("run", help="Run Whirl DAG")
        parser_run.add_argument(
            "--file", "-f", type=str, required=True, help="Path to the Whirl DAG file"
        )
        parser_run.set_defaults(func=run)

        parser_run = subparsers.add_parser(
            "plan", help="Plan Whirl DAG (this is like dry-run)"
        )
        parser_run.add_argument(
            "--file", "-f", type=str, required=True, help="Path to the Whirl DAG file"
        )
        parser_run.set_defaults(func=run)

        parser_run = subparsers.add_parser(
            "generate",
            help="Generate Whirl DAG if the notebooks follow numbering convetion",
        )
        parser_run.add_argument(
            "--file", "-f", type=str, required=True, help="Path to the Whirl DAG file"
        )
        parser_run.set_defaults(func=generate)
