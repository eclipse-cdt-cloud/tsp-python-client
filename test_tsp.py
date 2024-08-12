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

STATISTICS_DP_ID = (
    "org.eclipse.tracecompass.analysis.timing.core.segmentstore.SegmentStoreStatisticsDataProvider:"
    "org.eclipse.linuxtools.lttng2.ust.analysis.callstack"
)
TABLE_DP_ID = (
    "org.eclipse.tracecompass.analysis.timing.core.segmentstore.SegmentStoreTableDataProvider:"
    "org.eclipse.linuxtools.lttng2.ust.analysis.callstack"
)

REQUESTED_TIME_START = 1332170682440133097
REQUESTED_TIME_END = 1332170692664579801
REQUESTED_TIME_LENGTH = 10
REQUESTED_TIME_STEP = (REQUESTED_TIME_END -
                       REQUESTED_TIME_START) / REQUESTED_TIME_LENGTH


CONFIG_SOURCE_TYPE = 'org.eclipse.tracecompass.tmf.core.config.xmlsourcetype'

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
        status = ResponseStatus.RUNNING.name
        while status == ResponseStatus.RUNNING.name:
            time.sleep(1)
            response = self.tsp_client.fetch_xy_tree(
                experiment_uuid, output_id)
            assert response.model is not None
            status = response.model.status.upper()

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
        status = ResponseStatus.RUNNING.name
        while status == ResponseStatus.RUNNING.name:
            time.sleep(1)
            response = self.tsp_client.fetch_timegraph_tree(
                experiment_uuid, output_id)
            assert response.model is not None
            status = response.model.status.upper()

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

        status = ResponseStatus.RUNNING.name
        while status == ResponseStatus.RUNNING.name:
            time.sleep(1)
            response = self.tsp_client.fetch_virtual_table_columns(
                exp_uuid=experiment_uuid, output_id=TABLE_DP_ID)
            assert response.model is not None
            status = response.model.status.upper()

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

        status = ResponseStatus.RUNNING.name
        while status == ResponseStatus.RUNNING.name:
            time.sleep(1)
            response = self.tsp_client.fetch_virtual_table_columns(
                exp_uuid=experiment_uuid, output_id=TABLE_DP_ID)
            assert response.model is not None
            status = response.model.status.upper()

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

            assert len(line.cells) > 0
            for cell in line.cells:
                assert cell.content is not None

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
