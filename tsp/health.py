# The MIT License (MIT)
#
# Copyright (C) 2024 - Ericsson
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

"""Health class file."""

from enum import Enum

STATUS_KEY = "status"


class HealthStatus(Enum):
    '''
    The server is running and ready to receive requests
    '''
    UP = "UP"

    def __str__(self):
        return f"{self.value}"


# pylint: disable=too-few-public-methods
class Health:
    '''
    Model of server health
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

        # Health status
        if STATUS_KEY in params:
            self.status = HealthStatus(params.get(STATUS_KEY))
            del params[STATUS_KEY]
        else:
            self.status = None


    def __repr__(self):
        return f"Health(status={self.status})"
