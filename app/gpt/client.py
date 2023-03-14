from dataclasses import dataclass, field
from os import environ

import openai
from openai.openai_object import OpenAIObject

from app.gpt.constants import Model
from app.gpt.message import Message


@dataclass
class ChatGPTClient:
    model: Model
    messages: list[Message] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not (key := environ.get("CHATGPT_API_KEY")):
            raise Exception(
                "chatGPT api key is not set as an environment variable"
            )
        openai.api_key = key

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def create(self) -> OpenAIObject:
        return openai.ChatCompletion.create(
            model=self.model.value,
            messages=[m.to_dict() for m in self.messages],
        )
