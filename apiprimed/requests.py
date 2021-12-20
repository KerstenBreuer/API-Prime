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

"""Request conversion (from Starlette to target format) and spec-based validation."""

from typing import List

from werkzeug.datastructures import Headers
from starlette.requests import Request as StarletteRequest
from openapi_core.validation.request.datatypes import (
    OpenAPIRequest as OacRequest,
    RequestParameters as OacRequestParameters,
)
from openapi_core.validation.request.validators import (
    RequestValidator,
    RequestValidationResult,
)


from apiprimed.api_spec import OpenApiSpec


class Request:
    """Class containing a request data validated against the OpenAPI spec."""

    def __init__(
        self, star_request: StarletteRequest, validation_result: RequestValidationResult
    ):
        """Initialize class with the original starlette request and the request data
        validated by openapi_core."""

        # original starlette request can still be accessed if needed:
        self.starlette = star_request

        # validated data:
        self.query_params: dict[str, object] = validation_result.parameters.query
        self.path_params: dict[str, object] = validation_result.parameters.path
        self.headers: Headers = validation_result.parameters.header
        self.body: dict[str, object] = validation_result.body
        self.cookies: dict[str, object] = validation_result.parameters.cookie

        self.errors: List[Exception] = validation_result.errors


async def starlette_to_openapi_request(
    star_request: StarletteRequest,
) -> OacRequest:
    """Converts a starlette Request object to a OpenApiRequest object
    from the openapi_core library."""

    werkzeug_headers = Headers()
    werkzeug_headers.extend(**star_request.headers)

    request_params = OacRequestParameters(
        query=star_request.query_params,
        header=werkzeug_headers,
        path=star_request.path_params,
        cookie=star_request.cookies,
    )

    return OacRequest(
        full_url_pattern=str(star_request.url),
        method=star_request.method.lower(),
        parameters=request_params,
        body=await star_request.body(),
        mimetype=star_request.headers["content-type"],
    )


async def validate_request(
    star_request: StarletteRequest, spec: OpenApiSpec, raise_on_error: bool = True
) -> RequestValidationResult:
    """Validate a starlette request"""
    oac_request = await starlette_to_openapi_request(star_request)
    validator = RequestValidator(spec.openapi_core_spec)

    # result contains casted query, header, body, and path params:
    #   - converts to right type
    #   - adds defaults if not specified
    validation_result = validator.validate(oac_request)

    if raise_on_error:
        validation_result.raise_for_errors()

    return validation_result
