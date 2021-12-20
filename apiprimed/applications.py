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

"""Main application class and associated functionality."""

from typing import Sequence, Dict, Type, Callable, Union, AsyncContextManager
from pathlib import Path

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute

from .api_spec import OpenApiSpec


class ApiPrimed(Starlette):
    """
    Creates an application instance based on a Starlette app.
    """

    # many arguments cannot be avoided as ther are comming directly from starlette:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        spec: Union[Path, OpenApiSpec],
        debug: bool = False,
        routes: Sequence[BaseRoute] = None,
        middleware: Sequence[Middleware] = None,
        exception_handlers: Dict[Union[int, Type[Exception]], Callable] = None,
        on_startup: Sequence[Callable] = None,
        on_shutdown: Sequence[Callable] = None,
        lifespan: Callable[["Starlette"], AsyncContextManager] = None,
    ) -> None:
        """
        Initialize application instance.
        """

        self.spec = spec if isinstance(spec, OpenApiSpec) else OpenApiSpec(spec)

        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
        )
