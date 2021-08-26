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
from tsp.entry import Entry

TYPE_KEY = "type"
START_TIME_KEY = "startTime"
END_TIME_KEY = "endTime"
HAS_ROW_MODEL_KEY = "hasRowModel"
ROWS_KEY = "rows"
ENTRY_ID_KEY = "entryID"
STATES_KEY = "states"
DURATION_KEY = "duration"
LABEL_KEY = "label"
VALUE_KEY = "value"
TAGS_KEY = "tags"
STYLE_KEY = "style"
SOURCE_ID_TAG = "sourceId"
DESTINATION_ID_TAG = "destinationId"


class TimeGraphEntry(Entry):
    '''
    Entry in a time graph
    '''

    def __init__(self, params):
        super(TimeGraphEntry, self).__init__(params, False)

        '''
        Type of the entry
        '''
        if TYPE_KEY in params:
            self.type = params.get(TYPE_KEY)
            del params[TYPE_KEY]

        '''
        Start time of the entry
        '''
        if START_TIME_KEY in params:
            self.start_time = params.get(START_TIME_KEY)
            del params[START_TIME_KEY]

        '''
        End time of the entry
        '''
        if END_TIME_KEY in params:
            self.end_time = params.get(END_TIME_KEY)
            del params[END_TIME_KEY]

        '''
        Indicate if the entry will have row data
        '''
        if HAS_ROW_MODEL_KEY in params:
            self.has_row_model = params.get(HAS_ROW_MODEL_KEY)
            del params[HAS_ROW_MODEL_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in
        a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)


class TimeGraphModel(object):
    '''
    Time Graph model that will be returned by the server
    '''

    def __init__(self, params):
        self.rows = []
        if ROWS_KEY in params:
            for row in params.get(ROWS_KEY):
                self.rows.append(TimeGraphRow(row))
            del params[ROWS_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in
        a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)


class TimeGraphRow(object):
    '''
    Time graph row described by an array of states for a specific entry
    '''

    def __init__(self, params):
        '''
        Entry Id associated to the state array
        '''
        if ENTRY_ID_KEY in params:
            self.entry_id = params.get(ENTRY_ID_KEY)
            del params[ENTRY_ID_KEY]

        '''
        Array of states
        '''
        self.states = []
        if STATES_KEY in params:
            for state in params.get(STATES_KEY):
                self.states.append(TimeGraphState(state))
            del params[STATES_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in
        a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)


class TimeGraphState(object):
    '''
    Time graph state
    '''

    def __init__(self, params):
        '''
        Start time of the state
        '''
        if START_TIME_KEY in params:
            self.start_time = params.get(START_TIME_KEY)
            del params[START_TIME_KEY]

        '''
        Duration of the state
        '''
        if DURATION_KEY in params:
            self.duration = params.get(DURATION_KEY)
            del params[DURATION_KEY]

        '''
        Label to apply to the state
        '''
        if LABEL_KEY in params:
            self.label = params.get(LABEL_KEY)
            del params[LABEL_KEY]

        '''
        Values associated to the state
        '''
        if VALUE_KEY in params:
            self.value = params.get(VALUE_KEY)
            del params[VALUE_KEY]

        '''
        Tags for the state, used when the state pass a filter
        '''
        if TAGS_KEY in params:
            self.tags = params.get(TAGS_KEY)
            del params[TAGS_KEY]

        '''
        Optional information on the style to format this state
        '''
        if STYLE_KEY in params:
            self.style = params.get(STYLE_KEY)
            del params[STYLE_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in
        a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)


class TimeGraphArrow(object):
    '''
    Arrow for time graph
    '''

    def __init__(self, params):
        '''
        Source entry Id for the arrow
        '''
        if SOURCE_ID_TAG in params:
            self.source_id = params.get(SOURCE_ID_TAG)
            del params[SOURCE_ID_TAG]

        '''
        Destination entry Id for the arrow
        '''
        if DESTINATION_ID_TAG in params:
            self.destination_id = params.get(DESTINATION_ID_TAG)
            del params[DESTINATION_ID_TAG]

        '''
        Start time of the arrow
        '''
        if START_TIME_KEY in params:
            self.start_time = params.get(START_TIME_KEY)
            del params[START_TIME_KEY]

        '''
        Duration of the arrow
        '''
        if DURATION_KEY in params:
            self.duration = params.get(DURATION_KEY)
            del params[DURATION_KEY]

        '''
        Value associated to the arrow
        '''
        if VALUE_KEY in params:
            self.value = params.get(VALUE_KEY)
            del params[VALUE_KEY]

        '''
        Optional information on the style to format this arrow
        '''
        if STYLE_KEY in params:
            self.style = params.get(STYLE_KEY)
            del params[STYLE_KEY]

        '''
        Store other key/value pairs that are not defined in the TSP in
        a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)
