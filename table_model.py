
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

"""TableModel class file."""

from tabulate import tabulate

import pandas as pd


# pylint: disable=too-few-public-methods
class TableModel:
    """TreeModel class implementation."""

    def __init__(self, model, headers=None):
        self._headers = headers
        self._model = model

    def print(self):
        """Render this tree model."""
        frame = {}
        data = []
        low_index = self._model.low_index
        for line in self._model.lines:
            row = []
            row.append(low_index)
            low_index += 1
            for cell in line.cells:
                row.append(cell.content)
            data.append(row)

        headers = []
        headers.append("Index")

        if self._headers is not None:
            for col_id in self._model.column_ids:
                headers.append(self._headers[col_id].name)

            # for header in self._headers:
            #     headers.append(header.name)
            if len(headers) == len(data[0]):
                frame = pd.DataFrame(data, columns=headers)
            else:
                frame = pd.DataFrame(data)
        else:
            frame = pd.DataFrame(data)
        # print(frame.to_string())
        #frame.to_csv('output.csv', index=False, sep='\t')
        print(tabulate(frame.values, headers, tablefmt="fancy_grid"))

