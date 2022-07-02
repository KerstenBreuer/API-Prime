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
"""Examples for OpenAPI specs."""


from dataclasses import dataclass
from pathlib import Path

from apiprimed.api_spec import OpenApiSpec

from . import BASE_DIR

SPECS_DIR = BASE_DIR / "specs"


@dataclass
class ExampleSpec:
    """Data on an example OpenAPI spec."""

    json_path: Path
    yaml_path: Path
    spec: OpenApiSpec


EXAMPLE_SPEC = ExampleSpec(
    json_path=SPECS_DIR / "greet_api.json",
    yaml_path=SPECS_DIR / "greet_api.yaml",
    spec=OpenApiSpec(SPECS_DIR / "greet_api.json"),
)
