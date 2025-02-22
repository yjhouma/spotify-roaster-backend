import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import get_settings
import logging
import os
from dotenv import load_dotenv


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# get_settings.cache_clear()



def create_spotify_oauth():
    settings = get_settings()
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-top-read",
        open_browser=True,
        cache_path=None,  # Disable local caching
        show_dialog=True  # Forces re-auth if needed
    )

async def get_user_top_artists(token):
    """Get user's top artists using the provided token."""
    try:
        sp = spotipy.Spotify(auth=token)
        # Get top artists from the last 6 months

        print(sp.current_user())
        results = sp.current_user_top_artists(
            limit=10,
            offset=0,
            time_range='medium_term'
        )
        
        # Extract relevant information
        artists = []
        for item in results['items']:
            artist = {
                'name': item['name'],
                'genres': item['genres'],
                'popularity': item['popularity'],
                'spotify_url': item['external_urls']['spotify']
            }
            artists.append(artist)
            
        return artists
    except Exception as e:
        # print(f"Error fetching top artists: {e}")
        raise

if __name__ == '__main__':
    # Force reload environment variables
    # load_dotenv(override=True)
    
    # # Print all relevant environment variables
    # print("\nEnvironment Variables:")
    # print(f"SPOTIFY_REDIRECT_URI from env: {os.getenv('SPOTIFY_REDIRECT_URI')}")
    
    # # Get settings and print
    # settings = get_settings()
    # print("\nSettings Object:")
    # print(f"SPOTIFY_REDIRECT_URI from settings: {settings.SPOTIFY_REDIRECT_URI}")
    
    # # Create OAuth and print URL
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print("\nGenerated Auth URL:")
    print(auth_url)
    
    # Print OAuth object details
    print("\nOAuth Object Details:")
    print(f"OAuth redirect_uri: {sp_oauth.redirect_uri}")
    print(f"OAuth client_id: {'*' * len(sp_oauth.client_id)}")  # masked for security
    print(f"OAuth scope: {sp_oauth.scope}")
