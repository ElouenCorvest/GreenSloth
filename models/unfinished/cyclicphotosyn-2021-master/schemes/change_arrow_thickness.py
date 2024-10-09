# Export data via
# `s.get_fluxes_df().iloc[-1].to_csv("data_name.csv", index_label=["reaction"], header=["flux"])`

from collections import defaultdict
from pathlib import Path

import click
import pandas as pd
import xmltodict
from matplotlib import colors


def get_reactions(xml_objects: xmltodict.OrderedDict) -> dict[str, set[int]]:
    reactions = defaultdict(set)
    for idx, obj in enumerate(xml_objects):
        if reaction := obj.get("@reaction", False):
            reactions[reaction].add(idx)
    return dict(reactions)


def write_stroke_width(xml_objects: xmltodict.OrderedDict, idx: int, flux: float):
    style = xml_objects[idx]["mxCell"]["@style"].rstrip(";").split(";")
    d = {k: v for (k, v) in (i.split("=") for i in style)}
    d["strokeWidth"] = flux
    style = ";".join(f"{k}={v}" for k, v in d.items())
    xml_objects[idx]["mxCell"]["@style"] = style


def write_stroke_alpha(xml_objects: xmltodict.OrderedDict, idx: int, flux: float):
    style = xml_objects[idx]["mxCell"]["@style"].rstrip(";").split(";")
    d = {k: v for (k, v) in (i.split("=") for i in style)}
    d["strokeColor"] = colors.to_hex((1 - flux, 1 - flux, 1 - flux))
    style = ";".join(f"{k}={v}" for k, v in d.items())
    xml_objects[idx]["mxCell"]["@style"] = style


def scale(values: pd.Series, new_min: float, new_max: float) -> pd.Series:
    m = (values - values.min()) / (values.max() - values.min())
    return (new_max - new_min) * m + new_min


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("flux-csv", type=click.Path(exists=True))
@click.option("--output", type=click.Path())
@click.option("--mode", type=click.Choice(["width", "shade"]), default="width")
@click.option("--min-width", default=1.0)
@click.option("--max-width", default=5.0)
@click.option("--min-shade", default=0.5)
@click.option("--max-shade", default=1.0)
def main(
    input: str,
    flux_csv: str,
    output: str,
    mode: str,
    min_width: float,
    max_width: float,
    min_shade: float,
    max_shade: float,
):
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)

    with open(input, "rb") as f:
        diagram = xmltodict.parse(f)
    xml_objects = diagram["mxfile"]["diagram"]["mxGraphModel"]["root"]["object"]

    reactions = get_reactions(xml_objects)
    fluxes = pd.read_csv(flux_csv, index_col=0, squeeze=True)

    if mode == "width":
        widths = scale(fluxes.loc[reactions], min_width, max_width)
        for name, idxs in reactions.items():
            width = widths[name]
            for idx in idxs:
                write_stroke_width(xml_objects, idx, width)
    elif mode == "shade":
        alphas = scale(fluxes.loc[reactions], min_shade, max_shade)
        for name, idxs in reactions.items():
            alpha = alphas[name]
            for idx in idxs:
                write_stroke_alpha(xml_objects, idx, alpha)
    else:
        raise ValueError("Mode unknown")

    if output is None:
        output = input.split(".")[0] + "-out"
    if not output.endswith(".drawio"):
        output = f"{output}.drawio"

    with open(out_dir / output, "wb") as f:
        print(f"Writing file to {out_dir / output}")
        xmltodict.unparse(diagram, f)


if __name__ == "__main__":
    main()
