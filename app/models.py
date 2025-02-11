from pydantic import BaseModel
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