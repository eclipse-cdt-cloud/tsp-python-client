# The MIT License (MIT)
#
# Copyright (C) 2020 - Ericsson
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

from tsp.trace import Trace
import requests
from tsp.trace_set import TraceSet
import json
from tsp.tsp_client_response import TspClientResponse
from tsp.output_descriptor_set import OutputDescriptorSet
from tsp.response import GenericResponse, ModelType
from tsp.extension_set import ExtensionSet
from tsp.experiment_set import ExperimentSet
from tsp.experiment import Experiment
from tsp.output_descriptor import OutputDescriptor

headers = {'content-type': 'application/json', 'Accept': 'application/json'}
headers_form = {'content-type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'}

PARAMETERS_KEY = 'parameters'
REQUESTED_TIME_KEY = 'requested_times'


class TspClient(object):
    '''
    Trace Server Protocol tsp_cli_client
    '''

    def __init__(self, base_url):
        '''
        Constructor
        '''
        self.base_url = base_url

    def fetch_traces(self):
        '''
        Fetch all available traces on the server
        :return: :class:`TspClientResponse <TraceSet>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}traces'.format(self.base_url)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(TraceSet(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
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
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
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
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
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
        if delete_trace:
            parameters['deleteTrace'] = "true"

        if remove_cache:
            parameters['removeCache'] = "true"

        response = requests.delete(api_url, json=parameters, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
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
            return TspClientResponse(ExperimentSet(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
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
            return TspClientResponse(Experiment(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
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
            return TspClientResponse(Experiment(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
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
            return TspClientResponse(Experiment(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
            print("post experiment failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_experiment_outputs(self, exp_uuid):
        '''
        List all the outputs associated to this experiment
        :param exp_uuid: Experiment UUID
        :return: :class:  `TspClientResponse <OutputDescriptorSet>` object
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/'.format(self.base_url, exp_uuid)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(OutputDescriptorSet(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
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
            return TspClientResponse(OutputDescriptor(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
            print("failed to get tree: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_timegraph_tree(self, exp_uuid, output_id, parameters=None):
        '''
        Fetch Time Graph tree, Model extends TimeGraphEntry
        :param exp_uuid: Experiment UUID
        :param output_id: Output ID
        :param parameters: Query object
        :returns: :class:  `TspClientResponse <GenericResponse>` object Time graph entry response with entries and headers
        :rtype: TspClientResponse
        '''
        api_url = '{0}experiments/{1}/outputs/timeGraph/{2}/tree'.format(
            self.base_url, exp_uuid, output_id)

        params = parameters
        if (parameters is None):
            requested_times = [0, 1]
            my_parameters = {REQUESTED_TIME_KEY: requested_times}
            params = {PARAMETERS_KEY: my_parameters}

        response = requests.post(api_url, json=params, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')), ModelType.TIME_GRAPH_TREE), response.status_code, response.text)
        else:
            print("failed to get tree: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def fetch_extensions(self):
        '''
        Fetch Extensions (loaded files)
        '''
        api_url = '{0}xml'.format(self.base_url)

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return TspClientResponse(ExtensionSet(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
            print("failed to get extensions: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def post_extension(self, mypath):
        '''
        Load an extension
        '''
        api_url = '{0}xml'.format(self.base_url)

        payload = dict(path=mypath)
        response = requests.post(api_url, data=payload, headers=headers_form)

        if response.status_code == 200:
            return TspClientResponse("Loaded", response.status_code, response.text)
        else:
            print("post extension failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    def delete_extension(self, name):
        '''
        Delete an extension
        '''
        api_url = '{0}xml/{1}'.format(self.base_url, name)

        response = requests.delete(api_url, headers=headers_form)

        if response.status_code == 200:
            return TspClientResponse("Deleted", response.status_code, response.text)
        else:
            print("post extension failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)
