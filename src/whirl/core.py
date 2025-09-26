import sys
import pathlib
import yaml


def parse_dag(dag_path: pathlib.Path) -> tuple[bool, list[pathlib.Path]]:
    with open(dag_path, "r") as file:
        raw_dag = yaml.load(file, Loader=yaml.Loader)

    # TODO: Validate that DAG is actually acyclic and create output config

    return (False, [])


def run(args: dict) -> None:
    file_path = pathlib.Path(args.file).absolute()

    if not file_path.exists():
        print("Invalid file path, try again")
        sys.exit(1)

    valid, run_config = parse_dag(file_path)

    if not valid:
        print("Invalid DAG, exiting...")
        sys.exit(1)


def generate() -> None:
    print("I am generating")
