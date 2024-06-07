import openai
from PIL import Image
import requests
from io import BytesIO

# Initialize OpenAI API
openai.api_key = 'your_openai_api_key'

script = """
Scene 1: A park in the morning.
Character: Alice
Action: Walking her dog
Dialogue: "It's such a beautiful day!"

Scene 2: A cafe in the afternoon.
Character: Bob
Action: Drinking coffee
Dialogue: "I love this place."
"""

def parse_script(script):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a script parser."},
            {"role": "user", "content": f"Parse the following script:\n\n{script}"}
        ]
    )
    parsed_script = response['choices'][0]['message']['content']
    return parsed_script

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

def composite_images(background, character, position):
    background = background.convert("RGBA")
    character = character.convert("RGBA")
    background.paste(character, position, character)
    return background

parsed_script = parse_script(script)

character_prompt = "Alice walking her dog in a park in the morning"
background_prompt = "A park in the morning"

character_image_url = generate_image(character_prompt)
background_image_url = generate_image(background_prompt)

character_image = Image.open(BytesIO(requests.get(character_image_url).content))
background_image = Image.open(BytesIO(requests.get(background_image_url).content))

character_position = (100, 100)  # Example position
storyboard_frame = composite_images(background_image, character_image, character_position)
storyboard_frame.show()
