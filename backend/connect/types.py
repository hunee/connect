#print('__FILE__: ', __file__)

import typing

Scope = typing.MutableMapping[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]

Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]

ASGIApp = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]

DecoratedCallable = typing.TypeVar("DecoratedCallable", bound=typing.Callable[..., typing.Any])