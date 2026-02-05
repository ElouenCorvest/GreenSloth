from email.mime import text
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from pathlib import Path
import math

demon_dict = {}
fig_dict = {}

for d in (Path(__file__).parents[4] / "GreenSloth" / "models").iterdir():
    if "." in d.name or not d.is_dir():
        continue
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