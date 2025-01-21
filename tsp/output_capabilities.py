# The MIT License (MIT)
#
# Copyright (C) 2025 - Ericsson
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

"""OutputDescriptor class file."""

import json

CAN_CREATE_KEY = "canCreate"
CAN_DELETE_KEY = "canDelete"

# pylint: disable=too-few-public-methods,too-many-instance-attributes
class OutputCapabilities:
    '''
    classdocs
    '''

    # pylint: disable=too-many-branches
    def __init__(self, params):
        '''
        Constructor
        '''

        # Capability canCreate
        if CAN_CREATE_KEY in params:
            # pylint: disable=invalid-name
            self.can_create = params.get(CAN_CREATE_KEY)
            del params[CAN_CREATE_KEY]
        else:  # pragma: no cover
            self.can_create = None

        if CAN_DELETE_KEY in params:
            # pylint: disable=invalid-name
            self.can_delete = params.get(CAN_DELETE_KEY)
            del params[CAN_DELETE_KEY]
        else:  # pragma: no cover
            self.can_delete = None

    def __repr__(self):
        return 'OutputCapabilities(canCreate={}, canDelete={})'.format(self.can_create, self.can_delete)

    def to_json(self):
        return json.dumps(self, cls=OutputCapabilities, indent=4)

class OutputCapabilitiesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OutputCapabilities):
            return {
                'canCreate': obj.can_create,
                'canDelete': obj.can_delete
            }
        return super().default(obj)
