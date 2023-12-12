# -*- coding: UTF-8 -*-
"""
@Project : BrainViewer 
@File    : splash.py
@Author  : zheng.liu
@Date    : 2022/3/8 23:44 
"""

import numpy as np

from .config import DEFAULT_COLOR_LUT


def read_freesurfer_lut(fname=''):
    """Read a Freesurfer-formatted LUT.
    Parameters
    ----------
    fname : str | None
        The filename. Can be None to read the standard Freesurfer LUT.
    Returns
    -------
    atlas_ids : dict
        Mapping from label names to IDs.
    colors : dict
        Mapping from label names to colors.
    """
    fname = fname if fname else DEFAULT_COLOR_LUT
    print(f'Color Lut: {fname}')
    lut = _get_lut(fname)
    names, ids = lut['name'], lut['id']
    colors = np.array([lut['R'], lut['G'], lut['B'], lut['A']], int).T
    atlas_ids = dict(zip(names, ids))
    ids_atlas = dict(zip(ids, names))
    colors = dict(zip(names, colors))
    return atlas_ids, ids_atlas, colors


def _get_lut(fname=''):
    """Get a FreeSurfer LUT."""
    fname = fname if fname else DEFAULT_COLOR_LUT
    dtype = [('id', '<i8'), ('name', 'U'),
             ('R', '<i8'), ('G', '<i8'), ('B', '<i8'), ('A', '<i8')]
    lut = {d[0]: list() for d in dtype}
    with open(fname, 'r') as fid:
        for line in fid:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            line = line.split()
            if len(line) != len(dtype):
                raise RuntimeError(f'LUT is improperly formatted: {fname}')
            for d, part in zip(dtype, line):
                lut[d[0]].append(part)
    lut = {d[0]: np.array(lut[d[0]], dtype=d[1]) for d in dtype}
    assert len(lut['name']) > 0
    return lut
