# Reads the completed similarity table (SRVT-only `distance`, SRVT+DP
# `dp_distance`, and signature-based `signature_distance`) directly from
# the database and plots the MDS clustering for Figures 1, 2, and 3 — no
# recomputation needed.

import sqlite3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DB = "../../animation/db/mocap.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT animation_id, description FROM animation ORDER BY animation_id;")
descriptions = dict(cur.fetchall())
id_set = sorted(descriptions.keys())
n = len(id_set)
idx = {aid: i for i, aid in enumerate(id_set)}

cur.execute("SELECT animation_id1, animation_id2, distance, dp_distance, signature_distance FROM similarity;")
rows = cur.fetchall()

D_dist = np.zeros((n, n))
D_dp = np.zeros((n, n))
D_sig = np.zeros((n, n))
for a, b, dist, dp, sig in rows:
    i, j = idx[a], idx[b]
    D_dist[i, j] = dist
    D_dp[i, j] = dp
    D_sig[i, j] = sig

def classical_mds(D, k_dims=2):
    D2 = D ** 2
    n_ = D2.shape[0]
    J = np.eye(n_) - np.ones((n_, n_)) / n_
    B = -0.5 * J @ D2 @ J
    eigvals, eigvecs = np.linalg.eigh(B)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    L = np.diag(np.sqrt(np.clip(eigvals[:k_dims], 0, None)))
    return eigvecs[:, :k_dims] @ L

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
GRID = "#e7e6e2"
color_map = {
    'walk':         "#00998A",
    'run/jog':      "#D6483A",
    'forward jump': "#D99400",
}
legend_order = ['walk', 'run/jog', 'forward jump']

def make_plot(D, title, filename, seed):
    coords = classical_mds(D)
    rng = np.random.default_rng(seed)
    coords_j = coords + rng.normal(0, 0.012 * (coords.std() + 1e-9), coords.shape)

    fig, ax = plt.subplots(figsize=(7.5, 6.5), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    for desc in legend_order:
        mask = [descriptions[aid] == desc for aid in id_set]
        pts = coords_j[mask]
        ax.scatter(pts[:, 0], pts[:, 1], s=110, color=color_map[desc],
                   edgecolor=SURFACE, linewidth=1.2, label=desc, zorder=3)

    ax.grid(True, color=GRID, linewidth=1, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=13, color=TEXT_PRIMARY, pad=14, loc="left")
    ax.legend(loc="lower right", frameon=False, fontsize=10, labelcolor=TEXT_PRIMARY, handletextpad=0.6)

    fig.tight_layout()
    fig.savefig(filename, dpi=170, facecolor=SURFACE)
    print("Saved", filename)

make_plot(D_sig, "Signature distance (via similarity.py + signature.py)\n(same database-coupled workflow the repo originally intended)", "fig1_signature_db.png", seed=0)
make_plot(D_dist, "SRVT distance only, no time-alignment\n(no dynamic programming)", "fig2_srvt_only.png", seed=1)
make_plot(D_dp, "SRVT + dynamic-programming time-alignment\n(the paper's established baseline)", "fig3_srvt_dp.png", seed=2)
