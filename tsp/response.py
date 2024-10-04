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

"""Response classes file."""

import json

from enum import Enum

from tsp.model_type import ModelType
from tsp.output_descriptor import OutputDescriptor
from tsp.virtual_table_header_model import VirtualTableHeaderModel
from tsp.virtual_table_model import VirtualTableModel
from tsp.time_graph_model import TimeGraphModel, TimeGraphArrow, TimeGraphModelEncoder, TimeGraphArrowEncoder
from tsp.xy_model import XYModel
from tsp.entry_model import EntryModel, EntryModelEncoder
from tsp.xy_model import XYModel, XYModelEncoder

MODEL_KEY = "model"
OUTPUT_DESCRIPTOR_KEY = "output"
RESPONSE_STATUS_KEY = "status"
STATUS_MESSAGE_KEY = "statusMessage"


class ResponseStatus(Enum):
    '''
    Model is partial, data provider is still computing. If this status is
    returned, it's viewer responsability to request again the data provider after
    waiting some time. Request data provider until COMPLETED status is received
    '''
    RUNNING = "RUNNING"

    '''
    Model is complete, no need to request data provider again
    '''
    COMPLETED = "COMPLETED"

    '''
    Error happened. Please see logs or detailed message of status.
    '''
    FAILED = "FAILED"

    '''
    Task has been cancelled. Please see logs or detailed message of status.
    '''
    CANCELLED = "CANCELLED"


# pylint: disable=too-few-public-methods
class GenericResponse:
    '''
    Output element style object for one style key. It supports style
    inheritance. To avoid creating new styles the element style can have a parent
    style and will have all the same style properties values as the parent and
    can add or override style properties.
    '''

    def __init__(self, params, model_type):
        '''
        Constructor
        '''
        self.model_type = model_type

        # Model returned in the response
        self.model = params.get(MODEL_KEY)
        if MODEL_KEY in params and params.get(MODEL_KEY) is not None:
            if self.model_type == ModelType.TIME_GRAPH_TREE:
                self.model = EntryModel(params.get(MODEL_KEY), self.model_type)
            elif self.model_type == ModelType.TIME_GRAPH_STATE:
                self.model = TimeGraphModel(params.get(MODEL_KEY))
            elif self.model_type == ModelType.TIME_GRAPH_ARROW:
                arrows = []
                for arrow in params.get(MODEL_KEY):
                    arrows.append(TimeGraphArrow(arrow))
                self.model = arrows
            elif self.model_type == ModelType.XY_TREE:
                self.model = EntryModel(params.get(MODEL_KEY))
            elif self.model_type == ModelType.XY:
                self.model = XYModel(params.get(MODEL_KEY))
            elif self.model_type == ModelType.DATA_TREE:
                self.model = EntryModel(params.get(MODEL_KEY), self.model_type)
            elif self.model_type == ModelType.VIRTUAL_TABLE_HEADER:
                self.model = VirtualTableHeaderModel(params.get(MODEL_KEY))
            elif self.model_type == ModelType.VIRTUAL_TABLE: 
                self.model = VirtualTableModel(params.get(MODEL_KEY))

        # Output descriptor
        if OUTPUT_DESCRIPTOR_KEY in params:
            self.output = OutputDescriptor(params.get(OUTPUT_DESCRIPTOR_KEY))
        else:
            self.output = None

        # Response status as described by ResponseStatus
        if RESPONSE_STATUS_KEY in params:
            self.status = ResponseStatus(params.get(RESPONSE_STATUS_KEY))
        else:  # pragma: no cover
            self.status = ResponseStatus.FAILED

        # Message associated with the response
        if STATUS_MESSAGE_KEY in params:
            self.status_text = params.get(STATUS_MESSAGE_KEY)
        else:  # pragma: no cover
            self.status_text = ""

    def __repr__(self) -> str:
        return 'GenericResponse(model_type={}, model={}, output_descriptor={}, status={}, status_text={})'.format(
            self.model_type, self.model, self.output, self.status, self.status_text
        )


class GenericResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GenericResponse):
            model = obj.model
            if model is None:
                return None
            if obj.model_type ==  ModelType.TIME_GRAPH_TREE \
                or obj.model_type == ModelType.XY_TREE \
                or obj.model_type == ModelType.DATA_TREE:
                model = EntryModelEncoder().default(obj.model)
            elif obj.model_type == ModelType.TIME_GRAPH_STATE:
                model = TimeGraphModelEncoder().default(obj.model)
            elif obj.model_type == ModelType.TIME_GRAPH_ARROW:
                model = [TimeGraphArrowEncoder().default(arrow) for arrow in obj.model]
            elif obj.model_type == ModelType.XY:
                model = XYModelEncoder().default(obj.model)
            return model

        return super().default(obj)
