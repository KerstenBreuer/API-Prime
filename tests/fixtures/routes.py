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

"""Example route functions."""

from starlette.responses import JSONResponse

from apiprimed.requests import ValidatedRequest


def greet_route(request: ValidatedRequest):
    """An example route function."""

    lang = request.path_params["lang"]

    if lang == "en":
        message = "Hello World"
    else:
        message = "Hallo Welt"

    return JSONResponse({"message": message})
