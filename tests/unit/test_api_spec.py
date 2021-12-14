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

"""Tests the `api_spec` module."""

from api_primed.api_spec import OpenApiSpec

from .fixtures.specs import example_specs


def test_spec_from_yaml_and_json():
    """Make sure that creating specs from yaml and json yields the same result"""
    example_spec = example_specs["greet_api"]

    spec_from_json = OpenApiSpec(example_spec["json_path"])
    spec_from_yaml = OpenApiSpec(example_spec["yaml_path"])

    assert spec_from_json.spec_dict == spec_from_yaml.spec_dict
