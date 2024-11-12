"""App app subscriptions.

References:
    https://strawberry.rocks/docs/general/subscriptions
"""

import asyncio
import asyncio.subprocess as subprocess
from asyncio import streams
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    AsyncIterator,
    Coroutine,
    Optional,
)

import strawberry

if TYPE_CHECKING:
    pass


async def wait_for_call(coro: Coroutine[Any, Any, bytes]) -> Optional[bytes]:
    r"""Wait_for_call calls the supplied coroutine in a wait_for block.

    This mitigates cases where the coroutine doesn't yield until it has
    completed its task. In this case, reading a line from a StreamReader; if
    there are no `\n` line chars in the stream the function will never exit
    """
    try:
        return await asyncio.wait_for(coro(), timeout=0.1)  # type: ignore
    except asyncio.TimeoutError:
        return None


async def lines(stream: streams.StreamReader) -> AsyncIterator[str]:
    """Lines reads all lines from the provided stream, decoding them as UTF-8 strings."""
    while True:
        b = await wait_for_call(stream.readline)  # type: ignore
        if b:
            yield b.decode("UTF-8").rstrip()
        else:
            break


async def exec_proc(target: int) -> subprocess.Process:
    """exec_proc starts a sub process and returns the handle to it."""
    return await asyncio.create_subprocess_exec(
        "/bin/bash",
        "-c",
        f"for ((i = 0 ; i < {target} ; i++)); do echo $i; sleep 0.2; done",
        stdout=subprocess.PIPE,
    )


async def tail(proc: subprocess.Process) -> AsyncGenerator[str, None]:
    """Tail reads from stdout until the process finishes."""
    # Note: race conditions are possible here since we're in a subprocess. In
    # this case the process can finish between the loop predicate and the call
    # to read a line from stdout. This is a good example of why you need to
    # be defensive by using asyncio.wait_for in wait_for_call().
    while proc.returncode is None:
        async for line in lines(proc.stdout):  # type: ignore
            yield line
    else:
        # read anything left on the pipe after the process has finished
        async for line in lines(proc.stdout):  # type: ignore
            yield line


@strawberry.type
class Subscription:
    """App app subscription class."""

    @strawberry.subscription
    async def run_command(
        self, info: strawberry.Info, target: int = 100
    ) -> AsyncGenerator[str, None]:
        """Run command."""
        print(info.context["request"].scope["user"])
        proc = await exec_proc(target)
        return tail(proc)
