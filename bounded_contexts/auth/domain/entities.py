from common.base_utils import Entity


class Account(Entity):
    def __init__(self, entity_id: str, email: str, password_hash: str) -> None:
        super().__init__(entity_id=entity_id)
        self.email = email
        self.password_hash = password_hash

    def check_password_hash(self, password_hash: str) -> bool:
        return self.password_hash == password_hash
