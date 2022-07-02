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

import uvicorn
import werkzeug.datastructures
import yaml
from openapi_core import create_spec
from openapi_core.validation.request.datatypes import OpenAPIRequest, RequestParameters
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.datatypes import OpenAPIResponse
from openapi_core.validation.response.validators import ResponseValidator
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route


def get_openapi_spec():
    with open("./experiments/openapi.yaml") as spec_file:
        content = yaml.safe_load(spec_file)

    spec = create_spec(content)

    return spec


async def starlette_request_to_openapi_request(
    star_request: Request,
) -> OpenAPIRequest:
    """Converts a starlette Request object to a OpenApiRequest object
    from the openapi_core library."""

    werkzeug_headers = werkzeug.datastructures.Headers()
    werkzeug_headers.extend(**star_request.headers)

    request_params = RequestParameters(
        query=star_request.query_params,
        header=werkzeug_headers,
        path=star_request.path_params,
        cookie=star_request.cookies,
    )

    return OpenAPIRequest(
        full_url_pattern=str(star_request.url),
        method=star_request.method.lower(),
        parameters=request_params,
        body=await star_request.body(),
        mimetype=star_request.headers["content-type"],
    )


def starlette_response_to_openapi_response(star_response: Response) -> OpenAPIResponse:
    """Converts a starlette Response object to a OpenApiResponse object
    from the openapi_core library."""

    return OpenAPIResponse(
        data=star_response.body,
        status_code=star_response.status_code,
        mimetype=star_response.media_type,
    )


async def greet(request: Request):
    spec = get_openapi_spec()

    # validate request:
    openapi_request = await starlette_request_to_openapi_request(request)
    request_validator = RequestValidator(spec)
    request_validation_result = request_validator.validate(openapi_request)
    # result contains casted query, header, body, and path params:
    #   - converts to right type
    #   - adds defaults if not specified
    request_validation_result.raise_for_errors()

    # generate response:
    response = JSONResponse({"message": "Hello world!"})

    # validate response:
    openapi_response = starlette_response_to_openapi_response(response)
    response_validator = ResponseValidator(spec)
    response_validation_result = response_validator.validate(
        openapi_request, openapi_response
    )
    response_validation_result.raise_for_errors()

    return response


routes = [
    Route("/api/v1/greet/{lang}", greet, methods=["POST"]),
]


app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
