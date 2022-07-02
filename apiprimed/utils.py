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

"""A collection of general utilites."""

from enum import Enum
from typing import Optional, Union, overload

from apiprimed.exceptions import InvalidHttpMethodError, RouteIdentificationError


class HttpMethod(Enum):
    """An enum of HTTP methods supported by OpenAPI."""

    GET = "get"
    HEAD = "head"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    OPTIONS = "options"
    TRACE = "trace"
    PATCH = "patch"


def cast_http_method(method: Union[str, HttpMethod]):
    """Try to cast the provided method into an HttpMethod.

    Args:
        method: A string or enum representation of an HTTP method.

    Returns:
        A corresponding value from the HttpMethod enum.

    Raises:
        InvalidHttpMethodError: If validation fails.
    """

    if isinstance(method, HttpMethod):
        return method

    method_str = method.lower()

    for http_method in HttpMethod:
        if http_method.value == method_str:
            return http_method

    raise InvalidHttpMethodError(
        method_str=method_str,
        expected_values=[http_method.value for http_method in HttpMethod],
    )


@overload
def generate_route_id(*, operation_id: str) -> str:
    ...


@overload
def generate_route_id(*, path: str, method: Union[str, HttpMethod]) -> str:
    ...


def generate_route_id(
    *,
    operation_id: Optional[str] = None,
    path: Optional[str] = None,
    method: Optional[Union[str, HttpMethod]] = None,
) -> str:
    """Generates a unique route identifier. If provided the operation_id is used
    otherwise the ID is derived from a combination of the path and the method.

    Args:
        operation_id: An operationId as per the OpenAPI spec.
        path: The path of the route as per the OpenAPI spec.
        method: The HTTP method used on that route.

    Returns:
        A unique identifier for that route.
    """

    if operation_id is not None:
        return operation_id

    if path is None or method is None:
        raise RouteIdentificationError()

    method_casted = cast_http_method(method)

    # format the path to look more like an ID:
    path_id = path.replace("/", ".").replace("{", "").replace("}", "").lower()

    return f"{method_casted.value}.{path_id}"
