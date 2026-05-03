"""
Export all K-Means story canvas visualizations to PNG.
Output directory: outputs/kmeans/plots/
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
OUT_DIR    = os.path.join(ROOT, 'outputs', 'kmeans', 'plots')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   'white',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.spines.left':   True,
    'axes.spines.bottom': True,
    'axes.edgecolor':   '#CCCCCC',
    'axes.labelcolor':  '#444444',
    'xtick.color':      '#666666',
    'ytick.color':      '#666666',
    'text.color':       '#222222',
    'font.family':      'sans-serif',
    'font.size':        10,
    'axes.titlesize':   12,
    'axes.titleweight': 'semibold',
    'axes.titlepad':    12,
    'axes.labelsize':   9,
    'grid.color':       '#EEEEEE',
    'grid.linewidth':   0.8,
    'savefig.dpi':      150,
    'savefig.bbox':     'tight',
    'savefig.facecolor':'white',
})

# Cluster palette
C_COLORS = ['#5B8FA8', '#E8A87C', '#7DBF7D', '#C47D98']
C_LABELS = ['C1 · Quiet Acoustic', 'C2 · Vocal Rhythmic',
            'C3 · Mellow Semi-Instr.', 'C4 · Energetic Mainstream']
C_SHORT  = ['C1', 'C2', 'C3', 'C4']

TIER_COLORS   = ['#888888', '#4A90C4', '#F5A623']
ACCENT        = '#4A90C4'
ACCENT2       = '#F5A623'

def save(name):
    path = os.path.join(OUT_DIR, name)
    plt.savefig(path)
    plt.close()
    print(f'  saved {name}')

# ── 1. Genre Distribution ─────────────────────────────────────────────────────
genres = ['electronic','pop','latin','hip-hop','ambient','rock','lofi',
          'world','arabic','jazz','gaming','classical','blues','afrobeats','wellness']
counts = [589,515,425,395,359,345,298,228,208,146,133,121,88,82,80]

fig, ax = plt.subplots(figsize=(8, 5.5))
y = np.arange(len(genres))
bars = ax.barh(y, counts, color=ACCENT, alpha=0.85, height=0.6)
ax.set_yticks(y)
ax.set_yticklabels(genres, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Track count')
ax.set_title('Genre Distribution — Top 15 Genres')
ax.axvline(100, color='#DDDDDD', linewidth=0.8, linestyle='--')
for bar, val in zip(bars, counts):
    ax.text(bar.get_width() + 6, bar.get_y() + bar.get_height()/2,
            str(val), va='center', fontsize=8, color='#555555')
ax.set_xlim(0, 680)
ax.xaxis.grid(True)
ax.set_axisbelow(True)
save('01_genre_distribution.png')

# ── 2. K-Selection: Silhouette ────────────────────────────────────────────────
k_vals = [2,3,4,5,6,7,8]
sil    = [0.341,0.204,0.199,0.193,0.168,0.169,0.175]

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(k_vals, sil, 'o-', color=ACCENT, linewidth=2, markersize=7)
ax.axvline(4, color=ACCENT2, linewidth=1.5, linestyle='--', alpha=0.8, label='k = 4 selected')
ax.scatter([4], [sil[2]], color=ACCENT2, s=100, zorder=5)
ax.set_xlabel('Number of clusters (k)')
ax.set_ylabel('Average Silhouette Score')
ax.set_title('K-Selection: Silhouette Score')
ax.set_xticks(k_vals)
ax.legend(fontsize=9)
ax.yaxis.grid(True)
ax.set_axisbelow(True)
save('02_k_silhouette.png')

# ── 3. K-Selection: WSS ──────────────────────────────────────────────────────
wss = [35086,31580,28437,26023,24052,22560,21097]

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(k_vals, wss, 's-', color='#7DBF7D', linewidth=2, markersize=7)
ax.axvline(4, color=ACCENT2, linewidth=1.5, linestyle='--', alpha=0.8, label='k = 4 selected')
ax.scatter([4], [wss[2]], color=ACCENT2, s=100, zorder=5)
ax.set_xlabel('Number of clusters (k)')
ax.set_ylabel('Total Within-Cluster SS')
ax.set_title('K-Selection: Within-Cluster Sum of Squares (Elbow)')
ax.set_xticks(k_vals)
ax.legend(fontsize=9)
ax.yaxis.grid(True)
ax.set_axisbelow(True)
save('03_k_wss.png')

# ── 4. Feature Fingerprint (Grouped Bar) ─────────────────────────────────────
feats = ['Danceability','Energy','Valence','Acousticness','Instrumentalness','Speechiness','Liveness']
c1 = [0.212, 0.068, 0.092, 0.932, 0.839, 0.043, 0.110]
c2 = [0.718, 0.656, 0.570, 0.260, 0.026, 0.297, 0.194]
c3 = [0.591, 0.367, 0.335, 0.660, 0.511, 0.062, 0.150]
c4 = [0.660, 0.715, 0.562, 0.170, 0.054, 0.067, 0.174]

x   = np.arange(len(feats))
w   = 0.2
fig, ax = plt.subplots(figsize=(10, 4.5))
for i, (data, color, label) in enumerate(zip([c1,c2,c3,c4], C_COLORS, C_LABELS)):
    ax.bar(x + (i - 1.5) * w, data, w, label=label, color=color, alpha=0.9)
ax.set_xticks(x)
ax.set_xticklabels(feats, fontsize=9)
ax.set_ylabel('Score (0 – 1 scale)')
ax.set_ylim(0, 1.05)
ax.set_title('Audio Fingerprints — All Four Clusters Side by Side')
ax.legend(fontsize=8.5, loc='upper right')
ax.yaxis.grid(True, alpha=0.5)
ax.set_axisbelow(True)
save('04_feature_fingerprint.png')

# ── 5. Loudness by Cluster ────────────────────────────────────────────────────
loudness = [-29.7, -6.6, -12.0, -6.4]

fig, ax = plt.subplots(figsize=(7, 3))
bars = ax.barh(C_LABELS, loudness, color=C_COLORS, alpha=0.88, height=0.5)
ax.axvline(0, color='#BBBBBB', linewidth=0.8)
ax.set_xlabel('Loudness (dB)')
ax.set_title('Loudness by Cluster')
for bar, val in zip(bars, loudness):
    ax.text(bar.get_width() - 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f} dB', va='center', ha='right', fontsize=9, color='white', fontweight='bold')
ax.invert_yaxis()
ax.xaxis.grid(True)
ax.set_axisbelow(True)
save('05_loudness_by_cluster.png')

# ── 6. Tempo by Cluster ───────────────────────────────────────────────────────
tempo = [102.0, 122.5, 114.6, 120.5]

fig, ax = plt.subplots(figsize=(7, 3))
bars = ax.barh(C_LABELS, tempo, color=C_COLORS, alpha=0.88, height=0.5)
ax.set_xlabel('Tempo (BPM)')
ax.set_title('Tempo by Cluster')
ax.set_xlim(90, 130)
for bar, val in zip(bars, tempo):
    ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2,
            f'{val:.1f} BPM', va='center', fontsize=9, color='#444444')
ax.invert_yaxis()
ax.xaxis.grid(True)
ax.set_axisbelow(True)
save('06_tempo_by_cluster.png')

# ── 7. Cluster Sizes (Donut) ──────────────────────────────────────────────────
sizes  = [355, 789, 991, 2695]
total  = sum(sizes)
pcts   = [s/total*100 for s in sizes]

fig, ax = plt.subplots(figsize=(6, 5))
wedges, texts, autotexts = ax.pie(
    sizes, labels=None, colors=C_COLORS, startangle=90,
    autopct='%1.1f%%', pctdistance=0.78,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_color('white')
    at.set_fontweight('bold')
ax.legend(
    [f'{l}\n{s:,} tracks ({p:.1f}%)' for l, s, p in zip(C_SHORT, sizes, pcts)],
    loc='lower center', bbox_to_anchor=(0.5, -0.15),
    ncol=2, fontsize=8.5, frameon=False
)
ax.set_title('Cluster Sizes', pad=16)
save('07_cluster_sizes.png')

# ── 8. Genre Composition — Stacked Bar ───────────────────────────────────────
genre_names = ['electronic','pop','rock','latin','hip-hop','lofi','jazz','ambient','classical','world']
# Rows: [C1, C2, C3, C4]
genre_data = {
    'electronic': [67,  54,  99,  369],
    'pop':        [ 0,  23,  56,  436],
    'rock':       [ 0,   5,  18,  322],
    'latin':      [ 0, 111,  47,  267],
    'hip-hop':    [ 0, 237,   7,  151],
    'lofi':       [19,  11, 266,    2],
    'jazz':       [ 2,   6, 116,   22],
    'ambient':    [73, 103,  58,  125],
    'classical':  [88,   0,  30,    3],
    'world':      [ 8,  13,  77,  130],
}
stack_colors = plt.cm.tab10(np.linspace(0, 1, len(genre_names)))

fig, ax = plt.subplots(figsize=(9, 4.5))
x    = np.arange(4)
bottom = np.zeros(4)
bars_list = []
for gname, color in zip(genre_names, stack_colors):
    vals = np.array(genre_data[gname])
    b = ax.bar(x, vals, bottom=bottom, label=gname, color=color, width=0.55, edgecolor='white', linewidth=0.5)
    bars_list.append(b)
    bottom += vals

ax.set_xticks(x)
ax.set_xticklabels(C_SHORT, fontsize=10)
ax.set_ylabel('Track count')
ax.set_title('Genre Composition of Each Cluster (Top 10 Genres)')
ax.legend(fontsize=8, ncol=2, bbox_to_anchor=(1.01, 1), loc='upper left', frameon=False)
ax.yaxis.grid(True, alpha=0.4)
ax.set_axisbelow(True)
save('08_genre_composition_stacked.png')

# ── 9. Cluster Purity ─────────────────────────────────────────────────────────
purity = [24.8, 30.0, 26.8, 16.2]
dominant = ['classical','hip-hop','lofi','pop']

fig, ax = plt.subplots(figsize=(7.5, 3.2))
bars = ax.bar(C_SHORT, purity, color=C_COLORS, alpha=0.9, width=0.5)
ax.set_ylabel('Dominant genre share (%)')
ax.set_title('Cluster Purity — Dominant Genre\'s Share Within Each Cluster')
ax.set_ylim(0, 40)
for bar, val, dom in zip(bars, purity, dominant):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val}%\n({dom})', ha='center', va='bottom', fontsize=8.5, color='#444444')
ax.yaxis.grid(True, alpha=0.5)
ax.set_axisbelow(True)
save('09_cluster_purity.png')

# ── 10. Match Rate by Popularity Tier ────────────────────────────────────────
tier_labels = ['Overall', 'High-popularity', 'Low-popularity']
tier_vals   = [21.3, 25.4, 19.1]

fig, ax = plt.subplots(figsize=(5.5, 3.5))
bars = ax.bar(tier_labels, tier_vals, color=TIER_COLORS, alpha=0.9, width=0.45)
ax.set_ylabel('Genre match rate (%)')
ax.set_title('Genre Match Rate by Popularity Tier')
ax.set_ylim(0, 35)
ax.axhline(21.3, color='#AAAAAA', linewidth=1, linestyle='--', alpha=0.7)
for bar, val in zip(bars, tier_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f'{val}%', ha='center', va='bottom', fontsize=10, fontweight='semibold')
ax.yaxis.grid(True, alpha=0.4)
ax.set_axisbelow(True)
save('10_match_rate_by_tier.png')

# ── 11. Match Rate by Cluster × Tier ─────────────────────────────────────────
cluster_cats = ['C1\n(hip-hop)','C2\n(classical)','C3\n(lofi)','C4\n(pop)']
high_vals    = [42.9, 64.3,  1.2, 24.4]
low_vals     = [23.2, 23.2, 32.2,  9.3]

x = np.arange(4)
w = 0.32
fig, ax = plt.subplots(figsize=(8, 4))
b1 = ax.bar(x - w/2, high_vals, w, label='High popularity', color=ACCENT, alpha=0.88)
b2 = ax.bar(x + w/2, low_vals,  w, label='Low popularity',  color=ACCENT2, alpha=0.88)
ax.set_xticks(x)
ax.set_xticklabels(cluster_cats, fontsize=9)
ax.set_ylabel('Genre match rate (%)')
ax.set_title('Match Rate by Cluster × Popularity Tier')
ax.legend(fontsize=9)
ax.set_ylim(0, 80)
for bar, val in zip(list(b1) + list(b2), high_vals + low_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
            f'{val}%', ha='center', va='bottom', fontsize=8)
ax.yaxis.grid(True, alpha=0.4)
ax.set_axisbelow(True)
save('11_match_rate_by_cluster_tier.png')

# ── 12. Sonic Identity Spectrum ───────────────────────────────────────────────
sonic_genres = ['wellness','punk','rock','lofi','pop','jazz','afrobeats',
                'classical','folk','latin','electronic','r&b',
                'hip-hop','gaming','world','blues','arabic','ambient']
sonic_pct = [100, 94.6, 93.3, 89.3, 84.7, 79.5, 79.3,
             72.7, 63.2, 62.8, 62.7, 62.0,
             60.0, 58.6, 57.0, 52.3, 49.0, 34.8]

def bar_color(p):
    if p > 80:   return '#4CAF82'
    if p >= 50:  return ACCENT
    return '#E08C6A'

colors = [bar_color(p) for p in sonic_pct]

fig, ax = plt.subplots(figsize=(8, 7))
y = np.arange(len(sonic_genres))
bars = ax.barh(y, sonic_pct, color=colors, alpha=0.88, height=0.6)
ax.set_yticks(y)
ax.set_yticklabels(sonic_genres, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('% of genre tracks in their primary cluster')
ax.set_title('Sonic Identity Spectrum\n% of Each Genre\'s Tracks in Its Primary Cluster')
ax.axvline(80, color='#4CAF82', linewidth=1, linestyle='--', alpha=0.5)
ax.axvline(50, color=ACCENT,    linewidth=1, linestyle='--', alpha=0.5)
for bar, val in zip(bars, sonic_pct):
    ax.text(min(bar.get_width() + 1.0, 102), bar.get_y() + bar.get_height()/2,
            f'{val}%', va='center', fontsize=8.5, color='#444444')
ax.set_xlim(0, 110)

legend_patches = [
    mpatches.Patch(color='#4CAF82', alpha=0.88, label='> 80% — Strong sonic identity'),
    mpatches.Patch(color=ACCENT,    alpha=0.88, label='50–80% — Mixed identity'),
    mpatches.Patch(color='#E08C6A', alpha=0.88, label='< 50% — Cultural / weak sonic'),
]
ax.legend(handles=legend_patches, fontsize=8.5, loc='lower right', frameon=True, framealpha=0.9)
ax.xaxis.grid(True, alpha=0.4)
ax.set_axisbelow(True)
save('12_sonic_identity_spectrum.png')

print(f'\nAll 12 plots saved to: {OUT_DIR}')
