import openapi_core
import yaml
from openapi_core import create_spec

with open("./openapi.yaml", "r") as spec_file:
    content = yaml.safe_load(spec_file)

spec = create_spec(content)


## example request:
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.contrib.requests import RequestsOpenAPIRequest
import requests

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
