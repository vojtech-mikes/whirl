import sys
import pathlib
import yaml
import networkx as nx
import nbclient as nc
import nbformat as nf
from nbclient.exceptions import CellExecutionError


def _parse_dag(dag_path: pathlib.Path) -> list[pathlib.Path]:
    with open(dag_path, "r") as file:
        raw_dag = yaml.load(file, Loader=yaml.Loader)

    tasks = raw_dag["tasks"]

    G = nx.DiGraph()

    task_all = all(["task" in x for x in tasks])

    file_all = all(["file" in x for x in tasks])

    if not task_all or not file_all:
        print("DAG definition is invalid. All tasks must have task and file")
        sys.exit(1)

    G.add_nodes_from([x["task"] for x in tasks])

    for t in tasks:
        if "after" in t:
            from_t = t["after"]
            to_t = t["task"]

            if isinstance(from_t, list):
                for t in from_t:
                    G.add_edge(from_t, to_t)
            else:
                G.add_edge(from_t, to_t)

    acyclic = nx.is_directed_acyclic_graph(G)

    tournament = nx.is_tournament(G)

    if not acyclic and not tournament:
        print("DAG error. Cycle found.")
        sys.exit(1)

    hamiltonian_path = nx.tournament.hamiltonian_path(G)

    lookup = {x["task"]: x["file"] for x in tasks}

    run_order = [pathlib.Path(lookup[x]).absolute() for x in hamiltonian_path]

    return run_order


def run(args: dict) -> None:
    command = args.command
    file_path = pathlib.Path(args.file).absolute()

    if not file_path.exists():
        print("Invalid file path, try again")
        sys.exit(1)

    run_config = _parse_dag(file_path)

    if command == "plan":
        print("Whirl will execute the notebooks in following order")
        print("Order is based on Hamiltonian path in directed acyclic graph\n")
        for idx, f in enumerate(run_config):
            if not f.exists():
                e_message = "ERROR: File on given path does not exist."
                print(f"{idx+1} : {f} - {e_message}")
            else:
                print(f"{idx+1} : {f} - File OK")
    else:

        print("Running notebooks...")
        for f in run_config:
            if not f.exists():
                print(f"Skipping notebook {f.name} because file does not exists")
            else:

                nb = nf.read(f, as_version=4)
                client = nc.NotebookClient(
                    nb,
                    timeout=600 if not args.timeout else args.timeout,
                    resources={"metadata": {"path": "/tmp/"}},
                )
                print("Creating ipykernel for notebook execution...")
                client.setup_kernel()
                print(f"Executing notebook: {f.name}")
                try:
                    client.execute()
                except CellExecutionError:
                    msg = f"Error executing the notebook {f.name}.\n"
                    print(msg)
                    raise

        print("All done.")


def generate(args: dict) -> None:
    print("I am generating")
    # TBI
