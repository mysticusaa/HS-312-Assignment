import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("screen_time.csv")

# merging minor categories into Other
df["Other"] += df["Productivity & Finance"] + df["Information & Reading"] + df["Education"]
df = df.drop(columns=["Productivity & Finance", "Information & Reading", "Education"])

# updated time categories and colors 
time_columns = ["Social", "Entertainment", "Games", "Other"]
colors = {
    "Social": "#FFD700",         # Yellow/Gold
    "Entertainment": "#457B9D",  # Muted Blue
    "Games": "#2A9D8F",          # Teal Green
    "Other": "#F4A261"           # Warm Orange
}

# computing total and the max total screen time for reference
for col in time_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
df["Total"] = df[time_columns].sum(axis=1)
max_total = df["Total"].max()

columns_per_row = 7
rows = (len(df) + columns_per_row - 1) // columns_per_row
fig, axs = plt.subplots(rows, columns_per_row, figsize=(14, 2.5 * rows))
axs = axs.flatten()

# circle plotting
BASE_RADIUS = 1.0
AXIS_LIMITS = (-BASE_RADIUS, BASE_RADIUS)

for i, row in df.iterrows():
    values = row[time_columns].tolist()
    day = row["Date"]
    total = row["Total"]

    if total == 0:
        continue

    ax = axs[i]
    rel_radius = total / max_total

    ax.set_xlim(*AXIS_LIMITS)
    ax.set_ylim(*AXIS_LIMITS)

    wedges, _ = ax.pie(
        values,
        colors=[colors[col] for col in time_columns],
        startangle=90,
        counterclock=False,
        radius=rel_radius
    )

    ax.set_aspect('equal')
    ax.set_title(day, fontsize=8, pad=-1) 

for j in range(i + 1, len(axs)):
    axs[j].axis('off')

# final plot
plt.tight_layout()
plt.savefig("screen_time_clockface_scaled_peachy.png", dpi=300)
# plt.show()
plt.close(fig)
