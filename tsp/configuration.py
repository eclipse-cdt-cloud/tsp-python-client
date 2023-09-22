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

"""Configuration class file."""

NAME_KEY = "name"
DESCTIPION_KEY = "description"
ID_KEY = "id"
SOURCE_TYPE_ID = "sourceTypeId"
PARAMETER_KEY = "parameters"

# pylint: disable=too-few-public-methods
class Configuration:
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

        if SOURCE_TYPE_ID in params:
            # pylint: disable=invalid-name
            self.source_type_id = params.get(SOURCE_TYPE_ID)
            del params[SOURCE_TYPE_ID]
        else:
            self.source_type_id = "unknown_source_type_id"

        if PARAMETER_KEY in params:
            # pylint: disable=invalid-name
            self.parameters = params.get(PARAMETER_KEY)
            del params[PARAMETER_KEY]
        else:
            self.parameters = {}


    # pylint: disable=consider-using-f-string
    def to_string(self):
        '''
        to_string method
        '''
        return 'Configuration[name={0}, description={1}, id={2}, source_type_id={3}, parameters={4}]'.format(self.name,
          self.description, self.id, self.source_type_id, self.parameters)
