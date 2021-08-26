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

from tsp.trace_set import TraceSet


NA = "N/A"
UUID_KEY = "UUID"
NAME_KEY = "name"
START_TIME_KEY = "start"
END_TIME_KEY = "end"
PATH_KEY = "path"
NB_EVENT_KEY = "nbEvents"
TRACES_TIME_KEY = "traces"
INDEXING_STATUS_KEY = "indexingStatus"


class Experiment(object):
    '''
    Model of a single Experiment
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

        '''
        Experiment's unique identifier
        '''
        if UUID_KEY in params:
            self.UUID = params.get(UUID_KEY)
            del params[UUID_KEY]
        else:
            self.UUID = NA

        '''
        User defined name for the experiment
        '''
        if NAME_KEY in params:
            self.name = params.get(NAME_KEY)
            del params[NAME_KEY]
        else:
            self.name = NA

        '''
        Experiment's start time
        '''
        if START_TIME_KEY in params:
            self.start = params.get(START_TIME_KEY)
            del params[START_TIME_KEY]
        else:
            self.start = -1

        '''
        Experiment's end time
        '''
        if END_TIME_KEY in params:
            self.end = params.get(END_TIME_KEY)
            del params[END_TIME_KEY]
        else:
            self.end = -1

        '''
        Current number of events
        '''
        if NB_EVENT_KEY in params:
            self.number_of_events = params.get(NB_EVENT_KEY)
            del params[NB_EVENT_KEY]
        else:
            self.number_of_events = 0

        '''
        Indicate if the indexing of the experiment is completed or still running.
        If it still running, the end time and number of events are not final
        '''
        if INDEXING_STATUS_KEY in params:
            self.indexin_status = params.get(INDEXING_STATUS_KEY)
            del params[INDEXING_STATUS_KEY]
        else:
            self.indexin_status = 0

        '''
        Array of all the traces contained in the experiment
        '''
        if TRACES_TIME_KEY in params:
            self.traces = TraceSet(params.get(TRACES_TIME_KEY))

        '''
        Store other key/value pairs that are not defined in the TSP in a dictionary
        '''
        self.others = {}
        if params:
            self.others = copy.deepcopy(params)
