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

from contextlib import nullcontext
from typing import Optional, Type

import pytest

from apiprimed.exceptions import RoutingError
from apiprimed.routes import OpenApiRoute

from .fixtures.routes import greet_route
from .fixtures.specs import EXAMPLE_SPEC


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
    expected_exception: Optional[Type[Exception]],
):
    """Test the `OpenApiRoute` class."""

    spec = EXAMPLE_SPEC.spec

    with pytest.raises(expected_exception) if expected_exception else nullcontext():  # type: ignore
        OpenApiRoute(
            greet_route,
            spec=spec,
            operation_id=operation_id,
            path=path,
            method=method,
        )
