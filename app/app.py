from fastapi import FastAPI, HTTPException, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from typing import Optional
from session import session_manager
import spotify
from config import get_settings
from session import session_manager
from models import TopArtistsResponse, SpotifySession


app = FastAPI()
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def get_current_session(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session = session_manager.get_session(session_id=session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid Session")
    return session
    

@app.get("/api/spotify/session")
async def get_session_status(session: SpotifySession = Depends(get_current_session)):
    """Check if the session is valid."""
    return {"status": "authenticated", "session": session}

@app.get("/api/spotify/login")
async def spotify_login():
    try:
        sp_oauth = spotify.create_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        return {"url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/spotify/callback")
async def spotify_callback(code: str):
    print(code)
    try:
        sp_oauth = spotify.create_spotify_oauth()
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']
        session_id = session_manager.create_session(
            access_token=token_info['access_token'],
            refresh_token=token_info['refresh_token'],
            expires_in=token_info['expires_in']
        )

        response = RedirectResponse(url=f"{settings.FRONTEND_URL}")
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=False,  # Enable in production with HTTPS
            samesite="lax",
            max_age=1800  # 30 minutes
        )

        return response


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/spotify/top-artists", response_model=TopArtistsResponse)
async def get_top_artists(session: SpotifySession = Depends(get_current_session)):
    """Get user's top artists using session token."""
    try:
        artists = await spotify.get_user_top_artists(session.access_token)
        return {"artists": artists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
