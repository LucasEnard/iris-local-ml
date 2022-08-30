from dataclasses import dataclass
from typing import List
from grongier.pex import Message
from obj import Person

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

@dataclass
# > The `CreatePersonResponse` class is a message that contains an `id` field of type `int`
class CreatePersonRequest(Message):

    person:Person = None

@dataclass
# > The `CreatePersonResponse` class is a message that contains an `id` field of type `int`
class CreatePersonResponse(Message):

    id:int=None

@dataclass
# > This class is a response to a request to get all persons
class GetAllPersonResponse(Message):
    persons:List[Person] = None

# A class that inherits from Message. It has two attributes, currPage and pageSize.
@dataclass
class GetAllPersonRequest(Message):
    currPage:int=None
    pageSize:int=None

@dataclass
# > The `GetPersonResponse` class is a `Message` class that has a `person` attribute of type `Person`
class GetPersonResponse(Message):
    person:Person = None

@dataclass
# > A request to get a person by id
class GetPersonRequest(Message):
    id:int = None

@dataclass
# > UpdatePersonRequest is a message that contains an id and a person
class UpdatePersonRequest(Message):
    id:int = None
    person:Person = None

@dataclass
# > UpdatePersonResponse is a Message.
class UpdatePersonResponse(Message):
    pass

@dataclass
# > DeletePersonRequest is a message that contains an id field
class DeletePersonRequest(Message):
    id:int = None

@dataclass
# DeletePersonResponse is a Message.
class DeletePersonResponse(Message):
    pass

