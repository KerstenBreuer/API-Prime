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

"""Response conversion (from source format to Starlette) and spec-based validation."""

from copy import deepcopy
import json

import starlette.responses
import starlette.requests
from openapi_core.validation.response.datatypes import OpenAPIResponse
from openapi_core.validation.response.validators import ResponseValidator


from apiprimed.api_spec import OpenApiSpec
from apiprimed.requests import ValidatedRequest


async def starlette_to_openapi_response(
    starlette_response: starlette.responses.Response,
) -> OpenAPIResponse:
    """Converts a startlette response into an OpenAPIResponse object."""

    return OpenAPIResponse(
        data=starlette_response.body,
        status_code=starlette_response.status_code,
        mimetype=starlette_response.media_type,
    )


async def validate_response(
    starlette_response: starlette.responses.Response,
    *,
    request: ValidatedRequest,
    spec: OpenApiSpec,
) -> starlette.responses.Response:
    """Validate a starlette response."""
    oac_response = await starlette_to_openapi_response(starlette_response)
    validator = ResponseValidator(spec.openapi_core_spec)

    # result contains casted query, header, body, and path params:
    #   - converts to right type
    #   - adds defaults if not specified
    validation_result = validator.validate(
        request=request.oac_request,  # pylint: disable=protected-access
        response=oac_response,
    )

    validation_result.raise_for_errors()

    # Insert the validated and casted response into a copy of the original
    # starlette request:
    casted_response = deepcopy(starlette_response)
    casted_response.body = json.dumps(validation_result.data).encode("utf-8")

    return casted_response
