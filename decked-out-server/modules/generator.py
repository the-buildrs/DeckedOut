import os
import openai
from dotenv import load_dotenv

# Set up the API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

# Generator Functions


def generate_completion(prompt: str, max_tokens=7, temperature=0.6) -> str:
    '''Get the completion response from OpenAI API'''
    completion_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return completion_response.choices[0].text


def get_bullet_type(prompt: str) -> bool:
    ''' Get the type of the bullet points (if talking about human or non-human object, etc)'''

    check_living = ("Return 'yes' if the following is talking about a human and"
    "return 'no' if it is referring to a non-human object")
    completion_response = generate_completion(f"'{check_living}: {prompt}'")

    if completion_response == "yes": living_thing = True
    else: living_thing = False

    return living_thing

def get_image_response(prompt: str) -> str:
    '''Get the DALLE2 image response from OpenAI API'''
    image_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
    )
    # returns URL of image
    return image_response.data[0]
