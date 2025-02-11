from pydantic import BaseModel
from typing import List, Optional

class NewArtist(BaseModel):
    artist_name: str


class NewSong(BaseModel):
    title: str
    artist: str

