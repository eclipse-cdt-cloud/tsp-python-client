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

"""ExperimentSet class file."""

import json
from tsp.experiment import Experiment, ExperimentEncoder

# pylint: disable=too-few-public-methods
class ExperimentSet:
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.experiments = []
        for obj in params:
            self.experiments.append(Experiment(obj))

class ExperimentSetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ExperimentSet):
            return [
                ExperimentEncoder().default(experiment) for experiment in obj.experiments
            ]
        return super().default(obj)