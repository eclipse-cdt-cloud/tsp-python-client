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

from tsp.trace import NAME_KEY
from tsp.output_element_style import OutputElementStyle
import copy

ID_KEY = "id"
PARENT_ID_KEY = "parentId"
LABELS_KEY = "labels"
STYLE_KEY = "style"
HEADER_NAME_KEY = "name"
UNKNOWN_ID = -1


class EntryHeader(object):
    '''
    Entry Header
    '''
    def __init__(self, params):
        '''
        Displayed name
        '''
        self.name = ""
        if NAME_KEY in params:
            self.name = params.get(NAME_KEY)
            del params[NAME_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)


class Entry(object):
    '''
    Basic entry
    '''
    def __init__(self, params, copy_others=True):
        '''
        Unique Id for the entry
        '''
        self.id = UNKNOWN_ID
        if ID_KEY in params:
            self.id = params.get(ID_KEY)
            del params[ID_KEY]
        '''
        Parent entry Id, or -1 if the entry does not have a parent
        '''
        self.parent_id = UNKNOWN_ID
        if PARENT_ID_KEY in params:
            self.parent_id = params.get(PARENT_ID_KEY)
            del params[PARENT_ID_KEY]
        '''
        Array of string that represent the content of each column
        '''
        self.labels = []
        if LABELS_KEY in params:
            self.labels = params.get(LABELS_KEY)
            del params[LABELS_KEY]
        '''
        Style key used to search for a The style map can be obtained by using the style endpoint.
        '''
        self.style = None
        if STYLE_KEY in params:
            if params.get(STYLE_KEY) is not None:
                self.style = OutputElementStyle(params.get(STYLE_KEY))
            del params[STYLE_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in a dictionary
        '''
        self.copy_others = copy_others
        if copy_others:
            self.others = {}
            if params:
                self.others = copy.deepcopy(params)
