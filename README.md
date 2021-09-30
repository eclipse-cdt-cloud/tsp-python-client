# tsp-python-client

Client-side implementation, in Python, of the [Trace Server Protocol (TSP)][tsp].

It provides a module that can be included in Python scripts to query a trace server via the Trace Server Protocol (TSP). The script **tsp-cli-client** provides a command-line interface for querying a trace server.

An example trace server implementation is provided by the [Eclipse Trace Compass Incubator][inc] project and can be downloaded [here][rcp]. It can be used to test this script and module.

This trace server bundles non-UI, core plug-ins of the [Eclipse Trace Compass][etc] project and comes with a server-side TSP implementation.

## Status

The **tsp-cli-client** script and the **tsp** module is under construction. This is an initial draft and only limited features have been currently implemented. **tsp** module only provides some limited number of TSP calls. The API will undergo revision till a stable version is reached.

## Setup

To initialize a local virtual environment, type the following commands in the root directory:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The virtual environment can be replaced with another local setup.

## Tests

To run currently available integration tests, launch a server and type the following command in the root directory:

```shell
git submodule update --init
.venv/bin/pytest
```

Above, the pytest command can be replaced with another local installation.

Add this to that command to also get **tsp** module code test coverage, here listing uncovered line numbers only:

```shell
pytest --cov tsp --cov-report term-missing:skip-covered
```

## Usage

To activate completion for **tsp-cli-client** options, follow [these instructions][agc].

To use the **tsp-cli-client** script, type the following command in the root directory to get the usage:

```python
./tsp-cli-client -h

usage: tsp-cli-client [-h] [--ip IP] [--port PORT] [--open-trace TRACE_PATH]
                      [--name NAME] [--list-trace UUID] [--list-traces]
                      [--delete-trace UUID] [--open-experiment EXP_NAME]
                      [--list-experiment UUID] [--list-experiments]
                      [--delete-experiment UUID] [--list-outputs UUID]
                      [--list-output OUTPUT_ID] [--get-tree OUTPUT_ID]
                      [--get-xy-tree OUTPUT_ID] [--get-xy OUTPUT_ID]
                      [--items [ITEMS ...]] [--times [TIMES ...]]
                      [--uuid UUID] [--uuids [UUIDS ...]] [--do-delete-traces]
                      [--paths [PATHS ...]] [--list-extensions]
                      [--load-extension EXTENSION_PATH]
                      [--delete-extension EXTENSION_NAME]

CLI client to send Trace Server Protocol commands to a Trace Server.

optional arguments:
  -h, --help            show this help message and exit
  --ip IP               IP address of trace server
  --port PORT           port of trace server
  --open-trace TRACE_PATH
                        Path to trace to open
  --name NAME           trace name
  --list-trace UUID     Get details on the given trace
  --list-traces         List all open traces on the server
  --delete-trace UUID   Delete a trace on the server
  --open-experiment EXP_NAME
                        Open experiment on the server
  --list-experiment UUID
                        Get details on the given experiment
  --list-experiments    List all open experiments on the server
  --delete-experiment UUID
                        Delete an experiment on the server
  --list-outputs UUID   Get details on the given trace
  --list-output OUTPUT_ID
                        Get details on the given output of a trace
  --get-tree OUTPUT_ID  Get the timegraph tree of an output
  --get-xy-tree OUTPUT_ID
                        Get the XY tree of an output
  --get-xy OUTPUT_ID    Get the XY data of an output
  --items [ITEMS ...]   The list of XY items requested
  --times [TIMES ...]   The list of XY times requested
  --uuid UUID           The UUID of a trace
  --uuids [UUIDS ...]   The list of UUIDs
  --do-delete-traces    Also delete traces when deleting experiment
  --paths [PATHS ...]   List of trace paths to be part of an experiment
  --list-extensions     Get the extensions loaded
  --load-extension EXTENSION_PATH
                        Load an extension
  --delete-extension EXTENSION_NAME
                        Delete an extension
```

[agc]: https://kislyuk.github.io/argcomplete/#activating-global-completion
[etc]: https://www.eclipse.org/tracecompass/
[inc]: https://projects.eclipse.org/projects/tools.tracecompass.incubator
[rcp]: https://download.eclipse.org/tracecompass.incubator/trace-server/rcp/
[tsp]: https://github.com/theia-ide/trace-server-protocol
