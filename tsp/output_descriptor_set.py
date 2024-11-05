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

"""OutputDescriptorSet class file."""

import json
from tsp.output_descriptor import OutputDescriptor, OutputDescriptorEncoder


# pylint: disable=too-few-public-methods
class OutputDescriptorSet:
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.descriptors = []
        for obj in params:
            self.descriptors.append(OutputDescriptor(obj))

    def __repr__(self):
        return 'OutputDescriptorSet({})'.format(', '.join(str(descriptor) for descriptor in self.descriptors))

    def to_json(self):
        return json.dumps(self, cls=OutputDescriptorSetEncoder, indent=4)


class OutputDescriptorSetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OutputDescriptorSet):
            return [
                OutputDescriptorEncoder().default(descriptor) for descriptor in obj.descriptors
            ]
        return super().default(obj)