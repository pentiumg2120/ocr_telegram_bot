import config
import promt, text

from google import genai
from google.genai import types

client = genai.Client(api_key=config.gemini_api_key)


async def photo_to_text(encoded_image):
    global client
    try:
        image = types.Part.from_bytes(
            data=encoded_image, mime_type="image/jpeg"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[promt.photo_to_text, image],
        )

    except Exception:
        return text.ai_error

    else:
        return response.text
