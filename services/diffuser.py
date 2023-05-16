# %%
from pathlib import Path
from diffusers import DiffusionPipeline
from PIL import Image
from IPython.display import display
from random import choice, random
from uuid import uuid1
import torch

# %%
pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
if torch.cuda.is_available():
    pipeline.to("cuda")  # type: ignore

# %%
persons = [
    "magician",
    "wizard",
    "witch",
    "alchemist",
    "sorcerer",
    "mage",
    "enchanter",
    "druid",
]
styles = [
    "photorealistic",
    "cartoon",
    "sketch",
    "hyper-realistic",
    "watercolor",
    "fantasy comic",
]
potions = ["potion", "liquid", "elixir", "brew"]
bottles = ["bottle", "beaker", "flask", "vial", "jar", "jug", "pitcher"]
colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "orange",
    "pink",
    "black",
    "white",
    "colorful",
]
potions = ["potion", "liquid", "elixir", "brew"]
activities = [
    "swirling",
    "bubbling",
    "boiling",
    "fizzing",
    "smoking",
    "steaming",
    "glowing",
    "sparkling",
]
people = [
    "Rembrandt",
    "Norman Rockwell",
    "Patrick Nagel",
    "Ruan Jia and Mandy Jurgens and William-Adolphe Bouguereau",
    "Gaston Bussiere and Craig Mulling and J. C. Leyendecker",
    "Andy Warhol",
    "Pablo Picasso",
    "Salvador Dali",
    "Vincent van Gogh",
    "Claude Monet",
    "Edgar Degas",
    "Paul Cezanne",
    "Paul Gauguin",
    "Henri Matisse",
    "Georges Seurat",
    "Edward Hopper",
    "Jackson Pollock",
    "Georgia O'Keeffe",
    "Frida Kahlo",
    "Grant Wood",
    "Roy Lichtenstein",
]


# %%
def generate_prompt():
    if random() < 0.3:
        result = (
            f"image of a {choice(persons)} holding a "
            f"{choice(bottles)} in which a {choice(colors)} "
            f"{choice(potions)} is {choice(activities)}"
        )
    else:
        result = (
            f"image of a {choice(bottles)} in which a {choice(colors)} "
            f"{choice(potions)} is {choice(activities)}"
        )
    if random() < 0.4:
        result = "An " + result + f" in the style of {choice(people)}"
    else:
        result = f"A {choice(styles)} " + result
    return result


# %%
# generate_prompt()


# %%
def generate_image():
    prompt = generate_prompt()
    id = uuid1().hex[:8]
    image = pipeline(prompt).images[0]  # type: ignore
    return id, prompt, image


# %%
def generate_and_save_image(output_dir: Path = Path("/tmp")):
    id, prompt, image = generate_image()
    prompt_file = output_dir / f"prompt-{id}.txt"
    image_file = output_dir / f"img-{id}.png"
    with open(prompt_file, "w") as f:
        f.write(prompt)
    image.save(image_file)  # type: ignore
    return id, prompt_file, image_file


# %%
def generate_and_display_image(output_dir="/tmp"):
    output_dir = Path(output_dir)
    id, prompt_file, image_file = generate_and_save_image(output_dir)
    img = Image.open(output_dir / image_file)
    with open(output_dir / prompt_file) as f:
        prompt = f.read()
    print(prompt)
    display(img)
    return id, prompt_file, image_file

# %%
