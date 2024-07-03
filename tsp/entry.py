# The MIT License (MIT)
#
# Copyright (C) 2020, 2022 - Ericsson
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

"""Entry classes file."""

from enum import Enum

from tsp.output_element_style import OutputElementStyle

ID_KEY = "id"
PARENT_ID_KEY = "parentId"
LABELS_KEY = "labels"
STYLE_KEY = "style"
HEADER_NAME_KEY = "name"
HEADER_DATA_TYPE_KEY = "dataType"
HEADER_TOOLTIP_KEY = "tooltip"
UNKNOWN_ID = -1

# pylint: disable=too-few-public-methods

class EntryHeaderDataType(Enum):
    '''
    The data types of a column entry.
    '''
    NUMBER = "NUMBER"
    BINARY_NUMBER = "BINARY_NUMBER"
    TIMESTAMP = "TIMESTAMP"
    DURATION = "DURATION"
    STRING = "STRING"
    TIME_RANGE = "TIME_RANGE"


class EntryHeader:
    '''
    Entry Header
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

        # Name for this header.
        if HEADER_NAME_KEY in params:
            self.name = params.get(HEADER_NAME_KEY)
            del params[HEADER_NAME_KEY]
        else:
            self.name = None

        # Tooltip for this header.
        if HEADER_TOOLTIP_KEY in params:
            self.tooltip = params.get(HEADER_TOOLTIP_KEY)
            del params[HEADER_TOOLTIP_KEY]
        else:
            self.tooltip = None

        # Data type for this header.
        if HEADER_DATA_TYPE_KEY in params:
            self.data_type = EntryHeaderDataType(params.get(HEADER_DATA_TYPE_KEY))
            del params[HEADER_DATA_TYPE_KEY]
        else:
            self.data_type = None


class Entry:
    '''
    Basic entry
    '''

    def __init__(self, params):
        '''
        Unique Id for the entry
        '''
        # pylint: disable=invalid-name
        self.id = UNKNOWN_ID
        if ID_KEY in params:
            self.id = params.get(ID_KEY)
            del params[ID_KEY]

        # Parent entry Id, or -1 if the entry does not have a parent
        self.parent_id = UNKNOWN_ID
        if PARENT_ID_KEY in params:
            self.parent_id = params.get(PARENT_ID_KEY)
            del params[PARENT_ID_KEY]

        # Array of string that represent the content of each column
        self.labels = []
        if LABELS_KEY in params:
            self.labels = params.get(LABELS_KEY)
            del params[LABELS_KEY]

        # Style key used to search for a style.
        # The style map can be obtained by using the style endpoint.
        self.style = None
        if STYLE_KEY in params:
            if params.get(STYLE_KEY) is not None:
                self.style = OutputElementStyle(params.get(STYLE_KEY))
            del params[STYLE_KEY]
