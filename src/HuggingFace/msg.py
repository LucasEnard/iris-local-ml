from dataclasses import dataclass
from grongier.pex import Message

@dataclass
class HFRequest(Message):
    """
    `HFRequest` is a `Message` that has two fields: `api_url` and `payload`
    """
    api_url:str = None
    payload:str = None

@dataclass
class HFResponse(Message):
    """
    "HFResponse is a Message with a payload of type str."

    The payload field is a special field that is used to store the message's payload. The payload is the
    data that is being sent from one node to another
    """
    payload:str = None

@dataclass
class MLRequest(Message):
    pass

@dataclass
class MLResponse(Message):
    output:str = None

