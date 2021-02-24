# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Poincaré section plots
#
# The Poincaré section plotting routine has many fun options for making cool-looking figures.

# %%
import sys
sys.path.append("../")

from ipywidgets import interact
import matplotlib.pyplot as plt
import numpy as np

import vorts

# %% [markdown]
# ## Create and run
#
# We need a good amount of tracers and a long enough run that there are (preferably) multiple full rotations of the system. Also, we want a small enough time step that we have enough coverage of the times when the vortons return to their original positions.

# %%
m = vorts.Model_py(
    vortons=vorts.Vortons.regular_polygon(5),
    tracers=vorts.Tracers.grid(20, 20, dxy=1.7),
    dt=0.05,
    nt=1e4,
).run()

# %% [markdown]
# ## Plotting options

# %% [markdown]
# ### No property cycling
#
# With the default settings, we get grayscale with small partially-transparent markers.

# %%
shared = dict(figsize=(6, 6), xtol=0.02, title=None)
m.plot("poincare", ms=2, **shared)

# %% [markdown]
# ### Color cycling

# %%
m.plot("poincare", ms=2.5, alpha=0.8, c=["g", "b"], **shared)

# %% [markdown]
# ### Color, marker size, and marker alpha cycling
#
# The default is to cycle the marker properties by tracer. If we cycle by time instead, the properties are more evenly distributed in space.

# %%
for cycle_by in ["vorton", "time"]:
    m.plot("poincare",
        ms=[1, 2, 4],
        c=plt.cm.rainbow(np.linspace(0, 1, 30)),
        alpha=[0.6, 0.85],
        cycle_by=cycle_by,
        **shared
    )