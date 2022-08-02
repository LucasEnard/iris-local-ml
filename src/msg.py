from time import strftime
from grongier.pex import Message
from dataclasses import dataclass

@dataclass()
class HFRequest(Message):
    api_url:str = None
    payload:str = None

@dataclass()
class HFResponse(Message):
    payload:str = None

@dataclass()
class MLRequest(Message):
    pass

@dataclass()
class MLResponse(Message):
    output:str = None

