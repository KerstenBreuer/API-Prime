# Copyright 2021 - 2022 Kersten Henrik Breuer (kersten-breuer@outlook.com)
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
from typing import NamedTuple, Optional

import openapi_core
import yaml


class RouteInfo(NamedTuple):
    """A container for information on a route"""

    path: str
    method: str


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
            self.content = yaml.safe_load(spec_file)

        self.openapi_core_spec = openapi_core.create_spec(self.content)

    def get_route_by_id(self, operation_id: str) -> Optional[RouteInfo]:
        """
        Get route infos by specifying the operation ID.
        Returns None if no route with specified ID is found."""

        for path, methods_dict in self.content["paths"].items():
            for method, route in methods_dict.items():
                if "operationId" in route and route["operationId"] == operation_id:
                    return RouteInfo(path=path, method=method)

        return None
