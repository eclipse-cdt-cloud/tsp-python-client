# The MIT License (MIT)
#
# Copyright (C) 2020 - 2025 - Ericsson
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

"""OutputDescriptor class file."""

import json
from tsp.configuration import Configuration, ConfigurationEncoder
from tsp.output_capabilities import OutputCapabilities, OutputCapabilitiesEncoder

NA = "N/A"
UNKOWN = "UNKNOWN"
PARENT_ID_KEY = "parentId"
ID_KEY = "id"
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
TYPE_KEY = "type"
QUERY_PARAMETERS_KEY = "queryParameters"
START_TIME_KEY = "start"
END_TIME_KEY = "end"
IS_FINAL_KEY = "final"
COMPATIBLE_PROVIDERS_KEY = "compatibleProviders"
CONFIGURATION_KEY = "configuration"
CAPABILITES_KEY = "capabilities"


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class OutputDescriptor:
    '''
    classdocs
    '''

    # pylint: disable=too-many-branches
    def __init__(self, params):
        '''
        Constructor
        '''

        # Output provider's parent ID
        if PARENT_ID_KEY in params:
            # pylint: disable=invalid-name
            self.parent_id = params.get(PARENT_ID_KEY)
            del params[PARENT_ID_KEY]
        else:  # pragma: no cover
            self.parent_id = None

        # Output provider's ID
        if ID_KEY in params:
            # pylint: disable=invalid-name
            self.id = params.get(ID_KEY)
            del params[ID_KEY]
        else:  # pragma: no cover
            self.id = None

        # Human readable name
        if NAME_KEY in params:
            self.name = params.get(NAME_KEY)
            del params[NAME_KEY]
        else:  # pragma: no cover
            self.name = UNKOWN

        # Description of the output provider
        if DESCRIPTION_KEY in params:
            self.description = params.get(DESCRIPTION_KEY)
            del params[DESCRIPTION_KEY]
        else:  # pragma: no cover
            self.description = UNKOWN

        # Type of data returned by this output.
        # Serve as a hint to determine what kind of view should be use for this output
        # (ex. XY, Time Graph, Table, etc..)
        if TYPE_KEY in params:
            self.type = params.get(TYPE_KEY)
            del params[TYPE_KEY]
        else:  # pragma: no cover
            self.type = UNKOWN

        # Map of query parameters that the provider accept
        if QUERY_PARAMETERS_KEY in params:
            self.query_parameters = params.get(QUERY_PARAMETERS_KEY)
            del params[QUERY_PARAMETERS_KEY]
        else:
            self.query_parameters = {}

        # Start time
        if START_TIME_KEY in params:
            self.start = params.get(START_TIME_KEY)
            del params[START_TIME_KEY]
        else:
            self.start = 0

        # End time
        if END_TIME_KEY in params:
            self.end = params.get(END_TIME_KEY)
            del params[END_TIME_KEY]
        else:
            self.end = 0

        # Indicate if the start, end times and current model are final,
        # or if they will need to be refreshed later to represent a more up to date version
        if IS_FINAL_KEY in params:
            self.final = params.get(IS_FINAL_KEY)
            del params[IS_FINAL_KEY]
        else:
            self.final = 0

        # List of compatible outputs that can be used in the same view (ex. as overlay)
        if COMPATIBLE_PROVIDERS_KEY in params:
            self.compatible_providers = params.get(COMPATIBLE_PROVIDERS_KEY)
            del params[COMPATIBLE_PROVIDERS_KEY]
        else:
            self.compatible_providers = []

        # Configuration used to create this data provider.
        if CONFIGURATION_KEY in params:
            self.configuration = Configuration(params.get(CONFIGURATION_KEY))
            del params[CONFIGURATION_KEY]
        else:
            self.configuration = []
        
        # Capabilites of this data provider.
        if CAPABILITES_KEY in params:
            self.capabilities = OutputCapabilities(params.get(CAPABILITES_KEY))
            del params[CAPABILITES_KEY]
        else:
            self.capabilities = None


    def __repr__(self):
        return 'OutputDescriptor(id={}, name={}, description={}, type={})'.format(self.id, self.name, self.description, self.type)

    def to_json(self):
        return json.dumps(self, cls=OutputDescriptorEncoder, indent=4)

class OutputDescriptorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OutputDescriptor):
            result = {}
            # optional parent_id
            if obj.parent_id is not None:
                result[PARENT_ID_KEY] = obj.parent_id

            result[ID_KEY] = obj.id
            result[NAME_KEY] = obj.name
            result[DESCRIPTION_KEY] = obj.description
            result[TYPE_KEY] = obj.type
            # Hide non-TSP fields
            # result[QUERY_PARAMETERS_KEY] = obj.query_parameters
            # result[START_TIME_KEY] = obj.start
            # result[END_TIME_KEY] = obj.end
            # result[IS_FINAL_KEY] = obj.final
            # result[COMPATIBLE_PROVIDERS_KEY] = obj.compatible_providers

            # optional configuration
            if isinstance(obj.configuration, Configuration):
                result[CONFIGURATION_KEY] = ConfigurationEncoder().default(obj.configuration)

            # optional capabilities
            if isinstance(obj.capabilities, OutputCapabilities):
                result[CAPABILITES_KEY] = OutputCapabilitiesEncoder().default(obj.capabilities)
            return result
        return super().default(obj)
