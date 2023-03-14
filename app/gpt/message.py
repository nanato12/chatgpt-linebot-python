from dataclasses import dataclass
from typing import Dict

from app.gpt.constants import Role


@dataclass
class Message:
    role: Role
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role.value, "content": self.content}
