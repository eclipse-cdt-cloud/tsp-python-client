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

"""Virtual table header model file."""

COLUMN_ID_KEY = "id"
COLUMN_NAME_KEY = "name"
COLUMN_DESCRIPTION_KEY = "description"
COLUMN_TYPE_KEY = "type"


class VirtualTableHeaderModel:
    '''
    Virtual table header model that will be returned by the server
    '''

    def __init__(self, params):
        # Array of columns in the virtual table
        self.columns = []
        if params is not None:
            for column in params:
                # Create a new virtual table header column model
                self.columns.append(VirtualTableHeaderColumnModel(column))

    def print(self):
        '''
        Print the virtual table header model
        '''
        print("Virtual Table Columns:")
        for column in self.columns:
            column.print()

class VirtualTableHeaderColumnModel:
    '''
    Virtual table header column model that will be returned by the server
    '''

    def __init__(self, params):
        # Column ID
        self.id = None
        if COLUMN_ID_KEY in params:
            self.id = params.get(COLUMN_ID_KEY)
            del params[COLUMN_ID_KEY]

        # Column name
        self.name = None
        if COLUMN_NAME_KEY in params:
            self.name = params.get(COLUMN_NAME_KEY)
            del params[COLUMN_NAME_KEY]

        # Column description
        self.description = None
        if COLUMN_DESCRIPTION_KEY in params:
            self.description = params.get(COLUMN_DESCRIPTION_KEY)
            del params[COLUMN_DESCRIPTION_KEY]

        # Column type
        self.type = None
        if COLUMN_TYPE_KEY in params:
            self.type = params.get(COLUMN_TYPE_KEY)
            del params[COLUMN_TYPE_KEY]

    def print(self):
        '''
        Print the virtual table header column model
        '''
        print("  id: " + str(self.id))
        print("  name: " + str(self.name))
        print("  description: " + str(self.description))
        print("  type: " + str(self.type))
        print("-" * 50)