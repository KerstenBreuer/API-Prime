from typing import Type

import yaml
import uvicorn

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import Response, JSONResponse

from openapi_core.validation.request.datatypes import OpenAPIRequest
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.datatypes import OpenAPIResponse
from openapi_core.validation.response.validators import ResponseValidator
from openapi_core import create_spec


def get_openapi_spec():
    with open('./openapi.yaml', 'r') as spec_file:
        spec_dict = yaml.safe_load(spec_file)

    spec = create_spec(spec_dict)
    
    return(spec)


async def starlette_request_to_openapi_request(star_request: Type[Response]) -> OpenAPIRequest:
    """Converts a starlette Request object to a OpenApiRequest object 
    from the openapi_core library."""

    return OpenAPIRequest(
        full_url_pattern=str(star_request.url),
        method=star_request.method.lower(),
        body=await star_request.body(),
        mimetype=star_request.headers["content-type"],
        #! need to add query parameters and header info a openapi_core RequestParameters object
    )


def starlette_response_to_openapi_response(star_response: Request) -> OpenAPIResponse:
    """Converts a starlette Response object to a OpenApiResponse object 
    from the openapi_core library."""

    return OpenAPIResponse(
        data=star_response.body,
        status_code=star_response.status_code,
        # add headers
        mimetype=star_response.media_type,
    )


async def greet(request: Request):
    spec = get_openapi_spec()

    # validate request: 
    openapi_request = await starlette_request_to_openapi_request(request)
    request_validator = RequestValidator(spec)
    request_validation = request_validator.validate(openapi_request)
    # request_validation.raise_for_errors()

    # generate response:
    response = JSONResponse({"messages": "Hello world!"})

    # validate response:
    openapi_response = starlette_response_to_openapi_response(response)
    response_validator = ResponseValidator(spec)
    response_validation = response_validator.validate(openapi_request, openapi_response)
    # response_validation.raise_for_errors()

    return response


routes = [
    Route('/api/v1/greet', greet, methods=["POST"]),
]

app = Starlette(
    debug=True, 
    routes=routes
)

if __name__ == "__main__":    
    uvicorn.run(
        app,
        port=8080
    )    