#!/usr/bin/env python3

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

# pylint: skip-file

"""This script checks that the license and license headers
exists and that they are up to date.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import List, Tuple, Union

# root directory of the package:
ROOT_DIR = Path(__file__).parent.parent.resolve()

# file containing the default global copyright notice:
GLOBAL_COPYRIGHT_FILE_PATH = ROOT_DIR / ".devcontainer" / "license_header.txt"

# exlude files and dirs from license header check:
EXCLUDE = [
    ".devcontainer",
    "eggs",
    ".eggs",
    "dist",
    "build",
    "develop-eggs",
    "lib",
    "lib62",
    "parts",
    "sdist",
    "wheels",
    "pip-wheel-metadata",
    ".git",
    ".github",
    ".flake8",
    ".gitignore",
    ".pylintrc",
    "example_config.yaml",
    "config_schema.json",
    "LICENSE",  # is checked but not for the license header
    ".pre-commit-config.yaml",
    "docs",
    "requirements.txt",
    ".vscode",
    ".mypy.ini",
    ".mypy_cache",
    "db_migration",
    ".pytest_cache",
    ".editorconfig",
    ".static_files",
    ".mandatory_files",
]

# exclude file by file ending from license header check:
EXCLUDE_ENDINGS = ["json", "pyc", "yaml", "yml", "md", "html", "xml"]

# exclude any files with names that match any of the following regex:
EXCLUDE_PATTERN = [r".*\.egg-info.*", r".*__cache__.*", r".*\.git.*"]

# A list of all chars that may be used to introduce a comment:
COMMENT_CHARS = ["#"]

AUTHOR = """Universität Tübingen, DKFZ and EMBL
for the German Human Genome-Phenome Archive (GHGA)"""

# The copyright notice should not date earlier than this year:
MIN_YEAR = 2021

# The path to the License file relative to target dir
LICENCE_FILE = "LICENSE"


class UnexpectedBinaryFileError(RuntimeError):
    """Thrown when trying to read a binary file."""

    def __init__(self, file_path: Union[str, Path]):
        message = f"The file could not be read because it is binary: {str(file_path)}"
        super().__init__(message)


def is_relative_to(*, parent: Path, child: Path):
    """Checks if the parent path is relative to the child path."""
    return str(child.absolute()).startswith(str(parent.absolute()))


def get_target_files(
    target_dir: Path,
    exclude: List[str] = EXCLUDE,
    exclude_endings: List[str] = EXCLUDE_ENDINGS,
    exclude_pattern: List[str] = EXCLUDE_PATTERN,
) -> List[Path]:
    """Get target files that are not match the exclude conditions.
    Args:
        target_dir (pathlib.Path): The target dir to search.
        exclude (List[str], optional):
            Overwrite default list of file/dir paths relative to
            the target dir that shall be excluded.
        exclude_endings (List[str], optional):
            Overwrite default list of file endings that shall
            be excluded.
        exclude_pattern (List[str], optional):
            Overwrite default list of regex patterns match file path
            for exclusion.
    """
    abs_target_dir = Path(target_dir).absolute()
    exclude_normalized = [(abs_target_dir / excl).absolute() for excl in exclude]

    # get all files:
    all_files = [
        file_.absolute() for file_ in Path(abs_target_dir).rglob("*") if file_.is_file()
    ]

    target_files = [
        file_
        for file_ in all_files
        if not (
            any(
                [
                    is_relative_to(parent=excl, child=file_)
                    for excl in exclude_normalized
                ]
            )
            or any([str(file_).endswith(ending) for ending in exclude_endings])
            or any([re.match(pattern, str(file_)) for pattern in exclude_pattern])
        )
    ]
    return target_files


def normalized_line(line: str, chars_to_trim: List[str] = COMMENT_CHARS) -> str:
    norm_line = line.strip()

    for char in chars_to_trim:
        norm_line = norm_line.strip(char)

    return norm_line.strip("\n").strip("\t").strip()


def normalized_text(text: str, chars_to_trim: List[str] = COMMENT_CHARS) -> str:
    "Normalize a license header text."
    lines = text.split("\n")

    norm_lines: List[str] = []

    for line in lines:
        stripped_line = line.strip()
        # exclude shebang:
        if stripped_line.startswith("#!"):
            continue

        norm_line = normalized_line(stripped_line, chars_to_trim)

        # exclude empty lines:
        if norm_line == "":
            continue

        norm_lines.append(norm_line)

    return "\n".join(norm_lines).strip("\n")


def is_commented_line(line: str, comment_chars: List[str] = COMMENT_CHARS) -> bool:
    """Checks whether a line is a comment."""
    line_stripped = line.strip()
    for commment_char in comment_chars:
        if line_stripped.startswith(commment_char):
            return True

    return False


def is_empty_line(line: str) -> bool:
    """Checks whether a line is empty."""
    return line.strip("\n").strip("\t").strip() == ""


def get_header(file_path: Path, comment_chars: List[str] = COMMENT_CHARS):
    """Extracts the header from a file and normalizes it."""
    header_lines: List[str] = []

    try:
        with open(file_path) as file:
            for line in file:
                if is_commented_line(
                    line, comment_chars=comment_chars
                ) or is_empty_line(line):
                    header_lines.append(line)
                else:
                    break
    except UnicodeDecodeError as error:
        raise UnexpectedBinaryFileError(file_path=file_path) from error

    # normalize the lines:
    header = "".join(header_lines)
    return normalized_text(header, chars_to_trim=comment_chars)


def validate_year_string(year_string: str, min_year: int = MIN_YEAR) -> bool:
    """Check if the specified year string is valid.
    Returns `True` if valid or `False` otherwise."""

    current_year = date.today().year

    # If the year_string is a single number, it must be the current year:
    if year_string.isnumeric():
        return int(year_string) == current_year

    # Otherwise, a range (e.g. 2021 - 2022) is expected:
    match = re.match(r"(\d+) - (\d+)", year_string)

    if not match:
        return False

    year_1 = int(match.group(1))
    year_2 = int(match.group(2))

    # Check the validity of the range:
    if year_1 >= min_year and year_2 <= year_1:
        return False

    # year_2 must be equal to the current year:
    return year_2 == current_year


def check_copyright_notice(
    copyright: str,
    expected_license_header: str,
    min_year: int = MIN_YEAR,
) -> bool:
    """Checks the specified copyright text against a template.

    expected_license_header (str):
        The expected license header.
    author (str, optional):
        The author that shall be included in the license header.
        It will replace any appearance of "{author}" in the license
        header. This defaults to an auther info for GHGA.

    """
    # If the expected_license_header is already set, check if the current copyright is
    # identical to it:
    copyright_lines = copyright.split("\n")
    template_lines = expected_license_header.split("\n")

    # The header should be at least as long as the template:
    if len(copyright_lines) < len(template_lines):
        return False

    for idx, template_line in enumerate(template_lines):
        header_line = copyright_lines[idx]

        if "{year}" in template_line:
            pattern = template_line.replace("{year}", r"(.+?)")
            match = re.match(pattern, header_line)

            if not match:
                return False

            year_string = match.group(1)
            if not validate_year_string(year_string, min_year=min_year):
                return False

        elif template_line != header_line:
            return False

    # Take this copyright as the expected_license_header from now on:
    copyright_cleaned = "\n".join(copyright_lines[0 : len(template_line)])  # noqa: E203
    expected_license_header = copyright_cleaned

    return True


def check_file_headers(
    target_dir: Path,
    expected_license_header: str,
    exclude: List[str] = EXCLUDE,
    exclude_endings: List[str] = EXCLUDE_ENDINGS,
    exclude_pattern: List[str] = EXCLUDE_PATTERN,
    comment_chars: List[str] = COMMENT_CHARS,
) -> Tuple[List[Path], List[Path]]:
    """Check files for presence of a license header and verify that
    the copyright notice is up to date (correct year).

    Args:
        target_dir (pathlib.Path): The target dir to search.
        expected_license_header (str):
            The expected license header.
        exclude (List[str], optional):
            Overwrite default list of file/dir paths relative to
            the target dir that shall be excluded.
        exclude_endings (List[str], optional):
            Overwrite default list of file endings that shall
            be excluded.
        exclude_pattern (List[str], optional):
            Overwrite default list of regex patterns match file path
            for exclusion.
    """
    target_files = get_target_files(
        target_dir,
        exclude=exclude,
        exclude_endings=exclude_endings,
        exclude_pattern=exclude_pattern,
    )

    # check if license header present in file:
    passed_files: List[Path] = []
    failed_files: List[Path] = []

    for target_file in target_files:
        try:
            header = get_header(target_file, comment_chars=comment_chars)
            if check_copyright_notice(
                copyright=header,
                expected_license_header=expected_license_header,
            ):
                passed_files.append(target_file)
            else:
                failed_files.append(target_file)
        except UnexpectedBinaryFileError:
            # This file is a binary and is therefor skipped.
            pass

    return (passed_files, failed_files)


def check_license_file(
    license_file: Path,
    expected_license_header: str,
    comment_chars: List[str] = COMMENT_CHARS,
) -> bool:
    """Currently only checks if the copyright notice in the
    License file is up to data.

    Args:
        license_file (pathlib.Path, optional): Overwrite the default license file.
        expected_license_header (str):
            The expected license header.
    """

    if not license_file.is_file():
        print(f'Could not find license file "{str(license_file)}".')
        return False

    with open(license_file) as file_:
        license_text = normalized_text(file_.read(), chars_to_trim=comment_chars)

    # Extract the copyright notice:
    # (is expected to be at the end of the file):
    template_lines = expected_license_header.split("\n")
    license_lines = license_text.split("\n")
    copyright = "\n".join(license_lines[-len(template_lines) :])  # noqa: E203

    return check_copyright_notice(
        copyright=copyright,
        expected_license_header=expected_license_header,
    )


def run():
    """Run checks from CLI."""
    parser = argparse.ArgumentParser(
        prog="license-checker",
        description=(
            "This script checks that the license and license headers "
            + "exists and that they are up to date."
        ),
    )

    parser.add_argument(
        "-L",
        "--no-license-file-check",
        help="Disables the check of the license file",
        action="store_true",
    )

    parser.add_argument(
        "-t",
        "--target-dir",
        help="Specify a custom target dir. Overwrites the default package root.",
    )

    args = parser.parse_args()

    target_dir = Path(args.target_dir).absolute() if args.target_dir else ROOT_DIR

    print(f'Working in "{target_dir}"\n')

    # get global copyright from .devcontainer/license_header.txt file:
    with open(GLOBAL_COPYRIGHT_FILE_PATH) as expected_license_header_file:
        expected_license_header = normalized_text(expected_license_header_file.read())

    if args.no_license_file_check:
        license_file_valid = True
    else:
        license_file = Path(target_dir / LICENCE_FILE)
        print(f'Checking if LICENSE file is up to date: "{license_file}"')
        license_file_valid = check_license_file(
            license_file, expected_license_header=expected_license_header
        )
        print(
            "Copyright notice in license file is "
            + ("" if license_file_valid else "not ")
            + "up to date.\n"
        )

    print("Checking license headers in files:")
    passed_files, failed_files = check_file_headers(
        target_dir, expected_license_header=expected_license_header
    )
    print(f"{len(passed_files)} files passed.")
    print(f"{len(failed_files)} files failed" + (":" if failed_files else "."))
    for failed_file in failed_files:
        print(f'  - "{failed_file.relative_to(target_dir)}"')

    print("")

    if failed_files or not license_file_valid:
        print("Some checks failed.")
        sys.exit(1)

    print("All checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    run()
