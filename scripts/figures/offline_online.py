"""
Original explanatory figures for the blog post
"Offline to online RL: distribution shift, conservatism, and collapse".

All figures are synthetic / illustrative schematics (no paper screenshots),
styled to match the site palette (Stanford cardinal on white).

Run:  python3 scripts/figures/offline_online.py
Out:  public/blog/assets/offline-to-online-rl/*.svg
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# palette + shared style (matches scripts/figures/flow_diffusion.py)
# ----------------------------------------------------------------------------
CARDINAL = "#8c1515"
SLATE    = "#35618f"
TEAL     = "#2e7d6f"
GOLD     = "#b8860b"
GRAY     = "#9a9a9a"
INK      = "#2a2a2a"
MUTED    = "#6c6c6c"
GRID     = "#e7e7e7"
SPINE    = "#cccccc"
BG       = "none"   # transparent: the page supplies the background

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(_ROOT, "public", "blog", "assets", "offline-to-online-rl")
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
    "axes.labelsize": 12,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 10.5,
    "text.color": INK,
    "legend.frameon": False,
    "legend.fontsize": 10.5,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.9,
})


def clean(ax, grid=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    if not grid:
        ax.grid(False)


def save(fig, name):
    """Write SVG. Vector keeps the figure sharp at any zoom and, with a
    transparent canvas, lets the same asset serve the light and dark themes."""
    name = name.replace(".png", ".svg")
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.12, transparent=True)
    plt.close(fig)
    print("wrote", path)


# ----------------------------------------------------------------------------
# Figure 1 -- the collapse: return vs online steps
# ----------------------------------------------------------------------------
def fig_collapse():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    t = np.linspace(0, 1, 400)
    J0 = 0.60

    dip = 0.46 * np.exp(-((t - 0.16) ** 2) / (2 * 0.10 ** 2))
    recover = 0.32 * (1 / (1 + np.exp(-9 * (t - 0.58))))
    naive = np.clip(J0 - dip + recover, 0.07, 1)

    stable = (J0
              - 0.05 * np.exp(-((t - 0.12) ** 2) / (2 * 0.08 ** 2))
              + 0.27 * (1 / (1 + np.exp(-7 * (t - 0.42)))))

    ax.axhline(J0, ls="--", color=GRAY, lw=1.4)
    ax.text(0.012, J0 + 0.015, r"offline policy  $J(\pi_0)$",
            color=MUTED, fontsize=10, va="bottom")

    ax.plot(t, naive, color=CARDINAL, lw=2.7, label="naive online fine-tuning")
    ax.plot(t, stable, color=SLATE, lw=2.7, label="stable transition")

    # collapse depth
    imin = int(np.argmin(naive))
    tmin, jmin = t[imin], naive[imin]
    ax.annotate("", xy=(tmin, jmin), xytext=(tmin, J0),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
    ax.text(tmin + 0.022, (J0 + jmin) / 2, "collapse\ndepth $\\Delta$",
            color=INK, fontsize=9.5, va="center")

    # recovery time (first return to J0 after the dip)
    after = t > tmin
    cross = t[after][int(np.argmin(np.abs(naive[after] - J0)))]
    y_rec = 0.13
    ax.annotate("", xy=(cross, y_rec), xytext=(0.0, y_rec),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.2))
    ax.text(cross / 2, y_rec - 0.045, r"recovery time  $\tau_{\mathrm{rec}}$",
            color=MUTED, fontsize=9.5, ha="center", va="top")

    ax.set_xlim(0, 1)
    ax.set_ylim(0.04, 0.95)
    ax.set_xlabel("online interaction steps")
    ax.set_ylabel(r"held-out return  $J$")
    ax.set_xticks([])
    ax.set_title("Fine-tuning can wreck a good policy before it helps")
    ax.legend(loc="lower right")
    clean(ax)
    save(fig, "fig1_collapse.png")


# ----------------------------------------------------------------------------
# Figure 2 -- concentrability amplifies the replay residual off support
# ----------------------------------------------------------------------------
def fig_concentrability():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    C = np.logspace(0, 4, 300)
    eps = 0.02  # replay RMS Bellman residual
    err = np.sqrt(C) * eps

    ax.plot(C, err, color=CARDINAL, lw=2.7)
    ax.set_xscale("log")

    ax.axhline(1.0, ls="--", color=GRAY, lw=1.3)
    ax.text(1.15, 1.03, "return scale", color=MUTED, fontsize=9.3, va="bottom")

    ax.scatter([2], [np.sqrt(2) * eps], color=SLATE, s=60, zorder=5, edgecolor="white")
    ax.annotate("in support\n$C_t \\approx 2$", xy=(2, np.sqrt(2) * eps),
                xytext=(3.4, 0.24), color=SLATE, fontsize=9.3,
                arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.0))

    Coff = 2500
    ax.scatter([Coff], [np.sqrt(Coff) * eps], color=CARDINAL, s=60, zorder=5, edgecolor="white")
    ax.annotate("policy leaves support\n$C_t$ blows up", xy=(Coff, np.sqrt(Coff) * eps),
                xytext=(150, 1.18), color=CARDINAL, fontsize=9.3,
                arrowprops=dict(arrowstyle="-|>", color=CARDINAL, lw=1.0))

    ax.set_xlim(1, 1e4)
    ax.set_ylim(0, 1.5)
    ax.set_xlabel(r"concentrability  $C_t$   (log scale)")
    ax.set_ylabel("worst-case on-policy error")
    ax.set_title(r"A tiny replay residual, amplified $\sqrt{C_t}$ off support")
    clean(ax)
    save(fig, "fig2_concentrability.png")


# ----------------------------------------------------------------------------
# Figure 3 -- optimistic bootstrap: the actor maximizes an off-support overestimate
# ----------------------------------------------------------------------------
def fig_optimistic_bootstrap():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    a = np.linspace(-3, 3, 500)

    trueQ = np.exp(-((a - 0.4) ** 2) / (2 * 0.9 ** 2))
    spurious = 1.35 * np.exp(-((a - 2.2) ** 2) / (2 * 0.45 ** 2))
    estQ = trueQ + spurious

    ax.axvspan(-1, 1, color=SLATE, alpha=0.10)
    ax.text(0, 1.72, "data support", color=SLATE, fontsize=10, ha="center", fontweight="bold")

    ax.plot(a, trueQ, color=GRAY, lw=2.4, label=r"true value  $Q^{\pi}$")
    ax.plot(a, estQ, color=CARDINAL, lw=2.7, label=r"learned critic  $\widehat{Q}$")

    ax.scatter([0.4], [1.0], color=GRAY, s=55, zorder=5, edgecolor="white")
    ax.text(0.4, 1.08, "true optimum", color=MUTED, fontsize=9, ha="center", va="bottom")

    astar = a[int(np.argmax(estQ))]
    ax.scatter([astar], [estQ.max()], color=CARDINAL, marker="*", s=280, zorder=6, edgecolor="white")
    # centered above the star (far right), clear of the "data support" label
    ax.annotate("actor's argmax:\noff-support overestimate", xy=(astar, estQ.max() + 0.03),
                xytext=(astar, estQ.max() + 0.24), color=CARDINAL, fontsize=9.3,
                ha="center", va="bottom",
                arrowprops=dict(arrowstyle="-|>", color=CARDINAL, lw=1.1))

    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 2.25)
    ax.set_xlabel(r"action  $a$")
    ax.set_ylabel("value")
    ax.set_yticks([])
    ax.set_title("The actor maximizes the critic, into off-support overestimates")
    ax.legend(loc="upper left")
    clean(ax)
    save(fig, "fig3_optimistic_bootstrap.png")


# ----------------------------------------------------------------------------
# Figure 4 -- pessimism vs calibration (the Cal-QL fix)
# ----------------------------------------------------------------------------
def fig_calibration():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.9), sharey=True)
    Vmu = 100
    panels = [
        (axes[0], "uncalibrated pessimism", 10, 15, 1,
         r"$15 > 10$: actor switches," + "\nunlearns a strong policy"),
        (axes[1], "calibrated  (Cal-QL)", 100, 15, 0,
         r"$100 > 15$: actor keeps" + "\nthe good policy"),
    ]
    for ax, title, offv, explv, sel, note in panels:
        xs = [0, 1]
        vals = [offv, explv]
        ax.bar(xs, vals, width=0.58, color=[SLATE, GOLD], edgecolor="white", zorder=3)
        ax.axhline(Vmu, ls="--", color=GRAY, lw=1.3, zorder=2)
        ax.text(1.52, Vmu + 1, r"true value $V^{\mu}$", color=MUTED, fontsize=9,
                ha="right", va="bottom")
        for x, v in zip(xs, vals):
            ax.text(x, v + 3, f"{v}", ha="center", color=INK, fontsize=11, fontweight="bold")
        # star the actor's pick
        ax.scatter([xs[sel]], [vals[sel] + 13], marker="*", s=200, color=CARDINAL, zorder=5)
        ax.set_xticks(xs)
        ax.set_xticklabels(["offline\naction", "exploratory\naction"], fontsize=9.5)
        ax.set_ylim(0, 122)
        ax.set_title(title, fontsize=11.5)
        ax.text(0.5, -0.30, note, transform=ax.transAxes, ha="center", va="top",
                fontsize=9, color=INK)
        clean(ax, grid=False)
    axes[0].set_ylabel(r"critic value  $\widehat{Q}$")
    fig.suptitle("Pessimism vs calibration", fontweight="bold", fontsize=13, color=INK, y=1.0)
    save(fig, "fig4_calibration.png")


if __name__ == "__main__":
    fig_collapse()
    fig_concentrability()
    fig_optimistic_bootstrap()
    fig_calibration()
    print("done ->", OUT)
