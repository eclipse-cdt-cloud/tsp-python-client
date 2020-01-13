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

headers={'content-type':'application/json', 'Accept':'application/json'}

class TspClient(object):
    '''
    Trace Server Protocol tsp_cli_client
    '''
    
    def __init__(self, base_url):
        '''
        Constructor
        '''
        self.base_url = base_url

    '''
    Fetch all available traces on the server
    :return: :class:`TspClientResponse <TraceSet>` object
    :rtype: TspClientResponse
     '''
    def fetch_traces(self): 
        api_url = '{0}traces'.format(self.base_url)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(TraceSet(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
            print ("get traces failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)
    
    '''
    Fetch a specific trace information
    :param uuid: Trace UUID to fetch
    :return: :class:`TspClientResponse <Trace>` object
    :rtype: TspClientResponse
    '''
    def fetch_trace(self, uuid):
        api_url = '{0}traces/{1}'.format(self.base_url, uuid)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
            print ("get trace failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)
    
    '''
    Open a trace on the server
     parameters: Query object
    :return: :class:`TspClientResponse <Trace>` object
    :rtype: TspClientResponse
    '''
    def open_trace(self, name, path):
        api_url = '{0}traces'.format(self.base_url)
        
        my_parameters = {'name': name, 'uri': path}
        parameters = {'parameters': my_parameters}
        
        response = requests.post(api_url, json=parameters, headers=headers)
        
        if response.status_code == 200:
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        elif response.status_code == 409:
            fetch_response = self.fetch_traces()
            if fetch_response.status_code == 200:
                #TODO don't just blindly use the first one
                return TspClientResponse(fetch_response.model.traces[0], response.status_code, response.text)
            else:
                return TspClientResponse(None, fetch_response.status_code, fetch_response.status_text)
        else:
            print ("post trace failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)
     
    '''
    Delete a trace on the server
    :param uuid: Trace UUID to delete
    :param delete_trace: Also delete the trace from disk
    :param remove_cache: Remove all cache for this trace
    :return: :class:`TspClientResponse <Trace>` object
    :rtype: TspClientResponse
     '''
    def delete_trace(self, uuid, delete_trace, remove_cache=False):
        api_url = '{0}traces/{1}'.format(self.base_url, uuid)
        parameters = {};
        if delete_trace: 
            parameters.append('deleteTrace', "true")
        
        if remove_cache: {
            parameters.append('removeCache', "true")
        }
        response = requests.delete(api_url, json=parameters, headers=headers)
        if response.status_code == 200:
            return TspClientResponse(Trace(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
            print ("delete trace failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)
        
        
    '''
    List all the outputs associated to this experiment
    :param exp_uuid: Experiment UUID
    :return: :class:  `TspClientResponse <OutputDescriptorSet>` object
    :rtype: TspClientResponse
     '''
    def experiment_outputs(self, exp_uuid):
        api_url = '{0}experiments/{1}/outputs/'.format(self.base_url, exp_uuid)

        response = requests.get(api_url, headers=headers)
    
        if response.status_code == 200:
            return TspClientResponse(OutputDescriptorSet(json.loads(response.content.decode('utf-8'))), response.status_code, response.text)
        else:
            print ("get output descriptors failed: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)

    '''
    Fetch Time Graph tree, Model extends TimeGraphEntry
    :param exp_uuid: Experiment UUID
    :param output_id: Output ID
    :param parameters: Query object
    :returns: :class:  `TspClientResponse <GenericResponse>` object Time graph entry response with entries and headers
    :rtype: TspClientResponse
     '''
    def fetch_timegraph_tree(self, exp_uuid, output_id, parameters = None):
        api_url = '{0}experiments/{1}/outputs/timeGraph/{2}/tree'.format(self.base_url, exp_uuid, output_id)
        
        if (parameters == None): 
            requested_times= [0, 1]
            my_parameters = {'requested_times': requested_times}
            params = {'parameters': my_parameters}
        else:
            params = parameters    
    
        response = requests.post(api_url, json=params, headers=headers)
    
        if response.status_code == 200:
            return TspClientResponse(GenericResponse(json.loads(response.content.decode('utf-8')), ModelType.TREE), response.status_code, response.text)
        else:    
            print ("failed to get tree: {0}".format(response.status_code))
            return TspClientResponse(None, response.status_code, response.text)
            
