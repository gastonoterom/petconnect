from abc import ABC


class Entity(ABC):
    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id


class Message(ABC):
    pass


class Command(Message, ABC):
    pass


class Event(Message, ABC):
    pass
