#NEWFIX: plot_dsig.py: compute pairwise d_sig distances between animations, then cluster via classical MDS and plot the result

import sys, time
sys.path.append("../../")

from animation import fetch_animations, unpack
from id_set import get_id_set, crop_curve_based_on_id
from so3.convert import animation_to_SO3
import so3.log_signature as log_signature
from iisignature import prepare

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

start = time.time()
id_set = get_id_set()
n = len(id_set)

k = 3
d = 69
s = prepare(d, k)

descriptions = {}
log_sigs = {}
for id in id_set:
    subject, animation, description = unpack(fetch_animations(1, animation_id=id))
    curve_full = animation_to_SO3(subject, animation)
    curve = crop_curve_based_on_id(curve_full, id)
    log_sigs[id] = log_signature.curve_log_signature(curve, s)
    descriptions[id] = description
    print("explored:", id, description, "frames:", curve.shape[1], " t=%.1fs" % (time.time()-start))

# Pairwise d_sig distance matrix
D = np.zeros((n, n))
for i in range(n):
    for j in range(i+1, n):
        a_id, b_id = id_set[i], id_set[j]
        dist = log_signature.normalized_linear_distance(log_sigs[a_id], log_sigs[b_id])
        D[i, j] = dist
        D[j, i] = dist

print("Distance matrix computed in %.1fs" % (time.time()-start))

# Classical (metric) MDS via double-centering + eigendecomposition
D2 = D ** 2
J = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * J @ D2 @ J

eigvals, eigvecs = np.linalg.eigh(B)
order = np.argsort(eigvals)[::-1]
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]

k_dims = 2
L = np.diag(np.sqrt(np.clip(eigvals[:k_dims], 0, None)))
coords = eigvecs[:, :k_dims] @ L

# ---- Plot ----
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
GRID = "#e7e6e2"

color_map = {
    'walk':         "#00998A",  # teal
    'run/jog':      "#D6483A",  # coral-red
    'forward jump': "#D99400",  # amber
}
legend_order = ['walk', 'run/jog', 'forward jump']

rng = np.random.default_rng(0)
jitter = rng.normal(0, 0.012, coords.shape)
coords_j = coords + jitter

fig, ax = plt.subplots(figsize=(7.5, 6.5), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

for desc in legend_order:
    mask = [descriptions[id] == desc for id in id_set]
    pts = coords_j[mask]
    ax.scatter(
        pts[:, 0], pts[:, 1],
        s=110, color=color_map[desc],
        edgecolor=SURFACE, linewidth=1.2,
        label=desc, zorder=3,
    )

# Recessive grid, no axis chrome (matches the paper's minimal style)
ax.grid(True, color=GRID, linewidth=1, zorder=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("")
ax.set_ylabel("")

ax.set_title(
    r"Motion capture animations clustered by $d_{sig}$" + "\n(normalized log-signature distance)",
    fontsize=13, color=TEXT_PRIMARY, pad=14, loc="left",
)

ax.legend(loc="upper right", frameon=False, fontsize=10, labelcolor=TEXT_PRIMARY, handletextpad=0.6)

fig.tight_layout()
fig.savefig('dsig_mds_plot.png', dpi=170, facecolor=SURFACE)
print("Saved dsig_mds_plot.png")