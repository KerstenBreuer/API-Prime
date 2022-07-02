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

"""Request conversion (from Starlette to target format) and spec-based validation."""

from typing import Dict

import starlette.requests
from openapi_core.validation.request.datatypes import OpenAPIRequest
from openapi_core.validation.request.datatypes import (
    RequestParameters as OpenAPIRequestParameters,
)
from openapi_core.validation.request.validators import RequestValidator
from pydantic import BaseModel
from werkzeug.datastructures import Headers

from apiprimed.api_spec import OpenApiSpec


class ValidatedRequest(BaseModel):
    """Class containing a request data validated against the OpenAPI spec."""

    query_params: Dict[str, object]
    path_params: Dict[str, object]
    headers: Headers
    body: Dict[str, object]
    cookies: Dict[str, object]
    oac_request: OpenAPIRequest

    class Config:
        "pydantic config"
        arbitrary_types_allowed = True


async def starlette_to_openapi_request(
    starlette_request: starlette.requests.Request,
) -> OpenAPIRequest:
    """Converts a starlette Request object to a OpenApiRequest object
    from the openapi_core library."""

    werkzeug_headers = Headers()
    werkzeug_headers.extend(**starlette_request.headers)

    request_params = OpenAPIRequestParameters(
        query=starlette_request.query_params,
        header=werkzeug_headers,
        path=starlette_request.path_params,
        cookie=starlette_request.cookies,
    )

    return OpenAPIRequest(
        full_url_pattern=str(starlette_request.url),
        method=starlette_request.method.lower(),
        parameters=request_params,
        body=await starlette_request.body(),
        mimetype=starlette_request.headers["content-type"],
    )


async def validate_request(
    starlette_request: starlette.requests.Request,
    *,
    spec: OpenApiSpec,
) -> ValidatedRequest:
    """Validate a starlette request"""
    oac_request = await starlette_to_openapi_request(starlette_request)
    validator = RequestValidator(spec.openapi_core_spec)

    # result contains casted query, header, body, and path params:
    #   - converts to right type
    #   - adds defaults if not specified
    validation_result = validator.validate(oac_request)

    validation_result.raise_for_errors()

    return ValidatedRequest(
        query_params=validation_result.parameters.query,
        path_params=validation_result.parameters.path,
        headers=validation_result.parameters.header,
        body=validation_result.body,
        cookies=validation_result.parameters.cookie,
        oac_request=oac_request,
    )
