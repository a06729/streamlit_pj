from openai import OpenAI
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OpenAi_key = os.environ.get('openai_apikey')

client = OpenAI(api_key=OpenAi_key)

def createImgae(image_prompt:str):
    print(image_prompt)
    response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
    image_url = response.data[0].url
    return image_url