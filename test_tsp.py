# The MIT License (MIT)
#
# Copyright (C) 2021, 2023 - Ericsson
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

"""TestTspClient class file."""

import os
import time
import uuid

import pytest
import requests

from tsp.health import HealthStatus
from tsp.response import ResponseStatus
from tsp.tsp_client import TspClient
from tsp.virtual_table_tag import VirtualTableTag
from tsp.configuration_source import ConfigurationSource
from tsp.configuration_source_set import ConfigurationSourceSet
from tsp.output_descriptor import OutputDescriptor

STATISTICS_DP_ID = (
    "org.eclipse.tracecompass.analysis.timing.core.segmentstore.SegmentStoreStatisticsDataProvider:"
    "org.eclipse.linuxtools.lttng2.ust.analysis.callstack"
)
TABLE_DP_ID = (
    "org.eclipse.tracecompass.analysis.timing.core.segmentstore.SegmentStoreTableDataProvider:"
    "org.eclipse.linuxtools.lttng2.ust.analysis.callstack"
)
TIMEGRAPH_DP_ID = "org.eclipse.tracecompass.internal.analysis.os.linux.core.threadstatus.ThreadStatusDataProvider"

INANDOUT_DP_ID = "org.eclipse.tracecompass.incubator.inandout.core.analysis.inAndOutdataProviderFactory"

REQUESTED_TIME_START = 1332170682440133097
REQUESTED_TIME_END = 1332170692664579801
REQUESTED_TIME_LENGTH = 10
REQUESTED_TIME_STEP = (REQUESTED_TIME_END -
                       REQUESTED_TIME_START) / REQUESTED_TIME_LENGTH


CONFIG_SOURCE_TYPE = 'org.eclipse.tracecompass.tmf.core.config.xmlsourcetype'

INANDOUT_CONFIG_SOURCE_TYPE = 'org.eclipse.tracecompass.incubator.internal.inandout.core.config'

# pylint: disable=too-many-public-methods


