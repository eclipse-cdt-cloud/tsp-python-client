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

from tsp.configuration_parameter_descriptor_set import ConfigurationParameterDescriptorSet

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

    # pylint: disable=consider-using-f-string
    def to_string(self):
        '''
        to_string 
        '''
        my_str = "no parameter descriptor"
        if self.parameter_descriptors is not None:
            my_str = self.parameter_descriptors.to_string()

        my_schema = "no schema"
        if self.schema is not None:
            my_schema = self.schema

        return'Configuration Source[id={0}, name={1}, description: {2}, parameter_descriptor={3}, schema={4}]'.format(self.id,
              self.name, self.description, my_str, my_schema)

