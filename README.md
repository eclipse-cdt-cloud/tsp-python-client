# tsp-python-client

Client-side implementation, in Python, of the [Trace Server Protocol (TSP)][tsp].

It provides a module that can be included in Python scripts to query a trace server via the Trace Server Protocol (TSP).
The script **tsp_cli_client** provides a command-line interface for querying a trace server.

An example trace server implementation is provided by the [Eclipse Trace Compass Incubator][inc] project and can be downloaded [here][rcp].
It can be used to test this script and module.

This trace server bundles non-UI, core plug-ins of the [Eclipse Trace Compass][etc] project and comes with a server-side TSP implementation.

**👋 Want to help?** Read our [contributor guide][contributing].

## Status

- The **tsp_cli_client** script and the **tsp** module is under construction.
- This is an initial draft and only limited features have been currently implemented.
- **tsp** module only provides some limited number of TSP calls.
- The API will undergo revision till a stable version is reached.

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

**Note: Executing the tests will delete all traces and experiments from trace server workspace. Backup workspace before running the tests or start from fresh workspace.**

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

To activate completion for **tsp_cli_client** options, follow [these instructions][agc].

To use the **tsp_cli_client** script, type the following command in the root directory to get the usage:

```python
./tsp_cli_client -h

usage: tsp_cli_client [-h] [--ip IP] [--port PORT] 
                      [--open-trace TRACE_PATH]
                      [--name NAME] [--list-trace UUID] [--list-traces]
                      [--delete-trace UUID] [--open-experiment EXP_NAME]
                      [--list-experiment UUID] [--list-experiments]
                      [--delete-experiment UUID] [--list-outputs UUID]
                      [--list-output OUTPUT_ID] [--get-tree OUTPUT_ID]
                      [--get-virtual-table-columns OUTPUT_ID]
                      [--get-virtual-table-lines OUTPUT_ID] 
                      [--table-line-index INDEX] [--table-line-count COUNT]
                      [--table-times [TIMES ...]] [--table-column-ids [IDs ...]]
                      [--table-search-direction DIRECTION]
                      [--table-search-expression COLUMN_ID EXPRESSION]
                      [--get-timegraph-tree OUTPUT_ID] 
                      [--get-xy-tree OUTPUT_ID] [--get-xy OUTPUT_ID]
                      [--items [ITEMS ...]] [--time-range START END NUM_TIMES]
                      [--uuid UUID] [--uuids [UUIDS ...]] [--do-delete-traces]
                      [--paths [PATHS ...]]
                      [--list-configuration-sources] 
                      [--list-configuration-source TYPE_ID] 
                      [--list-configurations TYPE_ID]
                      [--list-configuration CONFIG_ID] 
                      [--load-configuration] 
                      [--update-configuration] 
                      [--delete-configuration CONFIGURATION_ID]
                      [--type-id TYPE_ID] 
                      [--config-id CONFIG_ID] 
                      [--params PARAMS]
                      [--get-health]
                      [--get-identifier]

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
  --get-tree OUTPUT_ID  Get the tree of an output of type DATA_TREE
  --get-virtual-table-columns OUTPUT_ID
                        Get the columns of an output of type DATA_TREE
  --get-virtual-table-lines OUTPUT_ID
                        Get the tree lines of an output of type DATA_TREE
  --table-line-index TABLE_LINE_INDEX
                        The index of the table line to start fetching
  --table-line-count TABLE_LINE_COUNT
                        The number of table lines to fetch
  --table-times [TABLE_TIMES ...]
                        The list of times to fetch from table
  --table-column-ids [TABLE_COLUMN_IDS ...]
                        The list of column ids to fetch
  --table-search-direction TABLE_LINE_SEARCH_DIRECTION
                        The direction to search for the table lines
  --table-search-expression COLUMN_ID EXPRESSION
                        The columns expression to search for the table lines
  --get-timegraph-tree OUTPUT_ID
                        Get the tree of an output of type TIME_GRAPH
  --get-xy-tree OUTPUT_ID
                        Get the tree of an output of type TREE_TIME_XY
  --get-xy OUTPUT_ID    Get the XY data of an output
  --items [ITEMS ...]   The list of XY items requested
  --time-range START END NUM_TIMES
                        The time range requested
  --uuid UUID           The UUID of a trace
  --uuids [UUIDS ...]   The list of UUIDs
  --do-delete-traces    Also delete traces when deleting experiment
  --paths [PATHS ...]   List of trace paths to be part of an experiment
  --list-configuration-sources
                        Get the available configuration sources
  --list-configuration-source TYPE_ID
                        Get a available configuration source
  --list-configurations TYPE_ID
                        Get the configurations loaded for given type
  --list-configuration CONFIG_ID
                        Get a configuration loaded for given type and config id
  --load-configuration  Load an configuration using paramemeters provided by --params
  --update-configuration
                        Update an configuration using paramemeters provided by --params
  --delete-configuration CONFIGURATION_ID
                        Delete a configuration
  --type-id TYPE_ID     id of configuration source type
  --config-id CONFIG_ID
                        id of configuration
  --params PARAMS       comma separated key value pairs (key1=val1,key2=val2)
  --get-health          Get the health status of the server
  --get-identifier      Identify important information regarding the server and the system
```

