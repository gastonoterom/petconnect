import asyncio
from typing import Callable, Any
from concurrent.futures import ThreadPoolExecutor

MAX_THREAD_POOL_SIZE = 100
BACKGROUND_THREAD_POOL_EXECUTOR = ThreadPoolExecutor(
    max_workers=MAX_THREAD_POOL_SIZE, thread_name_prefix="background_worker_"
)


async def run_async(func: Callable[..., Any], *args, **kwargs) -> Any:
    def work():
        return func(*args, **kwargs)

    return await asyncio.get_event_loop().run_in_executor(
        BACKGROUND_THREAD_POOL_EXECUTOR, work
    )


tasks = set()


def run_fire_forget(func: Callable[..., Any], *args, **kwargs) -> None:
    future = asyncio.ensure_future(run_async(func, *args, **kwargs))

    tasks.add(future)

    future.add_done_callback(lambda _: tasks.remove(future))
