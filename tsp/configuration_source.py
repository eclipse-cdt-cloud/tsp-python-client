# The MIT License (MIT)
#
# Copyright (C) 2023 - Ericsson
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

"""ConfigurationSource class file."""

import json
from tsp.configuration_parameter_descriptor_set import ConfigurationParameterDescriptorSet, ConfigurationParameterDescriptorSetEncoder

NAME_KEY = "name"
DESCTIPION_KEY = "description"
ID_KEY = "id"
PARAM_DESC_KEY = "parameterDescriptors"
SCHEMA_KEY = "schema"


# pylint: disable=too-few-public-methods
class ConfigurationSource:
    '''
    Class to handle configurations available on the remote node
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        if NAME_KEY in params:
            self.name = params.get(NAME_KEY)
            del params[NAME_KEY]
        else:
            self.name = ""

        if DESCTIPION_KEY in params:
            self.description = params.get(DESCTIPION_KEY)
            del params[DESCTIPION_KEY]
        else:
            self.description = ""

        if ID_KEY in params:
            # pylint: disable=invalid-name
            self.id = params.get(ID_KEY)
            del params[ID_KEY]
        else:
            self.id = "unknown-id"

        self.parameter_descriptors = None
        if PARAM_DESC_KEY in params:
            # pylint: disable=invalid-name
            self.parameter_descriptors = ConfigurationParameterDescriptorSet(params.get(PARAM_DESC_KEY))
            params[PARAM_DESC_KEY]

        self.schema = None
        if SCHEMA_KEY in params:
            self.schema = params.get(SCHEMA_KEY)
            del params[SCHEMA_KEY]

    def __repr__(self):
        return 'ConfigurationSource(id={}, name={}, description={}, parameter_descriptors={}, schema={})'.format(
            self.id,
            self.name,
            self.description,
            self.parameter_descriptors if self.parameter_descriptors is not None else 'None',
            obj.schema if obj.schema is not None else 'None')

    def to_json(self):
        return json.dumps(self, cls=ConfigurationSourceEncoder, indent=4)


class ConfigurationSourceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ConfigurationSource):
            return {
                ID_KEY: obj.id,
                NAME_KEY: obj.name,
                DESCTIPION_KEY: obj.description,
                PARAM_DESC_KEY: ConfigurationParameterDescriptorSetEncoder().default(obj.parameter_descriptors) if isinstance(obj.parameter_descriptors, ConfigurationParameterDescriptorSet) else "None",
                SCHEMA_KEY: obj.schema if obj.schema is not None else 'None'
            }
        return super().default(obj)

