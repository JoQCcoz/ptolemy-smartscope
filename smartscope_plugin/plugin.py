from Smartscope.lib.Datatypes.base_plugin import Finder
from Smartscope.lib.montage import create_targets_from_center, Target
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import numpy as np


class PtolemyHoleFinder(Finder):
    description: str = 'Hole finder that uses the ptolemy hole finder to find the holes at medium magnification.'
    reference: str = 'https://arxiv.org/abs/2112.01534'
    kwargs: Optional[Dict[str, Any]] = { 
        'model_path': Path(__file__).resolve().parents[1] / 'weights/211026_unet_9x64_ep6.torchmodel',
        'cuda': False,
        'height': 1024,
    }

    def run(self, montage, create_targets_method=create_targets_from_center)-> Tuple[List[Target], bool, Dict]:
        """Where the main logic for the algorithm is"""
        from .wrapper import ptolemy_find_holes         
        exposure = ptolemy_find_holes(montage, **self.kwargs)
        ptolemy_image_coords = np.array([exposure.crops.center_coords.y*exposure.scale,exposure.crops.center_coords.x*exposure.scale],dtype=int).transpose()
        targets = create_targets_method(ptolemy_image_coords,montage)
        return targets, True, {'lattice_angle': exposure.rot_ang_deg}
