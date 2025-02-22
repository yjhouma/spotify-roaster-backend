from fastapi import FastAPI, HTTPException, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from typing import Optional
from session import session_manager
import spotify
from config import get_settings
from session import session_manager
from models import TopArtistsResponse, SpotifySession, FullRoast
import gemini


app = FastAPI()
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL], # Change this to front_end url later on prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"]
)


async def get_current_session(session_id: Optional[str] = Cookie(None)):
    print(f"Received session_id: {session_id}")  

    if not session_id:
        print("No session cookie found")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session = session_manager.get_session(session_id=session_id)
    print("Session Recieved")
    if not session:
        print(f"Invalid session ID: {session_id}")
        raise HTTPException(status_code=401, detail="Invalid Session")
    return session

@app.get("/api/debug/cookie")
async def debug_cookie(session_id: Optional[str] = Cookie(None)):
    return {
        "has_cookie": session_id is not None,
        "session_id": session_id
    }

@app.get("/health")
async def healthcheck():
    return {"status": "healthy"}

@app.get("/api/debug/session")
async def debug_session(session_id: Optional[str] = Cookie(None)):
    """Debug endpoint to check session cookie."""
    return {
        "has_cookie": session_id is not None,
        "session_id": session_id,
        "is_valid": session_manager.get_session(session_id) is not None if session_id else False
    }

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
    try:
        sp_oauth = spotify.create_spotify_oauth()
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']
        session_id = session_manager.create_session(
            access_token=token_info['access_token'],
            refresh_token=token_info['refresh_token'],
            expires_in=token_info['expires_in']
        )
        print(f'creating Session ID: {session_id}')
        print(f'for token: {access_token}')
        response = RedirectResponse(url=f"{settings.FRONTEND_URL}/callback")
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=True,  # Enable in production with HTTPS, Change this in prod to True
            samesite="none",
            max_age=1800,  # 30 minutes
            domain=".onrender.com",  # Match your backend's domain
            path="/"
        )
        return response


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/spotify/top-artists", response_model=FullRoast)
async def get_top_artists(session: SpotifySession = Depends(get_current_session)):
    """Get user's top artists using session token."""
    try:
        print(f'running the api for {session.session_id}')
        artists = await spotify.get_user_top_artists(session.access_token)
        roasts = await gemini.generate_gemini_response(artists)


        return roasts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
