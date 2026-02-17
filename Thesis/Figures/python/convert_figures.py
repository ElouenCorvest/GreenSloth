from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from pathlib import Path
import math
import pandas as pd

demon_dict = {}
fig_dict = {}
info_dict = {}

for d in (Path(__file__).parents[4] / "GreenSloth" / "models").iterdir():
    if "." in d.name or not d.is_dir():
        continue
    
    info_dict[d.name] = {}
    for file in (d / "model_info").glob("*.csv"):
        df = pd.read_csv(file)
        info_dict[d.name][file.stem] = len(df)
    
    for file in (d / "figures").glob("*.svg"):
        file_name = file.name
        model_name = file_name.split("_")[0]
        sim_name = file_name.split("_")[-1].replace(".svg", "")
        if "demon" in file.name:
            if demon_dict.get(sim_name) is None:
                demon_dict[sim_name] = {}
            demon_dict[sim_name][model_name] = {"file path": str(file.absolute()), "drawing": svg2rlg(str(file.absolute()))}
        elif "fig" in file.name:
            if fig_dict.get(model_name) is None:
                fig_dict[model_name] = {}
            fig_dict[model_name][sim_name] = {"file path": str(file.absolute()), "drawing": svg2rlg(str(file.absolute()))}

info_df = pd.DataFrame(info_dict).T
name_pointer = {
    "derived_comps": "Derived Variables",
    "comps": "Variables",
    "rates": "Reactions",
    "params": "Parameters",
    "derived_params": "Derived Parameters",
}
custom_order = ["Variables", "Parameters", "Reactions", "Derived Variables", "Derived Parameters"]
info_df = info_df.rename(columns=name_pointer)
info_df = info_df[custom_order]
info_df = info_df.sort_index()
info_df["Total"] = info_df.sum(axis=1)
info_df.to_latex(
    buf=Path(__file__).parents[2] / "Tables" / "models_info.tex",
    column_format="lcccccc",
    longtable=True,
    caption=(
        r"\textbf{Summary of Meta-Information of All the Models.}\\The number of variables, parameters, reactions, and derived variables and parameters, and total sum are shown for each model. These values have been extracted directly from the model implementations. A derived quantity, is a quantity that is calculated inside the model. The separation between derived variable and parameter is based on expertise and is not based on a strict rule. However, a main aspect that was considered was with what quantity it was derived from. If the quantity was derived from even a single time-dependent quantity, it is considered a derived variable. The model used are Bellasio2019~\cite{bellasioGeneralisedDynamicModel2019}, Fuente2024~\cite{fuenteMathematicalModelSimulate2024}, Li2021~\cite{liImpactIonFluxes2021}, Matuszynska2016~\cite{matuszynskaMathematicalModelNonphotochemical2016}, and Saadat2021~\cite{saadatComputationalAnalysisAlternative2021}",
        r"Summary of Meta-Information of All the Models.",
    ),
    label="tab:models-meta",
)
    
for model, figs in fig_dict.items():
    for fig, info in figs.items():
        output_path = Path(__file__).parents[1] / "Validations" / f"{model}_{fig}.pdf"
        drawing = info["drawing"]
        c = canvas.Canvas(str(output_path), pagesize=(drawing.width, drawing.height))
        renderPDF.draw(drawing, c, 0, 0)
        c.save()

for sim, models in demon_dict.items():
    
    output_path = Path(__file__).parents[1] / "Demonstrations" / f"{sim}.pdf"
    
    num_cols = 2
    
    lst_names = [model for model in models.keys()]
    lst_names = sorted(lst_names)
    
    grid_drawings = []
    grid_names = []
    
    for model_name in lst_names:
        if grid_drawings == []:
            grid_drawings.append([models[model_name]["drawing"]])
            grid_names.append([model_name.capitalize()])
        elif len(grid_drawings[-1]) < num_cols:
            grid_drawings[-1].append(models[model_name]["drawing"])
            grid_names[-1].append(model_name.capitalize())
        else:
            grid_drawings.append([models[model_name]["drawing"]])
            grid_names.append([model_name.capitalize()])
    title_height_add = 40
    spacing_between = 40
    page_height = 0
    page_width = 0
    for row in grid_drawings:
        row_height = max([drawing.height for drawing in row])
        row_height += title_height_add
        page_height += row_height
        
        row_width = sum([drawing.width for drawing in row])
        page_width = max(row_width, page_width)

    page_width += spacing_between
    c = canvas.Canvas(str(output_path), pagesize=(page_width, page_height))
    fontsize = 24
    c.setFont("Helvetica-Bold", fontsize)
    
    for i, row in enumerate(grid_drawings):
        row_height = max([drawing.height for drawing in row])
        row_width = sum([drawing.width for drawing in row])
        x_offset = (page_width - spacing_between - row_width) / 2
        y_offset = page_height - (row_height + title_height_add) * (i + 1)
    
        
        for j, drawing in enumerate(row):
            renderPDF.draw(drawing, c, x_offset, y_offset)
            
            title = grid_names[i][j]
            text_width = c.stringWidth(title, "Helvetica-Bold", fontsize)
            if "mca" in sim.lower():
                text_x = x_offset + (drawing.width - text_width) / 2
            else:
                text_x = x_offset + (drawing.width * 0.1)
            c.drawString(text_x, y_offset + drawing.height + 5, title)
            x_offset += drawing.width + spacing_between
            
    
    c.save()
    


# for file in :
#     file_name = file.name
    
#     model_name = file_name.split("_")[0]
#     sim_name = file_name.split("_")[-1].replace(".svg", "")
#     drawing = svg2rlg(file.absolute())
#     output_path = Path(__file__).parents[1] / "Demonstrations" / f"{model_name}_{sim_name}.pdf"

#     c = canvas.Canvas(str(output_path), pagesize=(drawing.width, drawing.height + 40))
#     renderPDF.draw(drawing, c, 0, 0)
    
#     fontsize = 24
#     text = model_name.capitalize()
    
#     c.setFont("Helvetica-Bold", fontsize)
#     text_width = c.stringWidth(text, "Helvetica-Bold", fontsize)
    
#     c.drawString((drawing.width - text_width) / 2, drawing.height + 10, text)
#     c.save()