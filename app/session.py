import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from models import SpotifySession

class SessionManager:
    def __init__(self):
        self._sessions: Dict[str, SpotifySession] = {}
        print('SessionManager Created')

    def create_session(self, access_token: str, refresh_token: str, expires_in: int) -> str:
        session_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        session = SpotifySession(
            session_id=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        
        self._sessions[session_id] = session
        print(f"Created new session: {session_id}")
        print(f"Current sessions: {self._sessions}")

        return session_id
    
    def get_session(self, session_id: str) -> Optional[SpotifySession]:
        session = self._sessions.get(session_id)
        print(f"Getting session {session_id}: {'Found' if session else 'Not found'}")
        print(f"Current sessions in store: {list(self._sessions.keys())}")
        return session
    
    def remove_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]

# Global session manager instance
session_manager = SessionManager()