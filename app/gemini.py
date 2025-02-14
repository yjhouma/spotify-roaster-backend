from google import genai
from app.config import get_settings
from models import FullRoast

setting = get_settings()



prompt = '''
You are a sarcastic Music snob who thinks your music is superior to others.
Your job is to brutally roast my music taste, given my top 10 artists, and be brutally honest, sarcastic, and funny while roasting it.
First you will roast the artist one by one, making snarky sarcastic comment about my taste.

Then you will create a more coherent verdict about my music taste about 2 to 4 parahraph long.

'''

def generate_gemini_response(artists: list[str]) -> FullRoast:
    # artists = 'Here are my top 10 artists: Tyler, The Cereator; Kendrick Lamar; Frank Ocean; New Jeans; Doechii; Kanye West; XG; Charli xcx; SZA; N.E.R.D'
    inpt = 'Here are my top 10 artists: ' + '; '.join(artists)

    client = genai.Client(api_key=setting.GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt+inpt,
        config={
            
            'response_mime_type': 'application/json',
            'response_schema': FullRoast,
            'temperature': 0.8
        }
    )
    # Use the response as a JSON string.
    return response.parsed