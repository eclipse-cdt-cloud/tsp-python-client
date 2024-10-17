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

import json


TITLE_KEY = "title"
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

# pylint: disable=too-few-public-methods


class XYModel:
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

        # Array of XY series
        self.series = []
        if SERIES_KEY in params:
            for series in params.get(SERIES_KEY):
                self.series.append(XYSeries(series))
            del params[SERIES_KEY]

    def __repr__(self):
        return f'XYModel(title={self.title}, series={self.series})'

class XYSeries:
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

    def __repr__(self):
        return 'XYSeries(name={}, id={}{}{}{}{})'.format(self.series_name, self.series_id,
           f', x_axis={self.x_axis}' if hasattr(self, 'x_axis') else '',
           f', y_axis={self.y_axis}' if hasattr(self, 'y_axis') else '',
           f', x_values={self.x_values}' if hasattr(self, 'x_values') else '',
           f', y_values={self.y_values}' if hasattr(self, 'y_values') else '')

class XYAxis:
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

    def __repr__(self):
        return f'XYAxis(label={self.label}, unit={self.unit}, data_type={self.data_type})'

class XYModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, XYModel):
            return {
                'title': obj.title,
                'common_x_axis': getattr(obj, 'common_x_axis', False),
                'series': [XYSeriesEncoder().default(series) for series in obj.series]
            }
        return super().default(obj)

class XYSeriesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, XYSeries):
            return {
                'series_name': obj.series_name,
                'series_id': obj.series_id,
                'x_axis': XYAxisEncoder().default(obj.x_axis) if hasattr(obj, 'x_axis') else None,
                'y_axis': XYAxisEncoder().default(obj.y_axis) if hasattr(obj, 'y_axis') else None,
                'x_values': obj.x_values,
                'y_values': obj.y_values,
                'tags': obj.tags
            }
        return super().default(obj)

class XYAxisEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, XYAxis):
            return {
                # 'label': obj.label,
                # 'unit': obj.unit,
                # 'data_type': obj.data_type
            }
        return super().default(obj)
