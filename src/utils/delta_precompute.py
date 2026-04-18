import torch
from PIL import Image


def compute_and_save_delta(image_path: str, output_path: str = "delta.npy"):
    img = Image.open(image_path).convert("L")
    delta = torch.log(torch.tensor(img) + 1.0) - torch.log(256.0 - torch.tensor(img))
    torch.save(delta.cpu().numpy(), output_path)
