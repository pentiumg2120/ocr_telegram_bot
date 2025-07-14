import config
from google import genai
from google.genai import types

client = genai.Client(api_key=config.gemini_api_key)


async def photo_to_text(encoded_image):
    global client
    image = types.Part.from_bytes(
        data=encoded_image, mime_type="image/jpeg"
    )
    promt = "You are a document processor. Your task is to extract all meaningful text from the provided image, including mathematical calculations and formulas. Identify and discard all irrelevant information, such as system UI elements (e.g., battery life, network signal, and time). Organize the remaining text logically for maximum human readability and present it as a single, clean block of plain text. Do not use any special formatting, markup (like HTML or Markdown), or add any introductory or concluding phrases. Your output must be only the extracted content."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[promt, image],
    )
    print(response.text)
    return response.text
