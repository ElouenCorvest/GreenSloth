from github import Github, Auth
import requests
import os
from pathlib import Path
import json
import importlib
import sys
from mxlpy import Model, Simulator, make_protocol
import shutil
import numpy as np

models_pointer = Path(__file__).parents[3] / "src" / "js" / "models.json"

with open(models_pointer) as f:
    d = json.load(f)
    models_to_get = d.keys()

g = Github()
repo = g.get_repo("ElouenCorvest/GreenSloth")

pfd_pointer = {
    "Bellasio2019": "PPFD",
    "Matuszynska2016": "pfd",
    "Saadat2021": "PPFD",
    "Fuente2024": "PPFD",
    "Li2021": "PPFD"
}

for model in models_to_get:  # Example PPFD values
    print(f"Getting {model}...")
    (Path(__file__).parent / "tmp").mkdir(exist_ok=True)
    
    contents = repo.get_contents(f"/models/{model}/model")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            # Download the file
            print(f"Downloading {file_content.path}...")
            r = requests.get(file_content.download_url)
            with open(Path(__file__).parent / "tmp" / file_content.name, "wb") as f:
                content_str = r.content.decode('utf-8')
                updated_str = content_str.replace(model, 'get_model')
                f.write(updated_str.encode('utf-8'))
                

    if 'tmp' in sys.modules:
        del sys.modules['tmp']
        # Also delete submodules if they exist (e.g., tmp.model)
        for mod in list(sys.modules.keys()):
            if mod.startswith("tmp."):
                del sys.modules[mod]

    import tmp
    importlib.reload(tmp)
    model_here = tmp.get_model()
    
    (Path(__file__).parents[1] / f"{model}").mkdir(exist_ok=True)
    
    for pfd in np.arange(100, 1600, 100):
        sim = Simulator(model_here)
        sim.simulate_protocol(make_protocol([
            (10, {pfd_pointer[model]: 0}),
            (50, {pfd_pointer[model]: pfd})
        ]), time_points_per_step=100)
        sim.get_result().unwrap_or_err().get_variables().to_json(Path(__file__).parents[1] / f"{model}" / f"{pfd}.json")
    
    shutil.rmtree(Path(__file__).parent / "tmp")  # Clean up the temporary folder