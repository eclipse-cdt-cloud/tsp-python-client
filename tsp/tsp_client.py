# The MIT License (MIT)
#
# Copyright (C) 2020, 2023 - Ericsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""TspClient class file."""

import json
import requests

from tsp.trace import Trace
from tsp.trace_set import TraceSet
from tsp.tsp_client_response import TspClientResponse
from tsp.output_descriptor_set import OutputDescriptorSet
from tsp.response import GenericResponse, ModelType
from tsp.configuration_source_set import ConfigurationSourceSet
from tsp.configuration_source import ConfigurationSource
from tsp.configuration import Configuration
from tsp.configuration_set import ConfigurationSet
from tsp.experiment_set import ExperimentSet
from tsp.experiment import Experiment
from tsp.output_descriptor import OutputDescriptor
from tsp.health import Health

APPLICATION_JSON = 'application/json'

headers = {'content-type': APPLICATION_JSON, 'Accept': APPLICATION_JSON}
headers_form = {'content-type': 'application/x-www-form-urlencoded',
                'Accept': APPLICATION_JSON}

GET_TREE_FAILED = "failed to get tree: {0}"

# pylint: disable=consider-using-f-string,missing-timeout


class TspClient:
    '''
    Trace Server Protocol tsp_cli_client
    '''

    PARAMETERS_KEY = 'parameters'
    REQUESTED_TIME_KEY = 'requested_times'
    REQUESTED_ITEM_KEY = 'requested_items'

    REQUESTED_TIME_RANGE_KEY = 'requested_timerange'
    REQUESTED_TIME_RANGE_START_KEY = 'start'
    REQUESTED_TIME_RANGE_END_KEY = 'end'
    REQUESTED_TIME_RANGE_NUM_TIMES_KEY = 'nbTimes'

    REQUESTED_TABLE_LINE_INDEX_KEY = 'requested_table_index'
    REQUESTED_TABLE_LINE_COUNT_KEY = 'requested_table_count'
    REQUESTED_TABLE_LINE_COLUMN_IDS_KEY = 'requested_table_column_ids'
    REQUESTED_TABLE_LINE_SEACH_DIRECTION_KEY = 'table_search_direction'
    REQUESTED_TABLE_LINE_SEARCH_EXPRESSION_KEY = 'table_search_expressions'

    def __init__(self, base_url):
        '''
        Constructor
        '''
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'

    def fetch_traces(self):
        '''
        Fetch all available traces on the server
        :return: :class:`TspClientResponse <TraceSet>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}traces'.format(self.base_url)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(TraceSet(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("get traces failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_trace(self, uuid):
        '''
        Fetch a specific trace information
        :param uuid: Trace UUID to fetch
        :return: :class:`TspClientResponse <Trace>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}traces/{1}'.format(self.base_url, uuid)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:
            print("get trace failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def open_trace(self, name, path):
        '''
        Open a trace on the server
        parameters: Query object
        :return: :class:`TspClientResponse <Trace>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}traces'.format(self.base_url)

        my_parameters = {'name': name, 'uri': path}
        parameters = {'parameters': my_parameters}

        response = requests.post(api_url, json=parameters, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("post trace failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def delete_trace(self, uuid, delete_trace, remove_cache=False):
        '''
        Delete a trace on the server
        :param uuid: Trace UUID to delete
        :param delete_trace: Also delete the trace from disk
        :param remove_cache: Remove all cache for this trace
        :return: :class:`TspClientResponse <Trace>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}traces/{1}'.format(self.base_url, uuid)
        parameters = {}
        if delete_trace:  # pragma: no cover
            parameters['deleteTrace'] = "true"

        if remove_cache:
            parameters['removeCache'] = "true"

        response = requests.delete(api_url, json=parameters, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("delete trace failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_experiments(self):
        '''
        Fetch all available experiments on the server
        :return: :class:`TspClientResponse <ExperimentSet>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments'.format(self.base_url)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(ExperimentSet(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("get experiments failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_experiment(self, uuid):
        '''
        Fetch a specific experiment information
        :param uuid: Trace UUID to fetch
        :return: :class:`TspClientResponse <Experiment>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}'.format(self.base_url, uuid)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Experiment(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:
            print("get trace failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def delete_experiment(self, uuid):
        '''
        Delete a specific experiment
        :param uuid: Trace UUID to fetch
        :return: :class:`TspClientResponse <Trace>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}'.format(self.base_url, uuid)
        response = requests.delete(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Experiment(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("delete experiment failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def open_experiment(self, name, traces):
        '''
        Create an experiment on the server
        :param parameters: Query object
        :rtype: The created experiment
        '''
        api_url = '{0}experiments'.format(self.base_url)

        my_parameters = {'name': name, 'traces': traces}
        parameters = {'parameters': my_parameters}

        response = requests.post(api_url, json=parameters, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(Experiment(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("post experiment failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_experiment_outputs(self, exp_uuid):
        '''
        List all the outputs associated to this experiment
        :param exp_uuid: Experiment UUID
        :return: :class:  `TspClientResponse <OutputDescriptorSet>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs'.format(self.base_url, exp_uuid)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(OutputDescriptorSet(json.loads(
                response.content.decode('utf-8'))),
                response.status_code, response.text)
        else:  # pragma: no cover
            print("get output descriptors failed: {0}".format(
                response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_experiment_output(self, exp_uuid, output_id):
        '''
        Fetch given output descriptor
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :param parameters: Query object
        :returns: :class:  `TspClientResponse <OutputDescriptor>` object OutputDescriptor
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/{2}'.format(
            self.base_url, exp_uuid, output_id)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(OutputDescriptor(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print(GET_TREE_FAILED.format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_datatree(self, exp_uuid, output_id, parameters=None):
        '''
        Fetch Time Graph tree, Model extends TimeGraphEntry
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :param parameters: Query object
        :returns: :class:  `TspClientResponse <GenericResponse>` object Timegraph entries response
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/data/{2}/tree'.format(
            self.base_url, exp_uuid, output_id)

        params = parameters
        if parameters is None:
            params = {}

        response = requests.post(api_url, json=params, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')),
                                                     ModelType.DATA_TREE),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print(GET_TREE_FAILED.format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_virtual_table_columns(self, exp_uuid, output_id):
        '''
        Fetch Virtual Table columns, Model extends VirtualTableModel
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :returns: :class:  `TspClientResponse <GenericResponse>` object Virtual Table columns response
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/table/{2}/columns'.format(
            self.base_url, exp_uuid, output_id)

        response = requests.post(api_url, json={}, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')),
                                                     ModelType.VIRTUAL_TABLE_HEADER),
                                     response.status_code, response.text)
        else:
            print(GET_TREE_FAILED.format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_virtual_table_lines(self, exp_uuid, output_id, parameters=None):
        '''
        Fetch Virtual Table lines, Model extends VirtualTableModel
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :param parameters: Query object
        :returns: :class:  `TspClientResponse <GenericResponse>` object Virtual Table lines response
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/table/{2}/lines'.format(
            self.base_url, exp_uuid, output_id)

        params = parameters
        if parameters is None:
            params = {
                TspClient.PARAMETERS_KEY: {}
            }

        response = requests.post(api_url, json=params, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')),
                                                     ModelType.VIRTUAL_TABLE),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print(GET_TREE_FAILED.format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_timegraph_tree(self, exp_uuid, output_id, parameters=None):
        '''
        Fetch Time Graph tree, Model extends TimeGraphEntry
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :param parameters: Query object
        :returns: :class:  `TspClientResponse <GenericResponse>` object Timegraph entries response
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/timeGraph/{2}/tree'.format(
            self.base_url, exp_uuid, output_id)

        params = parameters
        if parameters is None:
            params = {}

        response = requests.post(api_url, json=params, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')),
                                                     ModelType.TIME_GRAPH_TREE),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print(GET_TREE_FAILED.format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_xy_tree(self, exp_uuid, output_id, parameters=None):
        '''
        Fetch XY tree, Model extends Entry
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :param parameters: Query object
        :returns: :class:  `TspClientResponse <GenericResponse>` object XY entries response
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/XY/{2}/tree'.format(
            self.base_url, exp_uuid, output_id)

        params = parameters
        if parameters is None:
            params = {}

        response = requests.post(api_url, json=params, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')),
                                                     ModelType.XY_TREE),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print(GET_TREE_FAILED.format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_xy(self, exp_uuid, output_id, parameters):
        '''
        Fetch XY xy, XYModel
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :param parameters: Query object (mandatory here; no defaults possible)
        :returns: :class:  `TspClientResponse <GenericResponse>` object XY series response
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/XY/{2}/xy'.format(
            self.base_url, exp_uuid, output_id)

        response = requests.post(api_url, json=parameters, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')),
                                                     ModelType.XY),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("failed to get xy: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_configuration_sources(self):
        '''
        Fetch Extensions (loaded files)
        '''
        api_url = '{0}config/types/'.format(self.base_url)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(ConfigurationSourceSet(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("failed to get configuration sources: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_configuration_source(self, type_id):
        '''
        Fetch Extensions (loaded files)
        '''
        api_url = '{0}config/types/{1}'.format(self.base_url, type_id)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(ConfigurationSource(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("failed to get a configuration source: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_configurations(self, type_id):
        '''
        Fetch configurations (loaded files)
        e.g. org.eclipse.tracecompass.tmf.core.config.xmlsourcetype
        '''
        api_url = '{0}config/types/{1}/configs'.format(self.base_url, type_id)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(ConfigurationSet(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("failed to get configurations: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_configuration(self, type_id, config_id):
        '''
        Fetch a configuration (loaded file)
        e.g. org.eclipse.tracecompass.tmf.core.config.xmlsourcetype
        '''
        api_url = '{0}config/types/{1}/configs/{2}'.format(self.base_url, type_id, config_id)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(Configuration(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("failed to get configuration: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def post_configuration(self, type_id, params):
        '''
        Load an extension
        '''
        api_url = '{0}config/types/{1}/configs'.format(self.base_url, type_id)

        parameters = {'parameters': params}

        response = requests.post(api_url, json=parameters, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(Configuration(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("post extension failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def put_configuration(self, type_id, config_id, params):
        '''
        Load an extension
        '''
        api_url = '{0}config/types/{1}/configs/{2}'.format(self.base_url, type_id, config_id)

        parameters = {'parameters': params}

        response = requests.put(api_url, json=parameters, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(Configuration(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("put extension failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def delete_configuration(self, type_id, config_id):
        '''
        Delete an extension
        '''
        api_url = '{0}config/types/{1}/configs/{2}'.format(self.base_url, type_id, config_id)

        response = requests.delete(api_url, headers=headers_form)

        if response.status_code == 200:
            return TspClientResponse(Configuration(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("post extension failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_health(self):
        '''
        Fetch the health status of the server
        :return: :class:`TspClientResponse <Health>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}health'.format(self.base_url)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Health(json.loads(response.content.decode('utf-8'))),
                                     response.status_code, response.text)
        else:  # pragma: no cover
            print("get health failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)