class TestTspClient:
    """TspClient test methods.

    [1] Each test below has a specific TSP endpoint focus, coming with its minimal assertions kit.
    [2] This means that some asserts only appear in the test that specifically exercises them.
    [3] Asserts for teardown test steps are otherwise repeated to confirm data deletions.
    [4] This is to diagnose potential subsequent test failures caused by uncleaned server data.
    [5] Should data get corrupted by test runs, ./tsp_cli_client can be used to manually clean it.
    [6] Some setup steps are minimized where the test method scope doesn't require more data.
    """

    def _delete_experiments(self):
        """To be called at the end of tests opening experiments, before deleting traces."""
        response = self.tsp_client.fetch_experiments()
        for experiment in response.model.experiments:
            self.tsp_client.delete_experiment(experiment.UUID)
            assert response.status_code == 200

    def _delete_traces(self):
        """To be called at the end of tests opening traces, after deleting experiments."""
        response = self.tsp_client.fetch_traces()
        for trace in response.model.traces:
            # Do not also delete the trace from disk; file part of this repo.
            self.tsp_client.delete_trace(trace.UUID, False)
            assert response.status_code == 200

    # Not a pytest fixture so that VS Code may find its definitions.
    tsp_client = TspClient('http://localhost:8080/tsp/api/')

    name = 'FunctionGraph.xml'

    @pytest.fixture(scope='module')
    def extension(self):
        """Absolute xml analysis file path."""
        return os.path.join(os.getcwd(), 'org.eclipse.tracecompass.incubator', 'tracetypes',
                            'org.eclipse.tracecompass.incubator.ftrace.core', 'xml_analyses', self.name)

    @staticmethod
    @pytest.fixture(scope='module')
    def kernel():
        """Absolute kernel test trace path."""
        return os.path.join(os.getcwd(), 'tracecompass-test-traces', 'ctf', 'src', 'main', 'resources', 'kernel')

    @staticmethod
    @pytest.fixture(scope='module')
    def other():
        """Absolute kernel-vm test trace path."""
        return os.path.join(os.getcwd(), 'tracecompass-test-traces', 'ctf', 'src', 'main', 'resources', 'kernel_vm')

    @staticmethod
    @pytest.fixture(scope='module')
    def switches():
        """Absolute switches test trace path."""
        return os.path.join(os.getcwd(), 'tracecompass-test-traces', 'ctf', 'src', 'main', 'resources', 'context-switches',
                            'context-switches-kernel')

    @staticmethod
    @pytest.fixture(scope='module')
    def ust():
        """Absolute ust test trace path."""
        return os.path.join(os.getcwd(), 'tracecompass-test-traces', 'ctf', 'src', 'main', 'resources', 'context-switches',
                            'context-switches-ust')

    @pytest.fixture(scope="module", autouse=True)
    def test_fetch_traces(self):
        """Check server availability before each test; don't fail all tests if none, but exit."""
        try:
            self.tsp_client.fetch_traces()
        except requests.exceptions.ConnectionError as ex:
            pytest.exit(str(ex))
        # Deleting left-over data here doesn't work consistently, but remains handy if tests fail.
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_with_other_client(self):
        """Expect client without end slash to respond with no traces"""
        tsp_client = TspClient('http://localhost:8080/tsp/api')
        response = tsp_client.fetch_traces()
        assert response.status_code == 200
        assert not response.model.traces

    def test_fetch_traces_none(self):
        """Expect no traces without opening any."""
        response = self.tsp_client.fetch_traces()
        assert response.status_code == 200
        assert not response.model.traces

    def test_open_trace_twice(self, kernel, other):
        """Expect two traces after opening them."""
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        response = self.tsp_client.open_trace(os.path.basename(other), other)
        assert response.status_code == 200

        response = self.tsp_client.fetch_traces()
        assert len(response.model.traces) == 2
        self._delete_traces()

    def test_fetch_opened_trace(self, kernel):
        """Expect trace that was opened."""
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        expected_uuid = response.model.UUID

        response = self.tsp_client.fetch_trace(expected_uuid)
        assert response.status_code == 200
        assert response.model.UUID == expected_uuid
        self._delete_traces()

    def test_opened_trace_deleted(self, kernel):
        """Expect no trace after deletion."""
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        trace_uuid = response.model.UUID

        response = self.tsp_client.delete_trace(trace_uuid, False)
        assert response.status_code == 200

        response = self.tsp_client.fetch_trace(trace_uuid)
        assert response.status_code == 404

    def test_opened_trace_deleted_with_cache(self, kernel):
        """Expect trace deleted while removing cache."""
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        trace_uuid = response.model.UUID

        # Also remove cache for this trace, but still not its file on disk.
        response = self.tsp_client.delete_trace(trace_uuid, False, True)
        assert response.status_code == 200

    def test_fetch_experiments_none(self):
        """Expect no experiments without opening any (nor traces)."""
        response = self.tsp_client.fetch_experiments()
        assert response.status_code == 200
        assert not response.model.experiments

    def test_open_experiment(self, kernel, other):
        """Expect experiment after opening it with traces."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_trace(os.path.basename(other), other)
        traces.append(response.model.UUID)

        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200

        response = self.tsp_client.fetch_experiments()
        assert len(response.model.experiments) == 1
        self._delete_experiments()
        self._delete_traces()

    def test_opened_trace_info(self, kernel, other):
        """Expect the info of the trace correctly set."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)

        # The trace info in read after it is opened in an
        # experiment, so open the experiment here.
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200

        trace = response.model.traces.traces[0]
        assert trace.start == 1332170682440133097
        assert trace.end == 1332170682702071857
        assert trace.path.endswith('/tracecompass-test-traces/ctf/src/main/resources/kernel')
        assert isinstance(trace.properties, dict)
        assert len(trace.properties) == 11
        assert trace.properties["clock_offset"] == '1332166405241713987'
        assert trace.properties["clock_scale"] == '1.0'
        assert trace.properties["domain"] == '"kernel"'
        assert trace.properties["host ID"] == '"84db105b-b3f4-4821-b662-efc51455106a"'
        assert trace.properties['tracer_name'] == '"lttng-modules"'
        assert trace.properties['tracer_major'] == '2'
        assert trace.properties['tracer_minor'] == '0'
        assert trace.properties['kernel_release'] == '"3.0.0-16-generic-pae"'
        assert trace.properties['sysname'] == '"Linux"'
        assert trace.properties['tracer_patchlevel'] == '0'
        assert trace.properties['kernel_version'] == '"#29-Ubuntu SMP Tue Feb 14 13:56:31 UTC 2012"'

        self._delete_experiments()
        self._delete_traces()

    def test_open_experiment_unopened_trace(self, kernel):
        """Expect 204 after opening experiment with unopened trace."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        unopened = str(uuid.uuid4())
        traces.append(unopened)

        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 204

        response = self.tsp_client.fetch_experiments()
        assert len(response.model.experiments) == 0
        self._delete_traces()

    def test_fetch_opened_experiment(self, kernel):
        """Expect experiment that was opened."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        expected_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment(expected_uuid)
        assert response.status_code == 200
        assert response.model.UUID == expected_uuid
        self._delete_experiments()
        self._delete_traces()

    def test_opened_experiment_deleted(self, kernel):
        """Expect no experiment after deletion."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.delete_experiment(experiment_uuid)
        assert response.status_code == 200
        self._delete_traces()

        response = self.tsp_client.fetch_experiment(experiment_uuid)
        assert response.status_code == 404

    def test_fetch_experiment_outputs(self, kernel):
        """Expect some experiment outputs."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        assert response.status_code == 200
        assert len(response.model.descriptors) > 0
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_experiment_output(self, kernel):
        """Expect opened experiment output."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        expected_id = response.model.descriptors[0].id
        response = self.tsp_client.fetch_experiment_output(
            experiment_uuid, expected_id)
        assert response.status_code == 200
        assert response.model.id == expected_id
        self._delete_experiments()
        self._delete_traces()

    def test_open_experiment_context_switches(self, switches, ust):
        """Expect experiment based on context-switches traces."""
        traces = []
        response = self.tsp_client.open_trace(
            os.path.basename(switches), switches)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_trace(os.path.basename(ust), ust)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename("context"), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment(experiment_uuid)
        assert response.status_code == 200
        for trace in response.model.traces.traces:
            response = self.tsp_client.fetch_trace(trace.UUID)
            assert response.status_code == 200

        self._delete_experiments()
        self._delete_traces()

    def test_fetch_data_tree(self, ust):
        """Expect data tree out of opened trace experiment."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(ust), ust)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(ust), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        output_id = STATISTICS_DP_ID
        response = self.tsp_client.fetch_datatree(experiment_uuid, output_id)
        assert response.status_code == 200
        assert response.model.model_type == response.model.model_type.DATA_TREE
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_timegraph_tree(self, kernel):
        """Expect timegraph tree out of opened trace experiment."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        output_id = response.model.descriptors[0].id
        response = self.tsp_client.fetch_timegraph_tree(
            experiment_uuid, output_id)
        assert response.status_code == 200
        assert response.model.model_type == response.model.model_type.TIME_GRAPH_TREE
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_xy_tree(self, kernel):
        """Expect XY tree out of opened trace experiment."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        output_id = response.model.descriptors[0].id
        response = self.tsp_client.fetch_xy_tree(experiment_uuid, output_id)
        assert response.status_code == 200
        assert response.model.model_type == response.model.model_type.XY_TREE
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_xy(self, kernel):
        """Expect XY data out of completed trace experiment."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        output_id = response.model.descriptors[0].id
        status = ResponseStatus.RUNNING
        while status == ResponseStatus.RUNNING:
            time.sleep(1)
            response = self.tsp_client.fetch_xy_tree(
                experiment_uuid, output_id)
            assert response.model is not None
            status = response.model.status

        params = self.__requested_parameters(response)
        response = self.tsp_client.fetch_xy(experiment_uuid, output_id, params)
        assert response.status_code == 200
        assert response.model.model_type == response.model.model_type.XY
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_timegraph_tree_complete(self, kernel):
        """Expect completing timegraph tree."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        output_id = response.model.descriptors[0].id
        status = ResponseStatus.RUNNING
        while status == ResponseStatus.RUNNING:
            time.sleep(1)
            response = self.tsp_client.fetch_timegraph_tree(
                experiment_uuid, output_id)
            assert response.model is not None
            status = response.model.status

        params = self.__requested_parameters(response)
        response = self.tsp_client.fetch_timegraph_tree(
            experiment_uuid, output_id, params)
        assert response.status_code == 200
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_virtual_table_columns(self, ust):
        """Expect virtual table columns out of opened trace experiment."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(ust), ust)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(ust), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        status = ResponseStatus.RUNNING
        while status == ResponseStatus.RUNNING:
            time.sleep(1)
            response = self.tsp_client.fetch_virtual_table_columns(
                exp_uuid=experiment_uuid, output_id=TABLE_DP_ID)
            assert response.model is not None
            status = response.model.status

        output_id = TABLE_DP_ID
        response = self.tsp_client.fetch_virtual_table_columns(exp_uuid=experiment_uuid, output_id=output_id)
        assert response.status_code == 200
        assert response.model.model_type == response.model.model_type.VIRTUAL_TABLE_HEADER
        assert len(response.model.model.columns) > 0
        for column in response.model.model.columns:
            assert column.id is not None
            assert column.name is not None
        
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_virtual_table_lines(self, ust):
        """Expect virtual table out of opened trace experiment."""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(ust), ust)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(ust), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        status = ResponseStatus.RUNNING
        while status == ResponseStatus.RUNNING:
            time.sleep(1)
            response = self.tsp_client.fetch_virtual_table_columns(
                exp_uuid=experiment_uuid, output_id=TABLE_DP_ID)
            assert response.model is not None
            status = response.model.status

        output_id = TABLE_DP_ID
        response = self.tsp_client.fetch_virtual_table_columns(exp_uuid=experiment_uuid, output_id=output_id)
        assert response.status_code == 200
        assert response.model.model_type == response.model.model_type.VIRTUAL_TABLE_HEADER
        assert len(response.model.model.columns) > 0
        for column in response.model.model.columns:
            assert column.id is not None
            assert column.name is not None

        LOW_INDEX = 0
        LINE_COUNT = 10

        params = {
            TspClient.PARAMETERS_KEY: {
                TspClient.REQUESTED_TABLE_LINE_INDEX_KEY: LOW_INDEX,
                TspClient.REQUESTED_TABLE_LINE_COUNT_KEY: LINE_COUNT
            }
        }
        response = self.tsp_client.fetch_virtual_table_lines(exp_uuid=experiment_uuid, output_id=output_id, parameters=params)
        assert response.status_code == 200
        assert response.model.model_type == response.model.model_type.VIRTUAL_TABLE
        assert len(response.model.model.lines) == 10
        for i, line in enumerate(response.model.model.lines):
            assert line.index is not None
            if i == 0:
                assert line.index == LOW_INDEX
            assert line.tags == VirtualTableTag.NO_TAGS

            assert len(line.cells) > 0
            for cell in line.cells:
                assert cell.content is not None
                assert cell.tags == VirtualTableTag.NO_TAGS

    def test_fetch_timegraph_states(self, kernel):
        """Expect having states after tree is complete"""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        output_id = TIMEGRAPH_DP_ID
        status = ResponseStatus.RUNNING
        while status == ResponseStatus.RUNNING:
            time.sleep(1)
            response = self.tsp_client.fetch_timegraph_tree(
                experiment_uuid, output_id)
            assert response.model is not None
            status = response.model.status
        entries = [entry.id for entry in response.model.model.entries if entry.has_row_model]
        params = {
            TspClient.REQUESTED_TIME_RANGE_KEY: {
                TspClient.REQUESTED_TIME_RANGE_NUM_TIMES_KEY: 100,
                TspClient.REQUESTED_TIME_RANGE_START_KEY: REQUESTED_TIME_START,
                TspClient.REQUESTED_TIME_RANGE_END_KEY: REQUESTED_TIME_END
            },
            TspClient.REQUESTED_ITEM_KEY: entries
        }
        response = self.tsp_client.fetch_timegraph_states(
            experiment_uuid, output_id,  { TspClient.PARAMETERS_KEY: params })
        assert response.status_code == 200
        assert len(response.model.model.rows) > 0
        assert len(response.model.model.rows[0].states) != 0
        row = response.model.model.rows[0].states[0]
        assert row.start_time is not None
        assert row.end_time is not None
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_timegraph_arrows(self, kernel):
        """Expect having arrows after tree is complete"""
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        output_id = TIMEGRAPH_DP_ID
        status = ResponseStatus.RUNNING
        while status == ResponseStatus.RUNNING:
            time.sleep(1)
            response = self.tsp_client.fetch_timegraph_tree(
                experiment_uuid, output_id)
            assert response.model is not None
            status = response.model.status

        entries = [entry.id for entry in response.model.model.entries if entry.has_row_model]
        params = {
            TspClient.REQUESTED_TIME_RANGE_KEY: {
                TspClient.REQUESTED_TIME_RANGE_NUM_TIMES_KEY: 5000,
                TspClient.REQUESTED_TIME_RANGE_START_KEY: REQUESTED_TIME_START,
                TspClient.REQUESTED_TIME_RANGE_END_KEY: REQUESTED_TIME_END
            },
            TspClient.REQUESTED_ITEM_KEY: entries
        }
        response = self.tsp_client.fetch_timegraph_arrows(
            experiment_uuid, output_id, { TspClient.PARAMETERS_KEY: params })
        assert response.status_code == 200
        assert len(response.model.model) != 0
        arrow = response.model.model[0]
        assert arrow.source_id is not None
        assert arrow.target_id is not None
        if arrow.start is None or arrow.end is None:
            assert arrow.duration
        else:
            assert arrow.start is not None
            assert arrow.end is not None
        assert arrow.style is not None
        self._delete_experiments()
        self._delete_traces()

    def test_fetch_configuration_sources(self):
        """Expect at least configuration source ."""
        response = self.tsp_client.fetch_configuration_sources()
        assert response.status_code == 200
        assert response.model.configuration_source_set

        response = self.tsp_client.fetch_configuration_source(CONFIG_SOURCE_TYPE)
        assert response.status_code == 200
        assert response.model

        assert response.model.parameter_descriptors != None
        assert response.model.schema == None

    def test_fetch_configurations_none(self):
        """Expect no configurations without posting any."""
        response = self.tsp_client.fetch_configurations(CONFIG_SOURCE_TYPE)
        assert response.status_code == 200
        assert isinstance(response.model.configuration_set, list)

        response = self.tsp_client.fetch_configuration(CONFIG_SOURCE_TYPE, self.name)
        assert response.status_code == 404

    def test_post_configuration(self, extension):
        """Expect configuration after posting it."""
        params = {}
        params['path'] = extension
        response = self.tsp_client.post_configuration(CONFIG_SOURCE_TYPE, params)
        assert response.status_code == 200

        response = self.tsp_client.fetch_configurations(CONFIG_SOURCE_TYPE)
        assert len(response.model.configuration_set) > 0
        found = False
        for config in response.model.configuration_set:
            if config.id == self.name:
                found = True
        assert found

        response = self.tsp_client.fetch_configuration(CONFIG_SOURCE_TYPE, self.name)
        assert response.status_code == 200
        assert response.model
        assert response.model.id == self.name

        response = self.tsp_client.delete_configuration(CONFIG_SOURCE_TYPE, self.name)
        assert response.status_code == 200
        assert response.model
        assert response.model.id == self.name

    def test_posted_configuration_deleted(self, extension):
        """Expect no configuration after deletion."""
        params = {}
        params['path'] = extension
        self.tsp_client.post_configuration(CONFIG_SOURCE_TYPE, params)
        response = self.tsp_client.delete_configuration(CONFIG_SOURCE_TYPE, self.name)
        assert response.status_code == 200

        response = self.tsp_client.fetch_configurations(CONFIG_SOURCE_TYPE)
        assert isinstance(response.model.configuration_set, list)

    def test_put_configuration(self, extension):
        """Expect successful update of configuartion."""
        params = {}
        params['path'] = extension
        self.tsp_client.post_configuration(CONFIG_SOURCE_TYPE, params)

        response = self.tsp_client.put_configuration(CONFIG_SOURCE_TYPE, self.name, params)
        assert response.status_code == 200
        assert response.model
        assert response.model.id == self.name

        self.tsp_client.delete_configuration(CONFIG_SOURCE_TYPE, self.name)

    def test_fetch_output_configuration_sources(self, kernel):
        """Expect at least one configuration source ."""

        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.fetch_output_configuration_sources(experiment_uuid, INANDOUT_DP_ID)
        assert response.status_code == 200
        assert isinstance(response.model, ConfigurationSourceSet)
        assert response.model.configuration_source_set
        assert len(response.model.configuration_source_set) > 0

        response = self.tsp_client.fetch_output_configuration_source(experiment_uuid, INANDOUT_DP_ID, INANDOUT_CONFIG_SOURCE_TYPE)
        assert response.status_code == 200
        assert response.model
        assert isinstance(response.model, ConfigurationSource)

        assert response.model.schema != None

    def test_create_delete_derived_output(self, kernel):
        """Expect a data provider descriptor after creating it."""

        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        params = {
            "name": "My new InAndOut",
            "description": "My special configuration",
            "sourceTypeId": "org.eclipse.tracecompass.incubator.internal.inandout.core.config",
            "parameters": {
                "specifiers": [{
                    "label": "latency",
                    "inRegex": "(\\S*)_entry",
                    "outRegex": "(\\S*)_exit",
                    "contextInRegex": "(\\S*)_entry",
                    "contextOutRegex": "(\\S*)_exit",
                    "classifier": "CPU"
                }]
            }
        }
        
        response = self.tsp_client.create_derived_output(experiment_uuid, INANDOUT_DP_ID, params)
        assert response.status_code == 200
        assert response.model
        assert isinstance(response.model, OutputDescriptor)
        assert response.model.parent_id == INANDOUT_DP_ID

        derived_id = response.model.id

        response = self.tsp_client.fetch_experiment_outputs(experiment_uuid)
        assert response.status_code == 200
        assert response.model
        assert len(response.model.descriptors) > 0
        assert [desc for desc in response.model.descriptors if desc.id == derived_id]

        response = self.tsp_client.fetch_experiment_output(
            experiment_uuid, derived_id)
        assert response.status_code == 200
        assert response.model.id == derived_id

        response = self.tsp_client.delete_derived_output(experiment_uuid, INANDOUT_DP_ID, derived_id)
        assert response.status_code == 200
        assert response.model
        assert isinstance(response.model, OutputDescriptor)

    def test_fetch_health(self):
        """Expect a successful health response"""
        response = self.tsp_client.fetch_health()
        assert response.status_code == 200
        assert response.model
        assert response.model.status == HealthStatus.UP

    def test_fetch_identifier(self):
        """Expect a successful identifier response"""
        response = self.tsp_client.fetch_identifier()
        assert response.status_code == 200
        assert response.model
        assert response.model.server_version
        # optional field build_time
        if response.model.build_time is not None:
            assert response.model.build_time
        assert response.model.os_name
        assert response.model.os_arch
        assert response.model.os_version
        assert response.model.cpu_count
        assert response.model.max_memory
        assert response.model.product_id
        assert response.model.tsp_version

    @staticmethod
    def __requested_parameters(response):
        parameters = {}
        requested_items = []
        for entry in response.model.model.entries:
            requested_items.append(entry.id)
        parameters[TspClient.REQUESTED_ITEM_KEY] = requested_items

        requested_times = []
        requested_time = REQUESTED_TIME_START
        while len(requested_times) < REQUESTED_TIME_LENGTH:
            requested_time += REQUESTED_TIME_STEP
            requested_times.append(int(requested_time))
        parameters[TspClient.REQUESTED_TIME_KEY] = requested_times
        return {TspClient.PARAMETERS_KEY: parameters}
