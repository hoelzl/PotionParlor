# %%
from pathlib import Path
from diffusers import DiffusionPipeline
from PIL import Image
from IPython.display import display
from random import choice, random
from uuid import uuid1
import torch

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
artists = [
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
def create_pipeline():
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    if torch.cuda.is_available():
        pipeline.to("cuda")  # type: ignore
        # pipeline.enable_attention_slicing()  # type: ignore
    return pipeline


# %%
class PromptGenerator:
    def __init__(self) -> None:
        self.persons = persons
        self.styles = styles
        self.potions = potions
        self.bottles = bottles
        self.colors = colors
        self.activities = activities
        self.artists = artists

    def prompt(self) -> str:
        if random() < 0.3:
            result = (
                f"image of a {choice(self.persons)} holding a "
                f"{choice(self.bottles)} in which a {choice(self.colors)} "
                f"{choice(self.potions)} is {choice(self.activities)}"
            )
        else:
            result = (
                f"image of a {choice(self.bottles)} in which a {choice(self.colors)} "
                f"{choice(self.potions)} is {choice(self.activities)}"
            )
        if random() < 0.4:
            result = "An " + result + f" in the style of {choice(self.artists)}"
        else:
            result = f"A {choice(self.styles)} " + result
        return result


# %%
def generate_prompt():
    return PromptGenerator().prompt()


# %%
generate_prompt()


# %%
def generate_image(pipeline, generate_prompt=generate_prompt):
    prompt = generate_prompt()
    id = uuid1().hex[:8]
    image = pipeline(prompt).images[0]  # type: ignore
    return id, prompt, image


# %%
def generate_and_save_image(
    pipeline, output_dir: Path = Path("/tmp"), generate_prompt=generate_prompt
):
    id, prompt, image = generate_image(pipeline, generate_prompt=generate_prompt)
    prompt_file = output_dir / f"prompt-{id}.txt"
    image_file = output_dir / f"img-{id}.png"
    with open(prompt_file, "w") as f:
        f.write(prompt)
    image.save(image_file)  # type: ignore
    return id, prompt_file, image_file


# %%
def generate_and_display_image(
    pipeline, output_dir="/tmp", generate_prompt=generate_prompt
):
    output_dir = Path(output_dir)
    id, prompt_file, image_file = generate_and_save_image(
        pipeline, output_dir=output_dir, generate_prompt=generate_prompt
    )
    img = Image.open(output_dir / image_file)
    with open(output_dir / prompt_file) as f:
        prompt = f.read()
    print(prompt)
    display(img)
    return id, prompt_file, image_file


# %%
if __name__ == "__main__":
    pass
else:
    pipeline = create_pipeline()
    generate_and_display_image(pipeline)

# %%
