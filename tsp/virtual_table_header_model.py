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
                # Column ID
                column_id = None
                if COLUMN_ID_KEY in column:
                    column_id = column.get(COLUMN_ID_KEY)
                    del column[COLUMN_ID_KEY]

                # Column name
                column_name = None
                if COLUMN_NAME_KEY in column:
                    column_name = column.get(COLUMN_NAME_KEY)
                    del column[COLUMN_NAME_KEY]

                # Column description
                column_description = None
                if COLUMN_DESCRIPTION_KEY in column:
                    column_description = column.get(COLUMN_DESCRIPTION_KEY)
                    del column[COLUMN_DESCRIPTION_KEY]

                # Column type
                column_type = None
                if COLUMN_TYPE_KEY in column:
                    column_type = column.get(COLUMN_TYPE_KEY)
                    del column[COLUMN_TYPE_KEY]

                # Add column to the list
                self.columns.append({
                    COLUMN_ID_KEY: column_id,
                    COLUMN_NAME_KEY: column_name,
                    COLUMN_DESCRIPTION_KEY: column_description,
                    COLUMN_TYPE_KEY: column_type
                })

    def print(self):
        '''
        Print the virtual table header model
        '''
        print("Virtual Table Columns:")
        for column in self.columns:
            print("  id: " + str(column.get(COLUMN_ID_KEY)))
            print("  name: " + str(column.get(COLUMN_NAME_KEY)))
            print("  description: " + str(column.get(COLUMN_DESCRIPTION_KEY)))
            print("  type: " + str(column.get(COLUMN_TYPE_KEY)))
            print("-" * 50)
