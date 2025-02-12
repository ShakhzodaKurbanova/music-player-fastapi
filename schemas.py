from pydantic import BaseModel

class ArtistCreate(BaseModel):
    name: str

class SongCreate(BaseModel):
    title: str
    artist_id: int

class ArtistUpdate(BaseModel):
    old_name: str
    new_name: str

class PlaylistCreate(BaseModel):
    name: str