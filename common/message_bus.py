import logging
from typing import Callable, Optional
from dependency_injector.wiring import Provide, inject
from bounded_contexts.event_mappings import Dispatcher
from common.base_utils import Message, Event, Command
from common.unit_of_work import UnitOfWork
from dependencies.dependency_kinds import CommonDependencyKind


class MessageBus:
    dispatcher: Dispatcher = Provide[CommonDependencyKind.dispatcher_factory]
    logger: logging.Logger = logging.getLogger(__name__)

    event_exceptions: list[Exception] = []

    @inject
    async def handle(
        self, message: Message, uow: UnitOfWork = Provide[CommonDependencyKind.uow]
    ):
        queue: list[Message] = [message]

        while queue:
            message = queue.pop(0)

            if isinstance(message, Event):
                await self.handle_event(message, uow, queue)

            elif isinstance(message, Command):
                await self.handle_command(message, uow, queue)

            else:
                raise Exception(f"{message} was not an Event or Command")

    async def handle_event(self, event: Event, uow: UnitOfWork, queue: list):
        handlers: list[Callable] = self.dispatcher.event_handlers.get(type(event), [])

        for handler in handlers:
            try:
                await handler(event, uow)
                queue.extend(uow.collect_messages())

            except Exception as e:
                self.logger.exception(f"Exception handling event: {event}")
                self.logger.exception(f"Exception: {e}")

                self.event_exceptions.append(e)

    async def handle_command(self, command: Command, uow: UnitOfWork, queue: list):
        handler: Optional[Callable] = self.dispatcher.command_handlers.get(
            type(command), None
        )

        if handler is None:
            return

        await handler(command, uow)

        queue.extend(uow.collect_messages())
