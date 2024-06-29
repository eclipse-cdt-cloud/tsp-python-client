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

"""Configuration parameter descriptors class file."""

KEY_NAME_KEY = "keyName"
DESCTIPION_KEY = "description"
DATA_TYPE_KEY = "dataType"
REQUIRED_KEY = "isRequired"

# pylint: disable=too-few-public-methods
class ConfigurationParameterDescriptor:
    '''
    Class to handle configuration parameter descriptor available on the remote node
    '''
    def __init__(self, params):
        '''
        Constructor
        '''

        if KEY_NAME_KEY in params:
            self.key_name = params.get(KEY_NAME_KEY)
            del params[KEY_NAME_KEY]
        else:
            self.key_name = ""

        if DESCTIPION_KEY in params:
            self.description = params.get(DESCTIPION_KEY)
            del params[DESCTIPION_KEY]
        else:
            self.description = ""

        if DATA_TYPE_KEY in params:
            # pylint: disable=invalid-name
            self.data_type = params.get(DATA_TYPE_KEY)
            del params[DATA_TYPE_KEY]
        else:
            self.data_type = "STRING"

        if REQUIRED_KEY in params:
            # pylint: disable=invalid-name
            self.is_required = params.get(REQUIRED_KEY)
            del params[REQUIRED_KEY]
        else:
            self.is_required = "unknown_source_type_id"


    def __str__(self):
        '''
        to_string method
        '''
        return f'ConfigurationParameterDescriptor[key_name={self.key_name}, description={self.description}, data_type={self.data_type}, is_required={self.is_required}]'