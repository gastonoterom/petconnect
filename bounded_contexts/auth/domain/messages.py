from dataclasses import dataclass
from common.base_utils import Event


# Events
@dataclass
class AccountCreated(Event):
    account_id: str
