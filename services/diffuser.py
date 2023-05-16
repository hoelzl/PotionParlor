# %%
from diffusers import DiffusionPipeline
import torch

# %%
pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
if torch.cuda.is_available():
    pipeline.to("cuda")

# %%
result = pipeline("A photorealistic image of a full, swirling potion bottle")

