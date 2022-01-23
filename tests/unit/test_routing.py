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

"""Test routing module."""

from typing import Optional
import pytest

from apiprimed.routing import OpenApiRoute
from apiprimed.exceptions import RoutingError

from .fixtures.specs import EXAMPLE_SPEC
from .fixtures.routes import greet_route
from .fixtures.utils import null_context_manager


@pytest.mark.parametrize(
    "operation_id,path,method,expected_exception",
    [
        ("greetPost", None, None, None),
        (None, "/greet/{lang}", "post", None),
        (None, None, None, RoutingError),
        ("my_wrong_id", None, None, RoutingError),
    ],
)
def test_openapiroute(
    operation_id: Optional[str],
    path: Optional[str],
    method: Optional[str],
    expected_exception: Optional[Exception],
):
    """Test the `OpenApiRoute` class."""

    spec = EXAMPLE_SPEC["spec"]

    cm = (
        null_context_manager()
        if expected_exception is None
        else pytest.raises(expected_exception)
    )
    with cm:
        OpenApiRoute(
            greet_route,
            spec=spec,
            operation_id=operation_id,
            path=path,
            method=method,
        )
