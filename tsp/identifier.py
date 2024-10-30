# The MIT License (MIT)
#
# Copyright (C) 2024 - Ericsson
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

"""Identifier Service Class"""

SERVER_VERSION = "version"
BUILD_TIME = "buildTime"
OS_NAME = "os"
OS_ARCH = "osArch"
OS_VERSION = "osVersion"
CPU_COUNT = "cpuCount"
MAX_MEMORY = "maxMemory"
LAUNCHER_NAME = "launcherName"
PRODUCT_ID = "productId"
TSP_VERSION = "tspVersion"


class Identifier:
    '''
    Model of the Identifier Service. This is a Service used to identify important information
    regarding the trace server and the system it is running on.
    '''
    def __init__(self, params):
        '''
        Constructor
        '''

        # Server Version
        if SERVER_VERSION in params:
            self.server_version = params.get(SERVER_VERSION)
            del params[SERVER_VERSION]
        else:
            self.server_version = None

        # Build Time
        if BUILD_TIME in params:
            self.build_time = params.get(BUILD_TIME)
            del params[BUILD_TIME]
        else:
            self.build_time = None

        # OS Name
        if OS_NAME in params:
            self.os_name = params.get(OS_NAME)
            del params[OS_NAME]
        else:
            self.os_name = None

        # OS Arch
        if OS_ARCH in params:
            self.os_arch = params.get(OS_ARCH)
            del params[OS_ARCH]
        else:
            self.os_arch = None

        # OS Version
        if OS_VERSION in params:
            self.os_version = params.get(OS_VERSION)
            del params[OS_VERSION]
        else:
            self.os_version = None

        # CPU Count
        if CPU_COUNT in params:
            self.cpu_count = params.get(CPU_COUNT)
            del params[CPU_COUNT]
        else:
            self.cpu_count = None

        # Max Memory
        if MAX_MEMORY in params:
            self.max_memory = params.get(MAX_MEMORY)
            del params[MAX_MEMORY]
        else:
            self.max_memory = None

        # Product ID
        if PRODUCT_ID in params:
            self.product_id = params.get(PRODUCT_ID)
            del params[PRODUCT_ID]
        else:
            self.product_id = None

        # Launcher Name
        if LAUNCHER_NAME in params:
            self.launcher_name = params.get(LAUNCHER_NAME)
            del params[LAUNCHER_NAME]
        else:
            self.launcher_name = None

        # TSP Version
        if TSP_VERSION in params:
            self.tsp_version = params.get(TSP_VERSION)
        else:
            self.tsp_version = None

    def to_string(self):
        '''
        to_string method
        '''
        return f"Identifier[version={self.server_version}, buildTime={self.build_time}, os={self.os_name}, osArch={self.os_arch}, osVersion={self.os_version}, cpuCount={self.cpu_count}, maxMemory={self.max_memory}, productId={self.product_id}, launcherName={self.launcher_name}, tspVersion={self.tsp_version}]"
