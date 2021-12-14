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

import werkzeug.datastructures
from starlette.requests import Request

from openapi_core.validation.request.datatypes import OpenAPIRequest, RequestParameters


async def starlette_to_openapi_request(
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
