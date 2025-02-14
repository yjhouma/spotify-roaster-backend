from pydantic import BaseModel, TypeAdapter
from typing import List, Optional
from datetime import datetime

class SpotifySession(BaseModel):
    session_id: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    
class Artist(BaseModel):
    name: str
    genres: List[str]
    popularity: int
    spotify_url: str

class TopArtistsResponse(BaseModel):
    artists: List[Artist]


class RoastIndividualArtist(BaseModel):
    artist: str
    snarky_introduction: str
    comments: str

class FullRoast(BaseModel):
    artist_comment: list[RoastIndividualArtist]
    final_verdict: str
