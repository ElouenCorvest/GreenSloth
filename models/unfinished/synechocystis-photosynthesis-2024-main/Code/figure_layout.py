import matplotlib.pyplot as plt
import numpy as np

scaling_factor = 0.32

# Function for setting the default figure size
def figsize(rel_width, rel_height):
    default_width = 15 * scaling_factor  # inches

    return (rel_width * default_width, rel_height * default_width)


# Function for labelling figures with letters
def label_figure(fig, pos, label):
    if isinstance(pos, str):
        if pos == "top left":
            pos = (0, 1.01)
        elif pos == "top right":
            pos = (0.98, 1.01)
    
    if isinstance(pos, tuple):
        fig.text(*pos, label, size=13)


# Get a factor of the original rcParam as value
def rcfac(rckwarg: str, factor: float):
    old = plt.rcParams.get(rckwarg)
    if isinstance(old, int):
        return int(np.round(old * factor))
    elif isinstance(old, float):
        return old * factor
    elif old is None:
        raise ValueError(f"not an rcParam: {rckwarg}")
    else:
        raise ValueError(f"unsupported type of rcParam: {type(old)}")

# Set the default parameters for plots

# Generally halve the size and width of fonts, lines, etc.
plt.rcParams.update(
    {k:v*scaling_factor for k,v in plt.rcParams.items() if (k.endswith("size") or k.endswith("width") or k.endswith("pad")) and isinstance(v, (int, float))}
)

# plt.rcParams.update({
#     "font.size": 5,

#     "xtick.major.size": 1.25,
#     "xtick.minor.size": 1,

#     "ytick.major.size": 1.25,
#     "ytick.minor.size": 1,
# })
        


# Create the Figure layouts
paper_figs = {}

plt.rcParams["figure.max_open_warning"] = 30

# MAIN FIGURES
# Create figure 1
paper_figs["Fig1"] = {"main": plt.figure(figsize=figsize(1, 0.4))}


# Create figure 2
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.5))
gs = fig.add_gridspec(1,2)

sfig1 = fig.add_subfigure(gs[0])
label_figure(sfig1, pos="top left", label="A")
sfig2 = fig.add_subfigure(gs[1])
label_figure(sfig2, pos="top left", label="B")

paper_figs["Fig7"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
    }
}


# Create figure 3
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.8))
gs = fig.add_gridspec(2, 2, height_ratios=[2, 3], width_ratios=[2,1])

sfig2 = fig.add_subfigure(gs[0, :])
label_figure(sfig2, pos=(0.01,1.1), label="A")
label_figure(sfig2, pos=(0.2,1.1), label="B")
label_figure(sfig2, pos=(0.39,1.1), label="C")
label_figure(sfig2, pos=(0.58,1.1), label="D")
label_figure(sfig2, pos=(0.77,1.1), label="E")
sfig3 = fig.add_subfigure(gs[1, :-1])
label_figure(sfig3, pos=(0.03,1.01), label="F")
label_figure(sfig3, pos=(0.03,0.5), label="G")
sfig4 = fig.add_subfigure(gs[1, -1])
label_figure(sfig4, pos=(0.03,1.01), label="H")

paper_figs["Fig2"] = {
    "main": fig,
    "subs": {
        "A": sfig2,
        "F": sfig3,
        "H": sfig4,
    }
}


# Create figure 4
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 1.1))
gs = fig.add_gridspec(4,1, height_ratios=[1,1,1.5,1], hspace=0.12)

sfig1 = fig.add_subfigure(gs[0])
label_figure(sfig1, pos=(0.0,0.99), label="A")
sfig2 = fig.add_subfigure(gs[1])
label_figure(sfig2, pos=(0.0,0.99), label="B")
sfig3 = fig.add_subfigure(gs[2])
label_figure(sfig3, pos=(0.0,1.01), label="C")
label_figure(sfig3, pos=(0.25,1.01), label="D")
label_figure(sfig3, pos=(0.5,1.01), label="E")
label_figure(sfig3, pos=(0.75,1.01), label="F")
label_figure(sfig3, pos=(0.0,0.5), label="G")
label_figure(sfig3, pos=(0.25,0.5), label="H")
label_figure(sfig3, pos=(0.5,0.5), label="I")
label_figure(sfig3, pos=(0.75,0.5), label="J")
sfig4 = fig.add_subfigure(gs[3])
label_figure(sfig4, pos=(0.0,0.99), label="K")
label_figure(sfig4, pos=(0.5,0.99), label="L")

