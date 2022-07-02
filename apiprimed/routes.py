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

"""Extends the routing functionality of Starlette."""

from typing import Callable, Optional

import starlette.requests
import starlette.routing

from apiprimed.exceptions import RoutingError
from apiprimed.requests import ValidatedRequest, validate_request
from apiprimed.spec import OpenApiSpec


def endpoint_wrapper_factory(
    endpoint: Callable[[ValidatedRequest], object],
    spec: OpenApiSpec,
) -> Callable[[starlette.requests.Request], object]:
    """A for wrapper functions that adds OpenAPI-based validation to the endpoint
    function."""

    async def endpoint_wrapper(starlette_request: starlette.requests.Request):
        """The wrapper for the endpoint function."""

        validated_request = await validate_request(
            starlette_request,
            spec=spec,
        )

        # call original endpoint function:
        return endpoint(validated_request)

    return endpoint_wrapper


class OpenApiRoute(starlette.routing.Route):
    """Adds OpenAPI-based svalidation to the starlette Route class."""

    def __init__(
        self,
        endpoint: Callable[[ValidatedRequest], object],
        *,
        spec: OpenApiSpec,
        operation_id: Optional[str] = None,
        path: Optional[str] = None,
        method: Optional[str] = None,
    ):
        """
        Intit route.
        Either provide an `operation_id` or `path` plus `method`.
        """
        if operation_id is not None:
            route_info = spec.get_route_info(operation_id=operation_id)
            if route_info is None:
                raise RoutingError(
                    f"No endpoint found with operation ID '{operation_id}'."
                )
            path_, method_ = route_info
        elif path is not None and method is not None:
            try:
                _ = spec.content["paths"][path][method]
            except KeyError as error:
                raise RoutingError("Path does not exist.") from error
            path_ = path
            method_ = method
        else:
            raise RoutingError(
                "Please provide either an `operation_id` or `path` plus"
                + " `method` plus `name`"
            )

        wrapped_endpoint = endpoint_wrapper_factory(endpoint, spec=spec)

        super().__init__(
            path=path_,
            endpoint=wrapped_endpoint,
            methods=[method_],
            include_in_schema=False,
        )

        self.spec = spec
        self.operation_id = operation_id
