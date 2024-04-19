from .plugin import PtolemyHoleFinder
from Smartscope.lib.image_manipulations import extract_from_image
import numpy as np
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def alignToHolePtolemy(scope,params,instance, content:Dict, *args, **kwargs):
    """
    Aligns the hole using Ptolemy instead of a hole reference image. Slower but very precise
    """

    from Smartscope.core.db_manipulations import set_or_update_refined_finder
    iteration = 0
    while iteration < 2:
        scope.acquire_medium_mag()
        pixel_size = scope.get_image_settings()
        image, shape_x, shape_y, _, _, pixel_size = scope.buffer_to_numpy()
        coords, _ = PtolemyHoleFinder().find_holes(image)
        coords_from_center = coords - np.array([shape_x,shape_y])//2
        dist_to_center = np.sqrt(np.sum(np.power(coords_from_center,2),axis=1))
        closest_index = np.argmin(dist_to_center)
        if dist_to_center[closest_index] * pixel_size / 1_000 < 0.8:
            set_or_update_refined_finder(instance.pk,*scope.report_stage())
            break
        iteration += 1
        scope.align_to_coord(coords_from_center[closest_index])

def createHoleRefPtolemy(scope,params,instance, content:Dict, *args, **kwargs):
    """Uses Ptolemy on a view mag image, finds the holes, extracts and average them into a hole reference. The resulting reference will be copied in buffer T."""
    if scope.has_hole_ref:
        return
    scope.acquire_medium_mag()
    image, _, _, _, _, pixel_size = scope.buffer_to_numpy()
    coords, _ = PtolemyHoleFinder().find_holes(image)
    print(f'Found {len(coords)} holes, pixel_size= {pixel_size}')
    stack = None
    for coord in coords:
        crop, _, _, _, overLimits = extract_from_image(image,coord,pixel_size*10,box_size=instance.grid_id.holeType.hole_size*1.5)
        crop = crop.reshape((crop.shape + (1,)))
        print(f'Crop {crop.shape} is overlimits: {overLimits}. Stack created: {stack is not None}')
        if overLimits:
            continue
        if stack is None:
            stack = crop
            continue
        stack = np.concatenate((stack,crop),axis=2)
    average = np.mean(stack,axis=2).astype(image.dtype)
    scope.numpy_to_buffer(average)
    scope.hole_crop_size = average.shape[0]
    scope.has_hole_ref = True



protocolCommandsFactory= dict(
    alignToHolePtolemy=alignToHolePtolemy,
    createHoleRefPtolemy=createHoleRefPtolemy,
)