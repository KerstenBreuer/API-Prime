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

import requests
import yaml
from openapi_core import create_spec
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from openapi_core.validation.request.validators import RequestValidator

with open("./openapi.yaml", "r") as spec_file:
    content = yaml.safe_load(spec_file)

spec = create_spec(content)

request = requests.models.Request(
    method="post",
    url="http://localhost:8080/api/v1/test",
    json={"greeting": "Hello", "person": "world"},
    headers={
        "Content-Type": "application/json",
    },
)

openapi_request = RequestsOpenAPIRequest(request)
validator = RequestValidator(spec)
result = validator.validate(openapi_request)

result.raise_for_errors()
