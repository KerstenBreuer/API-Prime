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

"""Contains router class that is used to register route functions."""

from pathlib import Path
from typing import Callable, Mapping, Optional, Union, overload

from apiprimed.routes import OpenApiRoute
from apiprimed.spec import OpenApiSpec


class OpenApiRouter:
    """Collects and verifies route functions for a given OpenAPI spec.
    Can be used to emit starlette-compatible Route objects to be registered to
    a starlette app.
    """

    def __init__(self, *, spec: Union[Path, OpenApiSpec]) -> None:
        """
        Initialize application instance.
        """

        self.spec = spec if isinstance(spec, OpenApiSpec) else OpenApiSpec(spec)

        # Initialize the route registry that uses a unique route id (operationId or
        # derived from a combination of path and method) as keys an OpenApiRoute
        # instances as values:
        self._registry: Mapping[str, OpenApiRoute] = {}

    @overload
    def add_route(
        self, endpoint: Callable, *, operation_id: str, path: None, method: None
    ) -> None:
        ...

    @overload
    def add_route(
        self, endpoint: Callable, *, operation_id: None, path: str, method: str
    ) -> None:
        ...

    def add_route(
        self,
        endpoint: Callable,
        *,
        operation_id: Optional[str] = None,
        path: Optional[str] = None,
        method: Optional[str] = None
    ) -> None:
        """Create a route"""

        route = OpenApiRoute(
            endpoint=endpoint,
            spec=self.spec,
            operation_id=operation_id,
            path=path,
            method=method,
        )

        print(route)
