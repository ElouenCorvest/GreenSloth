import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import string
from RWTHColors import ColorManager as cm

"https://www.webofscience.com/wos/woscc/summary/0b793bdb-ab8b-456e-a5fb-085fc470f5a2-019f07a73b/relevance/1"

report_files_dir = Path(__file__).parent / "bib_report_files"
print(report_files_dir)

df_combined = pd.DataFrame()

for file in report_files_dir.iterdir():
    print(file.name)
    if file.suffix == ".xls":
        df = pd.read_excel(file)
        df_combined = pd.concat([df_combined, df], ignore_index=True)
        
year_counts = df_combined['Publication Year'].value_counts().sort_index()
year_counts = year_counts[year_counts.index < 2026]
year_counts = year_counts[year_counts.index >= 1970]

year_diff = year_counts.diff().fillna(0)

fig = plt.figure(figsize=(10, 4))
gs = GridSpec(1, 2, width_ratios=[1, 1], wspace=0.3)

axs = {}
axs["year_diff"] = fig.add_subplot(gs[0])
axs['year_citations'] = fig.add_subplot(gs[1])

odd_years = year_counts.index[year_counts.index % 2 == 1]
axs['year_citations'].bar(odd_years, year_counts.loc[odd_years], color='#E6C74C', width=1)
even_years = year_counts.index[year_counts.index % 2 == 0]
axs['year_citations'].bar(even_years, year_counts.loc[even_years], color='#6B5CA5', width=1)

years_cum = year_counts.cumsum()
years_cum_diff = years_cum.diff().fillna(0)
axs['year_diff'].bar(years_cum_diff.index, years_cum_diff.values, color='#A3A960', width=1, bottom=years_cum.shift(1, fill_value=0))
axs['year_diff'].bar(years_cum.shift(1, fill_value=0).index, years_cum.shift(1, fill_value=0).values, color='#EBEBEB', width=1.1)

for i, ax in enumerate(axs.values()):
    ax.set_xlabel("Year")
    ax.set_xlim(1969.5, 2025.5)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
        
    ax.text(-0.1, 1.1, string.ascii_uppercase[i], transform=ax.transAxes, fontsize=16, fontweight='bold', va='top', ha='right')
    
axs['year_citations'].set_ylabel("Number of New Publications per Year")
axs['year_diff'].set_ylabel("Cumulative Total of Publications")

plt.savefig(Path(__file__).parents[1] / f"bibsearch.pdf")

data = {
    "Plant Sciences": {"val": 2610, "color": cm.RWTHBlau.p(75)},
    "Ecology": {"val": 1030, "color": cm.RWTHBordeaux.p(75)},
    "Forestry": {"val": 862, "color": cm.RWTHTuerkis.p(75)},
    "Environmental Sciences": {"val": 1244, "color": cm.RWTHGruen.p(75)},
    "Meteorology & Atmospheric Sciences": {"val": 861, "color": cm.RWTHLila.p(75)},
}

total = 6877

data["Others"] = {"val": total - sum([v["val"] for v in data.values()]), "color": cm.RWTHOrange.p(75)}

fig, ax = plt.subplots(figsize=(3, 6))

def autopct_filter(pct):
    return ('%.1f%%' % pct) if pct >= 5 else ''

# ax.pie(data.values(), labels=data.keys(), autopct=autopct_filter, startangle=90, colors=[
#     cm.RWTHBlau.p(75),
#     cm.RWTHBordeaux.p(75),
#     cm.RWTHTuerkis.p(75),
#     cm.RWTHGruen.p(75),
#     cm.RWTHLila.p(75),
#     cm.RWTHOrange.p(75),
# ])
prior = 0
for key, val in data.items():
    ax.bar(1, val["val"]/total, label=key, bottom=prior, color=val["color"], width=1)
    if key != "Others":
        ax.text(1, prior + val["val"]/(2*total), f"{key}\n{val['val']} ({val['val']/total:.1%})", ha='center', va='center', fontsize=8)
    else:
        ax.text(1, prior + val["val"]/(2*total), f"{key} {val['val']} ({val['val']/total:.1%})", ha='center', va='center', fontsize=8)
    prior += val["val"]/total

ax.text(0.45, 0.5, f"Total: {total}", transform=ax.transData, fontsize=12, fontweight='bold', va='center', ha='right', rotation=90)
ax.set_xlim(0.5, 1.5)
ax.set_ylim(0, 1)

for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
ax.set_xticks([])
ax.set_yticks([0, 1])

plt.savefig(Path(__file__).parents[1] / "fvcb_analyse.pdf")
    