paper_figs["Fig3"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
        "C": sfig3,
        "K": sfig4,
    }
}


# Create figure 5
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.6))
gs = fig.add_gridspec(3,3, hspace=0.15, height_ratios=[1,0.01,2])

sfig1 = fig.add_subfigure(gs[:1, :])
label_figure(sfig1, pos=(0.0,1.01), label="A")
label_figure(sfig1, pos=(0.25,1.01), label="B")
label_figure(sfig1, pos=(0.5,1.01), label="C")
label_figure(sfig1, pos=(0.75,1.01), label="D")
sfig2 = fig.add_subfigure(gs[1:, :1])
label_figure(sfig2, pos="top left", label="E")
sfig3 = fig.add_subfigure(gs[2:, 1:])
sfig4 = fig.add_subfigure(gs[1, 1:])
label_figure(sfig4, pos=(0.0,1.01), label="F")
label_figure(sfig4, pos=(0.5,1.01), label="G")

paper_figs["Fig4"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "E": sfig2,
        "F": sfig3,
    }
}


# Create figure 6
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.6))
gs = fig.add_gridspec(2,3, hspace=0.12)

sfig1 = fig.add_subfigure(gs[:, 0])
label_figure(sfig1, pos="top left", label="A")
sfig2 = fig.add_subfigure(gs[0, 1:])
label_figure(sfig2, pos=(0.0,1.01), label="B")
label_figure(sfig2, pos=(0.5,1.01), label="C")
sfig3 = fig.add_subfigure(gs[1, 1])
label_figure(sfig3, pos="top left", label="D")
sfig4 = fig.add_subfigure(gs[1, 2])
label_figure(sfig4, pos="top left", label="E")

paper_figs["Fig6"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
        "D": sfig3,
        "E": sfig4,
    }
}


# Create figure 7
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.9))
gs = fig.add_gridspec(3,3, height_ratios=[0.5,1,1], hspace=0.12)

sfig1 = fig.add_subfigure(gs[0, :])
label_figure(sfig1, pos="top left", label="A")
sfig2 = fig.add_subfigure(gs[1, :])
label_figure(sfig2, pos=(0.0,1.01), label="B")
label_figure(sfig2, pos=(0.33,1.01), label="C")
label_figure(sfig2, pos=(0.66,1.01), label="D")
sfig3 = fig.add_subfigure(gs[2, :])
label_figure(sfig3, pos=(0.0,1.01), label="E")
label_figure(sfig3, pos=(0.5,1.01), label="F")

paper_figs["Fig5"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
        "E": sfig3,
    }
}


# Create figure 8
fig = plt.figure(figsize=figsize(1, 0.3))
label_figure(fig, pos=(0.1,0.95), label="A")
label_figure(fig, pos=(0.37,0.95), label="B")
label_figure(fig, pos=(0.64,0.95), label="C")

paper_figs["Fig8"] = {"main": fig}


# SUPPLEMENTAL FIGURES
# Create figure S1
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.5))
gs = fig.add_gridspec(1, 2)

sfig1 = fig.add_subfigure(gs[0])
label_figure(sfig1, pos=(0.0,0.9), label="A")
sfig2 = fig.add_subfigure(gs[1])
label_figure(sfig2, pos=(0.0,0.9), label="B")

paper_figs["FigS1"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
    }
}


# Create figure S2
paper_figs["FigS3"] = {"main": plt.figure(figsize=figsize(0.6, 0.4))}

# Create figure S3
paper_figs["FigS7"] = {"main": plt.figure(figsize=figsize(1, 0.4))}



# Create figure S4
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.5))
gs = fig.add_gridspec(1, 3, wspace=0.1)

sfig1 = fig.add_subfigure(gs[0])
label_figure(sfig1, pos=(0.0,0.8), label="A")
sfig2 = fig.add_subfigure(gs[1])
label_figure(sfig2, pos=(0.0,0.8), label="B")
sfig3 = fig.add_subfigure(gs[2])
label_figure(sfig3, pos=(0.0,0.8), label="C")

paper_figs["FigS11"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
        "C": sfig3,
    }
}


