# Copyright 2021 Kersten Henrik Breuer (kersten-breuer@outlook.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains functionalites for handling OpenAPI3 specification"""

from pathlib import Path

import yaml
import openapi_core


class OpenApiSpec:
    """A class for holding data and functionality for interacting
    with OpenAPI3-based specification."""

    def __init__(self, spec_path: Path):
        """Initialize an OpenApiSpec instance.

        Args:
            spec_path (Path): Path to the spec as JSON or YAML file.
        """

        self.spec_path = spec_path

        with open(self.spec_path, "r", encoding="utf8") as spec_file:
            self.spec_dict = yaml.safe_load(spec_file)

        self._openapi_core_spec = openapi_core.create_spec(self.spec_dict)
