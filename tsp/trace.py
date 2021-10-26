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

NA = "N/A"
UUID_KEY = "UUID"
NAME_KEY = "name"
START_TIME_KEY = "start"
END_TIME_KEY = "end"
PATH_KEY = "path"
NB_EVENT_KEY = "nbEvents"
PATH_TIME_KEY = "path"
INDEXING_STATUS_KEY = "indexingStatus"


class Trace(object):
    '''
    Model of a single trace
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

        # Trace's unique identifier
        if UUID_KEY in params:
            self.UUID = params.get(UUID_KEY)
            del params[UUID_KEY]
        else:  # pragma: no cover
            self.UUID = NA

        # User defined name for the trace
        if NAME_KEY in params:
            self.name = params.get(NAME_KEY)
            del params[NAME_KEY]
        else:  # pragma: no cover
            self.name = NA

        # Trace's start time
        if START_TIME_KEY in params:
            self.start = params.get(START_TIME_KEY)
            del params[START_TIME_KEY]
        else:  # pragma: no cover
            self.start = -1

        # Trace's end time
        if END_TIME_KEY in params:
            self.end = params.get(END_TIME_KEY)
            del params[END_TIME_KEY]
        else:  # pragma: no cover
            self.end = -1

        # URI of the trace
        if PATH_TIME_KEY in params:
            self.path = params.get(PATH_TIME_KEY)
            del params[PATH_TIME_KEY]
        else:  # pragma: no cover
            self.path = -1

        # Current number of events
        if NB_EVENT_KEY in params:
            self.number_of_events = params.get(NB_EVENT_KEY)
            del params[NB_EVENT_KEY]
        else:  # pragma: no cover
            self.number_of_events = 0

        # Indicate if the indexing of the trace is completed or still running.
        # If it still running, the end time and number of events are not final
        if INDEXING_STATUS_KEY in params:
            self.indexin_status = params.get(INDEXING_STATUS_KEY)
            del params[INDEXING_STATUS_KEY]
        else:  # pragma: no cover
            self.indexin_status = 0
