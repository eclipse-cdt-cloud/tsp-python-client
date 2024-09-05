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

"""VirtualTableModel class file."""

from tsp.virtual_table_tag import VirtualTableTag

SIZE_KEY = "size"
LOW_INDEX_KEY = "lowIndex"
COLUMN_IDS_KEY = "columnIds"
LINES_KEY = "lines"
TAGS_KEY = "tags"

TABLE_LINE_INDEX_KEY = "index"
TABLE_LINE_CELLS_KEY = "cells"
TABLE_LINE_CELL_CONTENT_KEY = "content"


# pylint: disable=too-few-public-methods
class VirtualTableModel:
    '''
    Virtual table model that will be returned by the server
    '''

    def __init__(self, params):
        # Size of the virtual table
        self.size = 0
        if SIZE_KEY in params:
            if params.get(SIZE_KEY) is not None and type(params.get(SIZE_KEY)) is int:
                self.size = int(params.get(SIZE_KEY))
            del params[SIZE_KEY]

        # Index of the first line in the virtual table
        self.low_index = 0
        if LOW_INDEX_KEY in params:
            if params.get(LOW_INDEX_KEY) is not None and type(params.get(LOW_INDEX_KEY)) is int:
                self.low_index = int(params.get(LOW_INDEX_KEY))
            del params[LOW_INDEX_KEY]

        # Array of column IDs in the virtual table
        self.column_ids = []
        if COLUMN_IDS_KEY in params:
            if params.get(COLUMN_IDS_KEY) is not None:
                for column_id in params.get(COLUMN_IDS_KEY):
                    self.column_ids.append(column_id)
            del params[COLUMN_IDS_KEY]

        # Array of lines in the virtual table
        self.lines = []
        if LINES_KEY in params:
            for line in params.get(LINES_KEY):
                self.lines.append(VirtualTableLine(line))
            del params[LINES_KEY]

    def print(self):
        print("VirtualTableModel:")
        print(f"  size: {self.size}")
        print(f"  low_index: {self.low_index}")
        print(f"  column_ids: {self.column_ids}")

        print("  lines:")
        for i, line in enumerate(self.lines):
            line.print()

class VirtualTableLine:
    '''
    Virtual table line that will be returned by the server
    '''

    def __init__(self, params):
        # Index of the line in the virtual table
        self.index = -1
        if TABLE_LINE_INDEX_KEY in params:
            if params.get(TABLE_LINE_INDEX_KEY) is not None and type(params.get(TABLE_LINE_INDEX_KEY)) is int:
                self.index = int(params.get(TABLE_LINE_INDEX_KEY))
            del params[TABLE_LINE_INDEX_KEY]

        # Array of cells in the line
        self.cells = []
        if TABLE_LINE_CELLS_KEY in params:
            if params.get(TABLE_LINE_CELLS_KEY) is not None:
                for cell in params.get(TABLE_LINE_CELLS_KEY):
                    self.cells.append(VirtualTableLineCell(cell))
            del params[TABLE_LINE_CELLS_KEY]

        self.tags = VirtualTableTag.NO_TAGS
        if TAGS_KEY in params:
            if params.get(TAGS_KEY) is not None and type(params.get(TAGS_KEY)) is int:
                tags = int(params.get(TAGS_KEY))

                match tags:
                    case 0: # Tag 0 is used for no tags
                        self.tags = VirtualTableTag.NO_TAGS
                    case 1 | 2: # Tags 1 and 2 are reserved
                        self.tags = VirtualTableTag.RESERVED
                    case 4: # Tag 4 is used for border
                        self.tags = VirtualTableTag.BORDER
                    case 8: # Tag 8 is used for highlight
                        self.tags = VirtualTableTag.HIGHLIGHT
                    case _: # Other tags are not supported
                        self.tags = VirtualTableTag.NO_TAGS
            del params[TAGS_KEY]

    def print(self):

        print(f"    index: {self.index}")
        print(f"    tags: {self.tags.name}")
        print("    cells:")
        for i, cell in enumerate(self.cells):
            cell.print()
        print(f"    {'-' * 30}")

class VirtualTableLineCell:
    '''
    Virtual table line cell that will be returned by the server
    '''

    def __init__(self, params):
        # Content of the cell
        self.content = None
        if TABLE_LINE_CELL_CONTENT_KEY in params:
            if params.get(TABLE_LINE_CELL_CONTENT_KEY) is not None:
                self.content = params.get(TABLE_LINE_CELL_CONTENT_KEY)
            del params[TABLE_LINE_CELL_CONTENT_KEY]

        self.tags = VirtualTableTag.NO_TAGS
        if TAGS_KEY in params:
            if params.get(TAGS_KEY) is not None and type(params.get(TAGS_KEY)) is int:
                tags = int(params.get(TAGS_KEY))

                match tags:
                    case 0: # Tag 0 is used for no tags
                        self.tags = VirtualTableTag.NO_TAGS
                    case 1 | 2: # Tags 1 and 2 are reserved
                        self.tags = VirtualTableTag.RESERVED
                    case 4: # Tag 4 is used for border
                        self.tags = VirtualTableTag.BORDER
                    case 8: # Tag 8 is used for highlight
                        self.tags = VirtualTableTag.HIGHLIGHT
                    case _: # Other tags are not supported
                        self.tags = VirtualTableTag.NO_TAGS
            del params[TAGS_KEY]

    def print(self):
        print(f"      \"{TABLE_LINE_CELL_CONTENT_KEY}\": \"{self.content}\"")
        print(f"      \"tags\": {self.tags.name}")
        print(f"    {'-' * 10}")