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

"""Object model file."""

import json

OBJECT_KEY = "object"
NEXT_KEY = "next"
PREVIOUS_KEY = "previous"

class ObjectModel:
    '''
    Object model that will be returned by the server
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        if OBJECT_KEY in params:
            self.object = params.get(OBJECT_KEY)
            del params[OBJECT_KEY]
        else:
            self.object = ""

        if NEXT_KEY in params:
            self.next = params.get(NEXT_KEY)
            del params[NEXT_KEY]
        else:
            self.next = ""

        if PREVIOUS_KEY in params:
            self.previous = params.get(PREVIOUS_KEY)
            del params[PREVIOUS_KEY]
        else:
            self.previous = ""

    def print(self):
        '''
        Print the Object model
        '''
        print("\"object\": {0}".format(json.dumps(self.object, indent=2)))
        if self.previous is not None:
            print("\"previous\": {0}".format(json.dumps(self.previous)))
        if self.next is not None:
            print("\"next\": {0}".format(json.dumps(self.next)))
