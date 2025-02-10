from pydantic import BaseModel
from typing import List, Optional

class NewSong(BaseModel):
    title: str
    artist: str
