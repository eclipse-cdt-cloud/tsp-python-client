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

"""ConfigurationSet class file."""

import json
from tsp.configuration_parameter_descriptor import ConfigurationParameterDescriptor, ConfigurationParameterDescriptorEncoder


# pylint: disable=too-few-public-methods
class ConfigurationParameterDescriptorSet:
    '''
    Class to handle configuration parameter descriptor available on the remote node
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.configuration_parameter_set = []
        for obj in params:
            self.configuration_parameter_set.append(ConfigurationParameterDescriptor(obj))

    def __repr__(self) -> str:
        return 'ConfigurationParameterDescriptorSet({})'.format(', '.join(str(source) for source in self.configuration_parameter_set))

    def to_json(self):
        return (json.dumps(self, cls=ConfigurationParameterDescriptorSetEncoder, indent=4))


class ConfigurationParameterDescriptorSetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ConfigurationParameterDescriptorSet):
            return [
                ConfigurationParameterDescriptorEncoder().default(configuration_parameter) for configuration_parameter in obj.configuration_parameter_set
            ]
        return super().default(obj)