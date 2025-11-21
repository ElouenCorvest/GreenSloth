import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import textwrap

# FAIR Usage

fig, ax = plt.subplots(figsize=(10, 5))

for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
    
ax.tick_params(axis="x", bottom=False, labelbottom=False)

# Seperation of FAIR citations over the years
year_num_citations = {
    "2025": {"num": 1265, "color": "#DA4167"},
    "2024": {"num": 1408, "color": "#297373"},
    "2023": {"num": 1327, "color": "#5C95FF"},
    "2022": {"num": 1283, "color": "#F19143"},
    "2021": {"num": 1016, "color": "#3F3244"},
    "2020": {"num": 685, "color": "#F15025"},
    "2019": {"num": 454, "color": "#88A2AA"},
    "2018": {"num": 216, "color": "#ECCBD9"},
    "2017": {"num": 114, "color": "#97D2FB"},
    "2016": {"num": 22, "color": "#F55536"}
}

total_citations = sum([data["num"] for data in year_num_citations.values()])
    
bottom = 0
for label, val in year_num_citations.items():
    height = val["num"] / total_citations
    if label == "2024":
        edgecolor = None
        zorder = 10
        for y in [[bottom, 0], [bottom + height, 1]]:
            ax.plot([0.5/2, 1 - 0.5/2], y, color=val["color"], lw=3, zorder=15)
    else:
        edgecolor = None
        zorder = 1
    bar = ax.bar(0, height, width=0.5, label=label, bottom=bottom, color=val["color"], edgecolor=edgecolor, lw=2, zorder=zorder)
    if height*100 >= 5:
        ax.text(0, bottom + height / 2, f"{height*100:.1f}%", ha='center', va='center', color='white', fontweight='bold', zorder=200)
    bottom += height

ax.legend(title="Year", loc="center left", bbox_to_anchor=(-0.2, 0, 0.5, 1), frameon=False)
ax.text(0, 1.05, f"Total citations: {total_citations}", horizontalalignment='center', verticalalignment='center', transform=ax.transData)


# Seperation of FAIR citations over publication types in year 2024

pub_types = {
    "Article": {"num": 1002, "color": "#318787", "hatch": "|"},
    "Review": {"num": 210, "color": "#369696", "hatch": "-"},
    "Proceeding Paper": {"num": 126, "color": "#3BA5A5", "hatch": "\\"},
    "Misc.": {"num": 64 + 32 + 6 + 5 + 2, "color": "#41B4B4", "hatch": "/" },
}

total_types = sum([data["num"] for data in pub_types.values()])

bottom = 0
for label, val in pub_types.items():
    height = val["num"] / total_types
    ax.bar(1, height, width=0.5, label=label, bottom=bottom, color=val["color"], hatch=val["hatch"])
    ax.text(1, bottom + height / 2, f"{height*100:.1f}%", ha='center', va='center', color='white', fontweight='bold')
    bottom += height

ax.text(1, 1.05, f"2024 citations: {year_num_citations['2024']['num']}", horizontalalignment='center', verticalalignment='center', transform=ax.transData)
ax.legend(title="Article Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False)

# Articles using FAIR in 2024

plt.tight_layout()
plt.savefig(Path(__file__).parent / ".." / "fair_usage.pdf", dpi=600)

# Photosynthesis model query
model_query = pd.read_csv(Path(__file__).parent / "photosynthesismodel_query.csv", index_col=0)
model_query = model_query.iloc[::-1]
model_query = model_query.loc[2000:2024]

fig, ax = plt.subplots()

ax.bar([i for i in range(len(model_query))], model_query["Count"], tick_label=model_query.index, color=["#ff616b" if year%2 == 0 else "#000831" for year in model_query.index])
ax.tick_params(axis="x", labelrotation=45)

ax.set_ylabel(textwrap.fill("Number of Publications with \"photosynthesis model\" query", width=40, break_long_words=False), fontsize="large")
ax.text(0.2, 0.8, f"Total: {model_query.sum().values[0]}", transform=ax.transAxes, ha="center", va="center", size="large", fontweight="bold")

for side in ["top", "right"]:
    ax.spines[side].set_visible(False)


plt.tight_layout()
plt.savefig(Path(__file__).parent / ".." / "photosynthesis_model_query.pdf", dpi=600)