Examples:
```python
  '''Open trace ''' 
  ./tsp_cli_client --open-trace TRACE_PATH [--name NAME]
  ./tsp_cli_client --list-traces
  ./tsp_cli_client --list-trace UUID
  ./tsp_cli_client --list-trace UUID
  ./tsp_cli_client --delete-trace UUID
  ./tsp_cli_client --open-experiment EXP_NAME --uuids UUIDS 
  ./tsp_cli_client --open-experiment EXP_NAME --paths PATHS
  ./tsp_cli_client --list-experiments
  ./tsp_cli_client --list-experiment UUID
  ./tsp_cli_client --delete-experiment UUID [--do-delete-traces]
  ./tsp_cli_client --list-outputs UUID
  ./tsp_cli_client --get-tree OUTPUT_ID --uuid UUID
  ./tsp_cli_client --get-virtual-table-columns OUTPUT_ID --uuid UUID
  ./tsp_cli_client --get-virtual-table-lines --table-line-index INDEX --table-line-count COUNT --table-column-ids IDs --table-search-direction DIRECTION --table-search-expression COLUMN_ID EXPRESSION
  ./tsp_cli_client --get-timegraph-tree OUTPUT_ID --uuid UUID
  ./tsp_cli_client --get-xy-tree OUTPUT_ID --uuid UUID
  ./tsp_cli_client --get-xy OUTPUT_ID --uuid UUID --items ITEMS --time-range START END NUM_TIMES
  ./tsp_cli_client --list-configuration-sources
  ./tsp_cli_client --list-configuration-source TYPE_ID
  ./tsp_cli_client --list-configurations TYPE_ID
  ./tsp_cli_client --list-configuration CONFIG_ID --type-id TYPE_ID
  ./tsp_cli_client --load-configuration --type-id TYPE_ID --params key1:value1
  ./tsp_cli_client --update-configuration --type-id TYPE_ID --config-id CONFIG_ID --params key1=value1,key2=value2
  ./tsp_cli_client --delete-configuration CONFIGURATION_ID --type-id TYPE_ID
  ./tsp_cli_client --get-health
  ./tsp_cli_client --get-identifier
```

[agc]: https://kislyuk.github.io/argcomplete/#activating-global-completion
[contributing]: CONTRIBUTING.md
[etc]: https://www.eclipse.org/tracecompass/
[inc]: https://projects.eclipse.org/projects/tools.tracecompass.incubator
[rcp]: https://download.eclipse.org/tracecompass.incubator/trace-server/rcp/
[tsp]: https://github.com/eclipse-cdt-cloud/trace-server-protocol
