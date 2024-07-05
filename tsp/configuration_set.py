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

"""ConfigurationSet class file."""

from tsp.configuration import Configuration


# pylint: disable=too-few-public-methods
class ConfigurationSet:
    '''
    Class to handle configurations available on the remote node
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.configuration_set = []
        for obj in params:
            self.configuration_set.append(Configuration(obj))


    def __str__(self):
        '''
        to string method
        '''
        my_str = ''
        sep = ''
        for desc in self.configuration_set:
            my_str += f'{sep}{desc}\n'
            sep = ', '
        return my_str