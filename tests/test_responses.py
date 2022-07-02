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

"""Tests the `responses` module."""

from contextlib import nullcontext

import pytest
import starlette.responses
from openapi_core.exceptions import OpenAPIError
from openapi_core.validation.response.datatypes import OpenAPIResponse

from apiprimed.api_spec import OpenApiSpec
from apiprimed.requests import validate_request
from apiprimed.responses import starlette_to_openapi_response, validate_response

from .fixtures.specs import EXAMPLE_SPEC
from .fixtures.starlette import (
    INVALID_STARLETTE_RESPONSE,
    VALID_STARLETTE_REQUEST,
    VALID_STARLETTE_RESPONSE,
)


@pytest.mark.asyncio
async def test_starlette_to_openapi_response():
    """Test the `starlette_to_openapi_response` conversion function."""
    starlette_response = VALID_STARLETTE_RESPONSE

    openapi_response = await starlette_to_openapi_response(starlette_response)

    assert isinstance(openapi_response, OpenAPIResponse)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "star_response,expect_error",
    [
        (VALID_STARLETTE_RESPONSE, False),
        (INVALID_STARLETTE_RESPONSE, True),
    ],
)
async def test_validate_response(
    star_response: starlette.responses.Response, expect_error: bool
):
    """Test the "validate_response" function."""
    spec = OpenApiSpec(spec_path=EXAMPLE_SPEC.json_path)
    request = await validate_request(VALID_STARLETTE_REQUEST, spec=spec)  # type: ignore

    with pytest.raises(OpenAPIError) if expect_error else nullcontext():  # type: ignore
        await validate_response(
            starlette_response=star_response, request=request, spec=spec
        )
