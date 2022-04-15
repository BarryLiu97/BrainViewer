# -*- coding: UTF-8 -*-
"""
@Project ：iEEGTool 
@File    ：surface.py
@Author  ：Barry
@Date    ：2022/3/16 17:00 
"""
import pathlib
import os.path as op
import numpy as np
import pyvista as pv
import nibabel as nib

from utils.numeric import apply_trans
from utils.marching_cubes import marching_cubes


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
    # surf = pathlib.Path(surf_path).suffix
    print(f'Loading surface files from {surf_path}')
    coords, faces = nib.freesurfer.read_geometry(surf_path)

    face_nums = np.ones(faces.shape[0]) * 3
    faces = np.c_[face_nums, faces].astype(np.int32)
    return coords, faces

def create_roi_surface(aseg_path, rois):
    from utils.freesurfer import read_freesurfer_lut

    print(f'loading {aseg_path}')
    aseg_mgz = nib.load(aseg_path)
    aseg_data = np.asarray(aseg_mgz.dataobj)
    vox_mri_t = aseg_mgz.header.get_vox2ras_tkr()

    if 'vep' not in aseg:
        lut_name = 'utils/FreeSurferColorLUT.txt'
    else:
        lut_name = 'utils/VepFreeSurferColorLut.txt'

    lut, fs_colors = read_freesurfer_lut(lut_name)
    if isinstance(rois, str):
        rois = [rois]
    roi2color = {roi: fs_colors[roi][:-1] / 255 for roi in rois}
    idx = [lut[roi] for roi in rois]

    print('Running marching cubes')
    if len(idx):
        surfs, _ = marching_cubes(aseg_data, idx, smooth=0.85)

        roi_mesh_color = {}
        for roi, (verts, faces) in zip(rois, surfs):
            roi_color = roi2color[roi]
            verts = apply_trans(vox_mri_t, verts)
            nums = np.ones(faces.shape[0]) * 3
            faces = np.c_[nums, faces].astype(np.int32)
            roi_mesh_color[roi] = [pv.PolyData(verts, faces), roi_color]
        return roi_mesh_color
    else:
        return None

