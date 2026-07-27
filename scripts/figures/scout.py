"""
Original explanatory figures for the blog post
"The best curriculum for your easy tasks is the worst for your hard ones".

Two conceptual figures, recreated in the site palette (Stanford cardinal on
warm white). Quantitative results live in tables in the post, not in these
figures; the conflict figure is an explicitly schematic illustration of the
mechanism.

Run:  python3 scripts/figures/scout.py
Out:  public/blog/assets/scout/*.svg
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# ----------------------------------------------------------------------------
# palette + shared style
# ----------------------------------------------------------------------------
CARDINAL = "#8c1515"   # hero accent / hard-in-air group / antistall
SLATE    = "#35618f"   # secondary / easy-on-table group
TEAL     = "#2e7d6f"
GOLD     = "#b8860b"
GRAY     = "#9a9a9a"
INK      = "#2a2a2a"
MUTED    = "#6c6c6c"
GRID     = "#e7e7e7"
SPINE    = "#cccccc"
BG       = "none"   # transparent: the page supplies the background

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(_ROOT, "public", "blog", "assets", "scout")
os.makedirs(OUT, exist_ok=True)

mpl.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 12,
    "axes.edgecolor": SPINE,
    "axes.linewidth": 1.0,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK,
    "axes.labelcolor": INK,
    "axes.labelsize": 11.5,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 10.5,
    "text.color": INK,
    "legend.frameon": False,
    "legend.fontsize": 10.0,
    "grid.color": GRID,
    "grid.linewidth": 0.9,
})


def clean(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)


def save(fig, name):
    """Write SVG. Vector keeps the figure sharp at any zoom and, with a
    transparent canvas, lets the same asset serve the light and dark themes."""
    name = name.replace(".png", ".svg")
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.12, transparent=True)
    plt.close(fig)
    print("wrote", path)


def rbox(ax, x, y, w, h, fc="white", ec=SPINE, lw=1.3, r=0.02, z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       mutation_aspect=2.0, fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(p)
    return p


# ----------------------------------------------------------------------------
# Figure 1 -- SCOUT controls a per-context scaffold frontier
# ----------------------------------------------------------------------------
def fig_method():
    fig, ax = plt.subplots(figsize=(11.2, 5.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 93)
    ax.axis("off")

    # ---- context bank -------------------------------------------------------
    rbox(ax, 5, 22, 39, 53, fc="#fbfbfc", ec=SLATE, lw=1.6, r=0.03, z=1)
    ax.text(6.5, 77.5, "Context bank", fontsize=12.5, fontweight="bold", color=SLATE)

    rows = ["$x_1$", "$x_2$", "$x_3$"]
    ycen = [64, 48, 32]
    frontier = {0: 2, 1: 0, 2: 3}       # row -> active scaffold level
    for ri, (lab, cy) in enumerate(zip(rows, ycen)):
        ax.text(3.0, cy, lab, fontsize=11, color=INK, ha="center", va="center")
        for c in range(5):
            cx = 11 + c * 7.2
            active = (frontier[ri] == c)
            fc = CARDINAL if active else "white"
            ec = CARDINAL if active else "#d7d7d7"
            rbox(ax, cx - 3, cy - 4.3, 6, 8.6, fc=fc, ec=ec, lw=1.4, r=0.02, z=3)
            ax.text(cx, cy, f"$\\ell{{=}}{c}$", fontsize=9.5, ha="center", va="center",
                    color="white" if active else "#7a7a7a",
                    fontweight="bold" if active else "normal", zorder=4)

    # scaffold axis legend under the bank
    ax.annotate("", xy=(40, 17.5), xytext=(8, 17.5),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1))
    ax.text(8, 14.0, "$\\ell{=}0$  target start", fontsize=8.8, color=MUTED, ha="left")
    ax.text(40, 14.0, "$\\ell{=}L$  most assistance", fontsize=8.8, color=MUTED, ha="right")
    ax.text(24, 8.6, "shaded = active frontier $f_x$: starts at $\\ell{=}L$, moves toward $\\ell{=}0$",
            fontsize=8.6, color=CARDINAL, ha="center", style="italic")

    # ---- learner ------------------------------------------------------------
    rbox(ax, 52, 45, 17, 18, fc="#fbfbfc", ec=SPINE, lw=1.5, r=0.04, z=2)
    ax.text(60.5, 58.5, "Learner", fontsize=12, fontweight="bold", ha="center", color=INK)
    ax.text(60.5, 53.6, "rollout & update", fontsize=9.8, ha="center", color=INK)
    ax.text(60.5, 49.2, "SAC+HER · SAC · PPO", fontsize=9.0, ha="center", color=MUTED, style="italic")

    # bank -> learner
    ax.annotate("", xy=(51.4, 54), xytext=(44.3, 54),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    ax.text(47.8, 56.4, "sample $(x, f_x)$", fontsize=9.3, ha="center", color=INK)

    # learner -> held-out eval (dashed)
    rbox(ax, 51, 20, 19, 11, fc="white", ec=SPINE, lw=1.3, r=0.05, z=2)
    ax.text(60.5, 25.5, "held-out eval\n(only $\\ell{=}0$)", fontsize=9.4, ha="center",
            va="center", color=MUTED)
    ax.annotate("", xy=(60.5, 31.2), xytext=(60.5, 44.6),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.3, ls=(0, (4, 3))))
    ax.text(62.4, 38, "$\\ell{=}0$", fontsize=8.8, color=MUTED, ha="left")

    # ---- controller ---------------------------------------------------------
    rbox(ax, 72, 34, 27, 31, fc="#fbfbfc", ec=CARDINAL, lw=1.6, r=0.04, z=2)
    ax.text(85.5, 60.5, "SCOUT controller", fontsize=12, fontweight="bold", ha="center", color=CARDINAL)
    rules = [
        (55.5, "$s > \\tau_{hi}$", "advance ($\\ell{-}1$)", INK),
        (50.8, "$s < \\tau_{lo}$", "retreat ($\\ell{+}1$)", INK),
        (46.1, "stale, mid", "antistall ($\\ell{-}1$)", CARDINAL),
        (41.4, "otherwise", "hold", INK),
    ]
    for y, cond, act, col in rules:
        ax.text(73.6, y, cond, fontsize=9.3, ha="left", va="center", color=INK)
        ax.text(81.6, y, "→", fontsize=9.3, ha="center", va="center", color=MUTED)
        ax.text(83.2, y, act, fontsize=9.3, ha="left", va="center", color=col,
                fontweight="bold" if col == CARDINAL else "normal")
    ax.text(85.5, 37.2, "success only · no critics or demos",
            fontsize=8.2, ha="center", color=MUTED, style="italic")

    # learner -> controller
    ax.annotate("", xy=(71.4, 54), xytext=(69.3, 54),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    ax.text(70.5, 56.4, "success $s$", fontsize=9.0, ha="center", color=INK)

    # controller -> bank feedback (elbow over the top)
    ax.plot([85.5, 85.5], [65, 88], color=INK, lw=1.6, zorder=1)
    ax.plot([85.5, 24.5], [88, 88], color=INK, lw=1.6, zorder=1)
    ax.annotate("", xy=(24.5, 75.3), xytext=(24.5, 88),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    ax.text(55, 90.2, "update each frontier $f_x$", fontsize=9.6, ha="center", color=INK)

    save(fig, "fig1_frontiers.png")


# ----------------------------------------------------------------------------
# Figure 2 -- the pacing conflict (schematic)
# ----------------------------------------------------------------------------
def fig_conflict():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.6, 4.3))
    t = np.linspace(0, 1, 300)
    L = 4.0

    def easy(t):     # needs assistance removed fast
        return L * np.exp(-6.5 * t)

    def hard(t):     # needs assistance retained, removed late
        return L * (1 - 1 / (1 + np.exp(-13 * (t - 0.72))))

    # ---- (a) one global pace cannot serve both ------------------------------
    glob = L * (1 - t)                     # a single compromise schedule
    axL.plot(t, easy(t), color=SLATE, lw=2.4)
    axL.plot(t, hard(t), color=CARDINAL, lw=2.4)
    axL.plot(t, glob, color=INK, lw=1.8, ls=(0, (5, 3)))

    # shade where the global schedule falls below what the hard group needs
    axL.fill_between(t, np.minimum(glob, hard(t)), hard(t),
                     where=(hard(t) > glob), color=CARDINAL, alpha=0.12)
    axL.text(0.40, 3.58, "hard group needs\nlong assistance", color=CARDINAL,
             fontsize=9.0, ha="left", va="top")
    axL.text(0.30, 0.95, "easy group needs\nfast removal", color=SLATE,
             fontsize=9.0, ha="left", va="bottom")
    axL.text(0.055, 1.35, "one global\nschedule", color=INK, fontsize=9.0, ha="left")
    axL.annotate("falls below what the\nhard group needs\n→ abandons it",
                 xy=(0.66, 0.5 * (glob[198] + hard(t)[198])), xytext=(0.99, 3.35),
                 fontsize=9.0, color=CARDINAL, ha="right", va="top",
                 arrowprops=dict(arrowstyle="-|>", color=CARDINAL, lw=1.1,
                                 connectionstyle="arc3,rad=0.25"))
    axL.set_title("(a)  One global pace cannot serve both", loc="left")
    _pace_axes(axL, L)

    # ---- (b) SCOUT: a separate frontier per context -------------------------
    rng = np.random.default_rng(0)
    for _ in range(3):
        axL_noise = 0.05 * rng.standard_normal(t.size).cumsum()
        axR.plot(t, np.clip(easy(t) + axL_noise, 0, L), color=SLATE, lw=0.7, alpha=0.18)
        axR.plot(t, np.clip(hard(t) + 0.05 * rng.standard_normal(t.size).cumsum(), 0, L),
                 color=CARDINAL, lw=0.7, alpha=0.18)
    axR.plot(t, easy(t), color=SLATE, lw=2.6)
    axR.plot(t, hard(t), color=CARDINAL, lw=2.6)
    axR.text(0.40, 3.58, "hard in-air\nfrontier", color=CARDINAL, fontsize=9.2,
             ha="left", va="top")
    axR.text(0.235, 0.95, "easy on-table\nfrontier", color=SLATE, fontsize=9.2,
             ha="left", va="bottom")
    axR.annotate("each context sets its\nown pace from its\nown success signal",
                 xy=(0.45, 2.1), xytext=(0.99, 1.75),
                 fontsize=9.0, color=INK, ha="right", va="center",
                 arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1,
                                 connectionstyle="arc3,rad=-0.2"))
    axR.set_title("(b)  SCOUT: a separate frontier per context", loc="left")
    _pace_axes(axR, L)

    fig.tight_layout(w_pad=2.2)
    save(fig, "fig2_conflict.png")


def _pace_axes(ax, L):
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.15, L + 0.15)
    ax.set_xlabel("training progress")
    ax.set_ylabel("scaffold level  (assistance)")
    ax.set_yticks([0, L])
    ax.set_yticklabels(["$\\ell{=}0$\ntarget", "$\\ell{=}L$\nassisted"])
    ax.set_xticks([])
    clean(ax)


def fig_tile():
    """Compact project-card infographic: the per-context frontier grid motif."""
    from matplotlib.patches import FancyBboxPatch as _Box
    fig, ax = plt.subplots(figsize=(4.0, 3.15))
    ax.set_xlim(0, 62)
    ax.set_ylim(0, 49)
    ax.set_aspect("equal")
    ax.axis("off")

    rows, cols = 4, 6
    active = [4, 2, 3, 1]          # active frontier level per context (varied pacing)
    cell, gap = 6.6, 1.7
    x0, y0 = 8, 10

    for r in range(rows):
        cy = y0 + (rows - 1 - r) * (cell + gap)
        for c in range(cols):
            cx = x0 + c * (cell + gap)
            act = (active[r] == c)
            box = _Box((cx, cy), cell, cell,
                       boxstyle="round,pad=0,rounding_size=1.4", mutation_aspect=1,
                       fc=CARDINAL if act else "none",
                       ec=CARDINAL if act else "#d0d0d0",
                       lw=1.8 if act else 1.4, zorder=3)
            ax.add_patch(box)

    grid_right = x0 + (cols - 1) * (cell + gap) + cell
    # direction of assistance removal: assisted (right) -> target (left)
    ax.annotate("", xy=(x0 - 1.5, 5.0), xytext=(grid_right, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.8))

    fig.savefig(os.path.join(OUT, "tile.png"), dpi=170, bbox_inches="tight",
                pad_inches=0.15, transparent=True)
    plt.close(fig)
    print("wrote", os.path.join(OUT, "tile.png"))


def fig_tile_schematic():
    """Project-card tile: the diverging-frontiers schematic (panel b) standalone."""
    fig, ax = plt.subplots(figsize=(5.3, 4.0))
    t = np.linspace(0, 1, 300)
    L = 4.0
    easy = L * np.exp(-6.5 * t)
    hard = L * (1 - 1 / (1 + np.exp(-13 * (t - 0.72))))

    rng = np.random.default_rng(0)
    for _ in range(3):
        ax.plot(t, np.clip(easy + 0.05 * rng.standard_normal(t.size).cumsum(), 0, L),
                color=SLATE, lw=0.7, alpha=0.18)
        ax.plot(t, np.clip(hard + 0.05 * rng.standard_normal(t.size).cumsum(), 0, L),
                color=CARDINAL, lw=0.7, alpha=0.18)
    ax.plot(t, easy, color=SLATE, lw=2.8)
    ax.plot(t, hard, color=CARDINAL, lw=2.8)
    ax.text(0.12, 3.58, "hard in-air\nfrontier", color=CARDINAL, fontsize=10.5,
            ha="left", va="top", fontweight="bold")
    ax.text(0.235, 0.95, "easy on-table\nfrontier", color=SLATE, fontsize=10.5,
            ha="left", va="bottom", fontweight="bold")
    ax.annotate("each context sets its\nown pace from its\nown success signal",
                xy=(0.45, 2.1), xytext=(0.99, 1.75),
                fontsize=9.5, color=INK, ha="right", va="center",
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1,
                                connectionstyle="arc3,rad=-0.2"))
    ax.set_title("SCOUT: a separate frontier per context", loc="center", pad=10)
    _pace_axes(ax, L)
    fig.savefig(os.path.join(OUT, "tile_schematic.svg"), bbox_inches="tight",
                pad_inches=0.12, facecolor=BG)
    plt.close(fig)
    print("wrote", os.path.join(OUT, "tile_schematic.png"))


def fig_tile_curves():
    """Alternative project-card tile: two diverging frontiers, text-free."""
    fig, ax = plt.subplots(figsize=(4.0, 3.15))
    t = np.linspace(0, 1, 300)
    L = 4.0
    easy = L * np.exp(-6.5 * t)
    hard = L * (1 - 1 / (1 + np.exp(-13 * (t - 0.72))))
    ax.fill_between(t, easy, hard, color=CARDINAL, alpha=0.07, zorder=1)
    ax.plot(t, hard, color=CARDINAL, lw=5.5, solid_capstyle="round", zorder=3)
    ax.plot(t, easy, color=SLATE, lw=5.5, solid_capstyle="round", zorder=3)
    ax.scatter([0], [L], s=60, color="#7a7a7a", zorder=4)      # shared assisted start
    ax.scatter([t[-1]], [easy[-1]], s=55, color=SLATE, zorder=4)
    ax.scatter([t[-1]], [hard[-1]], s=55, color=CARDINAL, zorder=4)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.3, L + 0.3)
    ax.axis("off")
    fig.savefig(os.path.join(OUT, "tile_curves.png"), dpi=170, bbox_inches="tight",
                pad_inches=0.15, transparent=True)
    plt.close(fig)
    print("wrote", os.path.join(OUT, "tile_curves.png"))


if __name__ == "__main__":
    # Only the figures the post actually uses are generated by default.
    # fig_method / fig_tile / fig_tile_curves remain defined above as
    # alternative designs, but are intentionally not regenerated.
    fig_conflict()          # fig2_conflict.png  (schematic in the conflict section)
    fig_tile_schematic()    # tile_schematic.png (project-card tile)
    print("done ->", OUT)
