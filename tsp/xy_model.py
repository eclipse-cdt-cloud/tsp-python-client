# The MIT License (MIT)
#
# Copyright (C) 2021 - Ericsson
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

"""XY classes file."""

TITLE_KEY = "title"
COMMON_X_AXIS_KEY = "commonXAxis"
SERIES_KEY = "series"
SERIES_NAME_KEY = "seriesName"
SERIES_ID_KEY = "seriesId"
X_AXIS_KEY = "xAxis"
Y_AXIS_KEY = "yAxis"
X_VALUES_KEY = "xValues"
Y_VALUES_KEY = "yValues"
TAGS_KEY = "tags"
LABEL_KEY = "label"
UNIT_KEY = "unit"
DATA_TYPE_KEY = "dataType"


class XYModel(object):
    '''
    Model of a XY chart, contains at least one XY series
    '''

    def __init__(self, params):
        '''
        Title of the model
        '''
        if TITLE_KEY in params:
            self.title = params.get(TITLE_KEY)
            del params[TITLE_KEY]

        # Indicate if all the Y values are using the same X axis
        if COMMON_X_AXIS_KEY in params:
            self.common_x_axis = params.get(COMMON_X_AXIS_KEY)
            del params[COMMON_X_AXIS_KEY]

        # Array of XY series
        self.series = []
        if SERIES_KEY in params:
            for series in params.get(SERIES_KEY):
                self.series.append(XYSeries(series))
            del params[SERIES_KEY]

    def print(self):  # pragma: no cover
        print(f'XY title: {self.title}')

        common_x_axis = False
        if hasattr(self, 'common_x_axis'):
            common_x_axis = self.common_x_axis
        print(f'XY has common X axis: {common_x_axis}')

        for series in self.series:
            series.print()


class XYSeries(object):
    '''
    Represent a XY series and its values
    '''

    def __init__(self, params):
        '''
        Name of the series
        '''
        if SERIES_NAME_KEY in params:
            self.series_name = params.get(SERIES_NAME_KEY)
            del params[SERIES_NAME_KEY]

        # Ìd of the series
        if SERIES_ID_KEY in params:
            self.series_id = params.get(SERIES_ID_KEY)
            del params[SERIES_ID_KEY]

        # Description of the X axis
        if X_AXIS_KEY in params:
            self.x_axis = XYAxis(params.get(X_AXIS_KEY))
            del params[X_AXIS_KEY]

        # Description of the Y axis
        if Y_AXIS_KEY in params:
            self.y_axis = XYAxis(params.get(Y_AXIS_KEY))
            del params[Y_AXIS_KEY]

        # Series' X values
        self.x_values = []
        if X_VALUES_KEY in params:
            for x_value in params.get(X_VALUES_KEY):
                self.x_values.append(x_value)
            del params[X_VALUES_KEY]

        # Series' Y values
        self.y_values = []
        if Y_VALUES_KEY in params:
            for y_value in params.get(Y_VALUES_KEY):
                self.y_values.append(y_value)
            del params[Y_VALUES_KEY]

        # Array of tags for each XY value, used when a value passes a filter
        self.tags = []
        if TAGS_KEY in params:
            for tag in params.get(TAGS_KEY):
                self.tags.append(tag)
            del params[TAGS_KEY]

    def print(self):  # pragma: no cover
        print(f' Series name: {self.series_name}')
        print(f' Series id: {self.series_id}')

        if hasattr(self, 'x_axis'):
            print(f' Series X-axis:\n{self.x_axis.print()}')
            print(f' Series Y-axis:\n{self.y_axis.print()}')
        for value in self.x_values:
            print(f' Series X-value: {value}')
        for value in self.y_values:
            print(f' Series Y-value: {value}')
        for tag in self.tags:
            print(f' Series tag: {tag}')


class XYAxis(object):
    '''
    Description of an axis for XY chart
    '''

    def __init__(self, params):
        '''
        Label of the axis
        '''
        if LABEL_KEY in params:
            self.label = params.get(LABEL_KEY)
            del params[LABEL_KEY]

        # The units used for the axis, to be appended to the numbers
        if UNIT_KEY in params:
            self.unit = params.get(UNIT_KEY)
            del params[UNIT_KEY]

        # Type of data for this axis, to give hint on number formatting
        if DATA_TYPE_KEY in params:
            self.data_type = params.get(DATA_TYPE_KEY)
            del params[DATA_TYPE_KEY]

    def print(self):  # pragma: no cover
        print(f'  Axis label: {self.label}')
        print(f'  Axis unit: {self.unit}')
        print(f'  Axis data type: {self.data_type}')
