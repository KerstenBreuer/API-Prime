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

"""Exceptions used in library."""

from typing import Sequence


class ApiPrimedError(Exception):
    """A generic base error. All Error custom errors thrown by the library do inherit
    from this base."""


class RoutingError(ApiPrimedError):
    """Thrown when an error occurs during routing. E.g. the specified operation id
    was not found in the spec."""


class RouteIdentificationError(ValueError, ApiPrimedError):
    """Thrown when providing not enough information to identify a route."""

    def __init__(self):
        """Initialize with a suitable message."""

        message = (
            "Route could not be identified. You must either provide the `operation_id`"
            + " or a combination of `path` or `method`"
        )
        super().__init__(message)


class InvalidHttpMethodError(ValueError, ApiPrimedError):
    """Thrown when providing an str that does not correspond to a supported HTTP
    Method."""

    def __init__(self, *, method_str: str, expected_values: Sequence[str]):
        """Initialize with a message based on the invalid method string."""

        message = (
            f"The provided string ('{method_str}') did not correspond to an HTTP method"
            + " supported by OpenAPI. Expected one of:"
            + ",".join(expected_values)
        )
        super().__init__(message)
