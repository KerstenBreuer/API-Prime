from typing import Type

import yaml
import uvicorn

import werkzeug.datastructures
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import Response, JSONResponse

from openapi_core.validation.request.datatypes import OpenAPIRequest, RequestParameters
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.datatypes import OpenAPIResponse
from openapi_core.validation.response.validators import ResponseValidator
from openapi_core import create_spec


def get_openapi_spec():
    with open("./experiments/openapi.yaml", "r") as spec_file:
        spec_dict = yaml.safe_load(spec_file)

    spec = create_spec(spec_dict)

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
