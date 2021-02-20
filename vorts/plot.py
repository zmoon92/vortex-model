"""
Plotting routines
"""

from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np


# Tableau's newer version of tab10
# https://www.tableau.com/about/blog/2016/7/colors-upgrade-tableau-10-56782
_NEW_TAB10 = [
    "#4e79a7",
    "#f28e2b",
    "#e15759",
    "#76b7b2",
    "#59a14f",
    "#edc948",
    "#b07aa1",
    "#ff9da7",
    "#9c755f",
    "#bab0ac",
]

# TODO: PlotMethods object that could allow .plot_type(...) and ("plot_type", ...) and be attached to the Model? (like pandas/xarray)

# TODO: should plotters return `fig, ax`, or just `ax`? or something else? xarray returns the set of matplotlib artists

# TODO: routine to determine system rotation; plot trajectories with respect to this rotating ref frame

def plot_vorton_trajectories(ds, **kwargs):
    """Plot lines: one for each vorton's trajectory.

    Parameters
    ----------
    ds : xarray.Dataset
        `hist` attribute of the model instance.
    **kwargs
        Passed on to [`plt.subplots()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
    """
    # select vortons
    iv = ds.G != 0
    ds = ds.sel(v=iv)

    fig, ax = plt.subplots(**kwargs)

    color_cycle = cycler(color=_NEW_TAB10)
    ax.set_prop_cycle(color_cycle)

    # could be done with one plot command, but...
    nv = ds.v.size
    for i in range(nv):
        ts_i = ds.isel(v=i)
        x = ts_i.x
        y = ts_i.y
        l, = ax.plot(x, y, lw=0.5, alpha=0.5)
        # highlight starting position
        ax.plot(x[0], y[0], 'o', c=l.get_color())


    ax.set(
        xlabel="$x$",
        ylabel="$y$",
        title="Vortons",
    )

    ax.set_aspect("equal", "box")

    fig.tight_layout()


# note much shared with vorton traj plot
def plot_tracer_trajectories(ds, **kwargs):
    """Plot tracer trajectories.

    Parameters
    ----------
    ds : xarray.Dataset
        `hist` attribute of the model instance.
    **kwargs
        Passed on to [`plt.subplots()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
    """
    # select tracers
    it = ds.G == 0  # tracers boolean
    ds = ds.sel(v=it)

    fig, ax = plt.subplots(**kwargs)

    nv = ds.v.size
    for i in range(nv):
        ts_i = ds.isel(v=i)
        x = ts_i.x
        y = ts_i.y
        ax.plot(x, y, c="0.5", lw=0.5, alpha=0.5)

    ax.set(
        xlabel="$x$",
        ylabel="$y$",
        title="Tracers",
    )

    ax.set_aspect("equal", "box")

    fig.tight_layout()


def ps_data(ds, iv_ref=0, *, xtol=1e-2):
    """From full set of data, extract data corresponding to times for the Poincare Section.

    We find the times when the reference vorton is in a certain place
    or passing through a certain plane (TODO).

    Parameters
    ----------
    ds : xarray.Dataset
        `hist` attribute of the model instance.
    iv_ref : int
        Index of the vorton to use for reference.
    xtol : float
        Tolerance to use when searching for timesteps when the reference vorton is in its original position.

    Returns
    -------
    xarray.Dataset
        Only consisting of the timesteps when the reference vorton is approximately in the desired position.
    """
    # initial position
    r0_ref = ds.isel(t=0, v=iv_ref)
    x0 = r0_ref.x#.values
    # y0 = r0_ref.y#.values

    # xtol = 1e-2
    # ytol = 1e-2

    # TODO: need to be more careful. should make wrt. center-of-vort, ...
    # cond = (np.abs(ds.x - x0) <= xtol) & (np.abs(ds.y - y0) <= ytol) & (ds.v == iv_ref)
    # cond = (np.abs(ds.x - x0) <= xtol) & (ds.v == iv_ref)
    cond = (np.abs(ds.x - x0) <= xtol) & (ds.y > 0) & (ds.v == iv_ref)
    ds_ps_ref = ds.where(cond, drop=True)
    t_ps = ds_ps_ref.t  # ps times

    ds_ps = ds.sel(t=t_ps)

    return ds_ps


def plot_ps(ds, *, iv_ref=0, **kwargs):
    """Poincare section plot.

    Here using the data set of all data.

    Parameters
    ----------
    ds : xarray.Dataset
        Output from `ps_data`.
    iv_ref : int
        Index of the vorton to use for reference.
    **kwargs
        Passed on to either `ps_data()` (if applicable) or [`plt.subplots()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)

    See also
    --------
    ps_data
    """
    # subset
    # first take only the kwargs we want
    # TODO: there's got to be a less awkward way to do this...
    ps_data_kwarg_keys = ["xtol", ]  # TODO: could get using `inspect`
    ps_data_kwargs = {k: kwargs.pop(k) for k in ps_data_kwarg_keys if k in kwargs}
    ds = ps_data(ds, iv_ref, **ps_data_kwargs)

    # select tracers
    it = ds.G == 0
    ds = ds.sel(v=it)

    fig, ax = plt.subplots(**kwargs)

    # TODO: (optionally?) plot vorton initial positions / positions at reference time?

    # TODO: algo for choosing marker size and alpha (but also allow passing in)

    # plot all
    x = ds.x  # (nt, nv)
    y = ds.y
    ax.plot(x, y, ".", c="0.35", ms=0.2, alpha=0.5, mew=0)

    ax.set(
        xlabel="$x$",
        ylabel="$y$",
        title="Poincaré map (tracers)",
    )

    ax.set_aspect("equal", "box")

    fig.tight_layout()


def frame_only(ax=None, *, keep_ax_labels=True, keep_title=True):
    """Remove ticks and tick labels from `ax` (uses current by default)."""
    if ax is None:
        ax = plt.gca()

    ax.tick_params(
        axis="both",
        which="both",  # 'major', 'minor', or 'both'
        bottom=False,
        labelbottom=False,
        left=False,
        labelleft=False,
        top=False,
        labeltop=False,
        right=False,
        labelright=False,
    )

    if not keep_ax_labels:
        ax.set(
            xlabel="",
            ylabel="",
        )

    if not keep_title:
        ax.set_title("")


def remove_frame(ax=None, *, keep_title=True):
    """Remove ticks, tick labels, and frame (spines) from `ax` (uses current by default)."""
    if ax is None:
        ax = plt.gca()

    frame_only(ax, keep_ax_labels=False, keep_title=keep_title)

    ax.set(
        frame_on=False,
    )