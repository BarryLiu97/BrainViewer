# -*- coding: UTF-8 -*-
"""
@Project : BrainViewer 
@File    : splash.py
@Author  : zheng.liu
@Date    : 2022/3/16 17:00 
"""

import nibabel as nib
import numpy as np
import pyvista as pv
from mne.surface import _marching_cubes as marching_cubes

from .numeric import apply_trans


def check_hemi(hemi):
    if hemi == 'Both':
        return ['lh', 'rh']
    elif 'Left' in hemi or 'lh' in hemi:
        return 'lh'
    elif 'Right' in hemi or 'rh' in hemi:
        return 'rh'
    else:
        return 'other'


def read_fs_surface(surf_path):
    print(f'Loading surface files from {surf_path}')
    coords, faces = nib.freesurfer.read_geometry(surf_path)

    face_nums = np.ones(faces.shape[0]) * 3
    faces = np.c_[face_nums, faces].astype(np.int32)
    return coords, faces


def create_roi_surface(aseg_mgz, roi, lut_path):
    from .freesurfer import read_freesurfer_lut

    aseg_data = np.asarray(aseg_mgz.dataobj)
    vox_mri_t = aseg_mgz.header.get_vox2ras_tkr()

    print(lut_path)
    lut, _, fs_colors = read_freesurfer_lut(lut_path)
    idx = [lut[roi]]

    if len(idx):
        surfs = marching_cubes(aseg_data, idx, smooth=0.85)
        verts = surfs[0][0]
        faces = surfs[0][1]
        roi_color = fs_colors[roi][:-1] / 255
        verts = apply_trans(vox_mri_t, verts)
        nums = np.ones(faces.shape[0]) * 3
        faces = np.c_[nums, faces].astype(np.int32)
        return pv.PolyData(verts, faces), roi_color
    else:
        return None, None
