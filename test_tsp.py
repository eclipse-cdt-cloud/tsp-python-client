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

from tsp.tsp_client import TspClient
import os
import pytest


class TestTspClient:
    """TspClient test methods.

    [1] Each test below has a specific TSP endpoint focus, coming with its minimal assertions kit.
    [2] This means that some asserts only appear in the test that specifically exercises them.
    [3] Asserts for teardown test steps are otherwise repeated to confirm data deletions.
    [4] This is to diagnose potential subsequent test failures caused by uncleaned server data.
    [5] Should data get corrupted by test runs, ./tsp-cli-client can be used to manually clean it.
    [6] Some setup steps are minimized where the test method scope doesn't require more data.
    """

    # Not a pytest fixture so that VS Code may find its definitions.
    tsp_client = TspClient('http://localhost:8080/tsp/api/')

    @pytest.fixture(scope='module')
    def kernel(self):
        return f'{os.getcwd()}/tracecompass-test-traces/ctf/src/main/resources/kernel'

    @pytest.fixture(scope='module')
    def other(self):
        return f'{os.getcwd()}/tracecompass-test-traces/ctf/src/main/resources/kernel_vm'

    def test_fetch_traces_none(self):
        response = self.tsp_client.fetch_traces()
        assert response.status_code == 200
        assert not response.model.traces

    def test_open_trace_twice_then_delete(self, kernel, other):
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        response = self.tsp_client.open_trace(os.path.basename(other), other)
        assert response.status_code == 200

        response = self.tsp_client.fetch_traces()
        assert len(response.model.traces) == 2
        # Delete each previously opened trace to clean server for next run.
        for trace in response.model.traces:
            # Do not also delete the trace from disk; file part of this repo.
            response = self.tsp_client.delete_trace(trace.UUID, False)
            assert response.status_code == 200

    def test_fetch_opened_trace_then_delete(self, kernel):
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        expected_uuid = response.model.UUID

        response = self.tsp_client.fetch_trace(expected_uuid)
        assert response.status_code == 200
        assert response.model.UUID == expected_uuid

        response = self.tsp_client.delete_trace(expected_uuid, False)
        assert response.status_code == 200

    def test_opened_trace_deleted(self, kernel):
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        trace_uuid = response.model.UUID

        response = self.tsp_client.delete_trace(trace_uuid, False)
        assert response.status_code == 200

        response = self.tsp_client.fetch_trace(trace_uuid)
        assert response.status_code == 404

    def test_opened_trace_deleted_with_cache(self, kernel):
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        assert response.status_code == 200
        trace_uuid = response.model.UUID

        # Also remove cache for this trace, but still not its file on disk.
        response = self.tsp_client.delete_trace(trace_uuid, False, True)
        assert response.status_code == 200

    def test_fetch_experiments_none(self):
        response = self.tsp_client.fetch_experiments()
        assert response.status_code == 200
        assert not response.model.experiments

    def test_open_experiment_then_delete(self, kernel, other):
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
        experiment_uuid = response.model.experiments[0].UUID

        response = self.tsp_client.delete_experiment(experiment_uuid)
        assert response.status_code == 200
        response = self.tsp_client.fetch_traces()
        for trace in response.model.traces:
            response = self.tsp_client.delete_trace(trace.UUID, False)
            assert response.status_code == 200

    def test_fetch_opened_experiment_then_delete(self, kernel):
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

        response = self.tsp_client.delete_experiment(expected_uuid)
        assert response.status_code == 200
        response = self.tsp_client.delete_trace(traces[0], False)
        assert response.status_code == 200

    def test_opened_experiment_deleted(self, kernel):
        traces = []
        response = self.tsp_client.open_trace(os.path.basename(kernel), kernel)
        traces.append(response.model.UUID)
        response = self.tsp_client.open_experiment(
            os.path.basename(kernel), traces)
        assert response.status_code == 200
        experiment_uuid = response.model.UUID

        response = self.tsp_client.delete_experiment(experiment_uuid)
        assert response.status_code == 200
        response = self.tsp_client.delete_trace(traces[0], False)
        assert response.status_code == 200
        response = self.tsp_client.fetch_experiment(experiment_uuid)
        assert response.status_code == 404
