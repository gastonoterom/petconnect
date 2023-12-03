from __future__ import annotations

from typing import Iterator

from common.base_utils import Message
from infrastructure import postgres_session_factory


# Too much coupling between this and the database, but it's okay.
# Ideally, there should be an abstract unit of work that separates this.


class UnitOfWork:
    def __init__(self, session_factory=postgres_session_factory) -> None:
        self.__messages: list[Message] = []
        self.session_factory = session_factory

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

    async def __aexit__(self, _, exception, __) -> None:
        # If an exception happened during the context manager, raise that
        if exception:
            await self.rollback()
            raise exception

        # If not, try to commit
        try:
            await self.commit()
        except Exception as e:
            await self.rollback()
            raise e
        finally:
            await self.session.close()

    def collect_messages(self) -> Iterator[Message]:
        for message in self.__messages:
            self.__messages.pop(0)
            yield message

    def publish_message(self, message: Message) -> None:
        self.__messages.append(message)

    def publish_messages(self, messages: list[Message]) -> None:
        self.__messages.extend(messages)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
