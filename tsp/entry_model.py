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

import copy

from tsp.model_type import ModelType
from tsp.time_graph_model import TimeGraphEntry
from tsp.entry import EntryHeader, Entry
from tsp.column_descriptor import ColumnDescriptor

HEADER_KEY = "headers"
ENTRIES_KEY = "entries"
DESCRIPTORS_KEY = "columnDescriptors"


class EntryModel(object):
    '''
    Entry model that will be returned by the server
    '''

    def __init__(self, params, model_type=ModelType.XY_TREE):
        '''
        Array of entry column
        '''
        self.headers = []
        if HEADER_KEY in params:
            if (params.get(HEADER_KEY) is not None):
                for column in params.get(HEADER_KEY):
                    self.headers.append(EntryHeader(column))
            del params[HEADER_KEY]

        '''
        Array of column descriptors
        '''
        self.descriptors = []
        if DESCRIPTORS_KEY in params:
            for column in params.get(DESCRIPTORS_KEY):
                self.descriptors.append(ColumnDescriptor(column))
            del params[DESCRIPTORS_KEY]

        '''
        Array of entry
        '''
        self.entries = []
        if ENTRIES_KEY in params:
            entries = params.get(ENTRIES_KEY)
            for entry in entries:
                if model_type == ModelType.TIME_GRAPH_TREE:
                    self.entries.append(TimeGraphEntry(entry))
                else:
                    self.entries.append(Entry(entry))
            del params[ENTRIES_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)
