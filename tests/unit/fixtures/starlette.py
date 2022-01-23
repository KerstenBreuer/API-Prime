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

"""Fake starlette requests and responses."""

from copy import deepcopy
from typing import Coroutine
from dataclasses import dataclass
from datetime import datetime, timezone

from starlette.datastructures import QueryParams, Headers, URL
from starlette.responses import JSONResponse


@dataclass
class FakeStareletteRequest:
    method: str
    url: URL
    query_params: QueryParams
    path_params: dict
    headers: Headers
    cookies: dict
    body: Coroutine


def body_coroutine_factory(body: bytes):
    """creates a coroutine for returning the specified body"""

    async def get_body():
        return body

    return get_body


# example requests and responses:

VALID_STARLETTE_REQUEST = FakeStareletteRequest(
    method="POST",
    url=URL("http://127.0.0.1:8080/api/v1/greet/en?informal=true"),
    query_params=QueryParams("informal=true"),
    path_params={"lang": "en"},
    headers=Headers(
        {
            "host": "127.0.0.1:8080",
            "user-agent": "python-requests/2.26.0",
            "accept-encoding": "gzip, deflate",
            "accept": "*/*",
            "connection": "keep-alive",
            "content-type": "application/json",
            "content-length": "40",
        }
    ),
    cookies={},
    body=body_coroutine_factory(b'{"greeting": "Hello", "person": "world"}'),
)

INVALID_STARLETTE_REQUEST = deepcopy(VALID_STARLETTE_REQUEST)
INVALID_STARLETTE_REQUEST.body = body_coroutine_factory(
    b'{"greeting": 1, "person": "world"}'
)


VALID_STARLETTE_RESPONSE = JSONResponse(
    {"message": "Hello world!", "time": datetime.now(timezone.utc).isoformat()}
)

INVALID_STARLETTE_RESPONSE = JSONResponse(
    {"message": 1, "time": datetime.now(timezone.utc).isoformat()}
)
