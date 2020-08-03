# tsp-typescript-client
Client-side implementation, in Python, of the [Trace Server Protocol (TSP)](https://github.com/theia-ide/trace-server-protocol).

It provides a module that can be included in Python scripts to query a trace server via the Trace Server Protocol (TSP). The script **tsp-cli-client** provides a command-line interface for querying a trace server. 

An example trace server implementation is provided by the [Eclipse Trace Compass Incubator](https://projects.eclipse.org/projects/tools.tracecompass.incubator) project and can be downloaded [here](https://download.eclipse.org/tracecompass.incubator/trace-server/rcp/). It can be used to test this script and module.

This trace server bundles non-UI, core plug-ins of the [Eclipse Trace Compass](https://www.eclipse.org/tracecompass/) project and comes with a server-side TSP implementation.

# Status
The **tsp-cli-client** script and the **tsp** module is under construction. This is an initial draft and only limited features have been currently implemented. **tsp** module only provides some limited number of TSP calls. The API will undergo revision till a stable version is reached. 

# Usage

To use the **tsp-cli-client** script, type the following command in the root directory to get the usage:

```python
./tsp-cli-client -h

usage: tsp-cli-client [-h] [--ip IP] [--port PORT] [--open-trace TRACE_PATH]
                      [--name NAME] [--list-trace UUID] [--list-traces]
                      [--open-experiment EXP_NAME] [--list-experiment UUID]
                      [--list-experiments] [--delete-experiment UUID]
                      [--list-outputs UUID] [--list-output OUTPUT_ID]
                      [--get-tree OUTPUT_ID] [--uuid UUID]
                      [--uuids [UUIDS [UUIDS ...]]] [--list-extensions]
                      [--load-extension EXTENSION_PATH]
                      [--delete-extension EXTENSION_NAME]

CLI client to sent Trace Server Protocol commands to a Trace Server.

optional arguments:
  -h, --help            show this help message and exit
  --ip IP               IP address of trace server
  --port PORT           port of trace server
  --open-trace TRACE_PATH
                        Path to trace to open
  --name NAME           trace name
  --list-trace UUID     Get details on the given trace
  --list-traces         List all open traces on the server
  --open-experiment EXP_NAME
                        Open experiment on the server
  --list-experiment UUID
                        Get details on the given experiment
  --list-experiments    List all open experiments on the server
  --delete-experiment UUID
                        Delete an experiment on the server
  --list-outputs UUID   Gets details on the given trace
  --list-output OUTPUT_ID
                        Gets details on the given output of a trace
  --get-tree OUTPUT_ID  Gets the tree of an output
  --uuid UUID           The UUID of a trace
  --uuids [UUIDS [UUIDS ...]]
                        The list of UUIDs
  --list-extensions     Get the extensions loaded
  --load-extension EXTENSION_PATH
                        Load an extension
  --delete-extension EXTENSION_NAME
                        Delete an extension


```
