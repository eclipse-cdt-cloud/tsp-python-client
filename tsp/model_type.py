# The MIT License (MIT)
#
# Copyright (C) 2020, 2022 - Ericsson
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

"""ModelType class file."""

from enum import Enum


class ModelType(Enum):
    '''
    Type enum to distinquish different parsing cases
    '''

    TIME_GRAPH_TREE = "time_graph_tree"
    TIME_GRAPH_STATE = "time_graph_state"
    TIME_GRAPH_ARROW = "time_graph_arrow"
    XY_TREE = "xy_tree"
    XY = "xy"
    DATA_TREE = "data_tree"
    VIRTUAL_TABLE_HEADER = "virtual_table_header"
    VIRTUAL_TABLE = "virtual_table"