# Create figure S5
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.5))
gs = fig.add_gridspec(1,2)

sfig1 = fig.add_subfigure(gs[0])
label_figure(sfig1, pos="top left", label="A")
sfig2 = fig.add_subfigure(gs[1])
label_figure(sfig2, pos=(-0.02, 1.01), label="B")

paper_figs["FigS2"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
    }
}


# Create figure S6
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.5))
gs = fig.add_gridspec(1, 2)

sfig1 = fig.add_subfigure(gs[0])
label_figure(sfig1, pos=(0.0,1.01), label="A")
label_figure(sfig1, pos=(0.0,0.5), label="B")
sfig2 = fig.add_subfigure(gs[1])
label_figure(sfig2, pos=(0.0,1.01), label="C")
label_figure(sfig2, pos=(0.0,0.5), label="D")

paper_figs["FigS4"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "C": sfig2,
    }
}


# Create figure S7
fig = plt.figure(figsize=figsize(1, 0.3))
label_figure(fig, pos=(0.0,1.1), label="A")
label_figure(fig, pos=(0.25,1.1), label="B")
label_figure(fig, pos=(0.5,1.1), label="C")
label_figure(fig, pos=(0.75,1.1), label="D")

paper_figs["FigS6"] = {"main": fig}

# Create figure S8
fig = plt.figure(figsize=figsize(1, 0.8))
label_figure(fig, pos=(0.1,0.89), label="A")
label_figure(fig, pos=(0.32,0.89), label="B")
label_figure(fig, pos=(0.52,0.89), label="C")
label_figure(fig, pos=(0.73,0.89), label="D")

label_figure(fig, pos=(0.1,0.61), label="E")
label_figure(fig, pos=(0.32,0.61), label="F")
label_figure(fig, pos=(0.52,0.61), label="G")
label_figure(fig, pos=(0.73,0.61), label="H")

label_figure(fig, pos=(0.1,0.335), label="I")
label_figure(fig, pos=(0.32,0.335), label="J")
label_figure(fig, pos=(0.52,0.335), label="K")
label_figure(fig, pos=(0.73,0.335), label="L")

paper_figs["FigS5"] = {"main": fig}

# Create figure S9
fig = plt.figure(constrained_layout=True, figsize=figsize(1, 0.5))
gs = fig.add_gridspec(1, 2)

sfig1 = fig.add_subfigure(gs[0])
label_figure(sfig1, pos="top left", label="A")
sfig2 = fig.add_subfigure(gs[1])
label_figure(sfig2, pos="top left", label="B")


paper_figs["FigS13"] = {
    "main": fig,
    "subs": {
        "A": sfig1,
        "B": sfig2,
    }
}



# Create figure S10
fig = plt.figure(figsize=figsize(1, 0.6))
label_figure(fig, pos=(0.10,0.9), label="A")
label_figure(fig, pos=(0.39,0.9), label="B")
label_figure(fig, pos=(0.67,0.9), label="C")

label_figure(fig, pos=(0.10,0.615), label="D")
label_figure(fig, pos=(0.39,0.615), label="E")
label_figure(fig, pos=(0.67,0.615), label="F")

label_figure(fig, pos=(0.10,0.34), label="G")
label_figure(fig, pos=(0.39,0.34), label="H")
label_figure(fig, pos=(0.67,0.34), label="I")

paper_figs["FigS10"] = {"main": fig}


# Create figure S11
fig = plt.figure(figsize=figsize(0.7, 0.4))
label_figure(fig, pos=(0.0,0.97), label="A")
label_figure(fig, pos=(0.5,0.97), label="B")

paper_figs["FigS8"] = {"main": fig}


# Create figure S12
fig = plt.figure(figsize=figsize(1, 0.5))
label_figure(fig, pos=(0.0,0.93), label="A")
label_figure(fig, pos=(0.33,0.93), label="B")
label_figure(fig, pos=(0.66,0.93), label="C")

paper_figs["FigS9"] = {"main": fig}



# Create figure S13
fig = plt.figure(figsize=figsize(1, 0.35))
label_figure(fig, pos=(0.1,0.93), label="A")
label_figure(fig, pos=(0.36,0.93), label="B")
label_figure(fig, pos=(0.65,0.93), label="C")

paper_figs["FigS12"] = {"main": fig}