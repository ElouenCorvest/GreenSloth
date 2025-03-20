from pathlib import Path

from greensloth_utils import update_from_main_gloss

model_name = "{{MODEL_NAME}}"


for i, j in zip(
    ("comps", "comps", "rates"), ("comps", "derived_comps", "rates"), strict=False
):
    update_from_main_gloss(
        main_gloss_path=Path(__file__).parents[4] / "Templates" / f"{i}_glossary.csv",
        gloss_path=Path(__file__).parents[1] / f"{j}.csv",
        add_to_main=False,
        model_title=model_name,
    )
