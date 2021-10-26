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

"""Output Style classes file."""

PARENTKEY_KEY = "parentKey"
SYTLE_VALUES_KEY = "styleValues"
STYLES_KEY = "styles"


class OutputElementStyle(object):
    '''
    Output element style object for one style key. It supports style
    inheritance. To avoid creating new styles the element style can have a parent
    style and will have all the same style properties values as the parent and
    can add or override style properties.
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

        # Parent style key
        if PARENTKEY_KEY in params:
            self.parent_key = params.get(PARENTKEY_KEY)
            del params[PARENTKEY_KEY]
        else:
            self.parent_key = None

        # Style values to override or define properties
        if SYTLE_VALUES_KEY in params:
            self.style_values = params.get(SYTLE_VALUES_KEY)
            del params[SYTLE_VALUES_KEY]
        else:
            self.style_values = {}


class OutputStyleModel(object):
    '''
    Style model that will be returned by the server
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

        # Parent style key
        if STYLES_KEY in params:
            self.style = OutputElementStyle(params.get(STYLES_KEY))
            del params[STYLES_KEY]
        else:
            self.style = None
