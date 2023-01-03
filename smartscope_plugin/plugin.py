from Smartscope.lib.Datatypes.base_plugin import Finder
from Smartscope.lib.montage import create_targets_from_center, Target
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import numpy as np
from .wrapper import ptolemy_find_holes 


class PtolemyHoleFinder(Finder):
    name:str = 'Ptolemy hole finder'
    description: str = 'Hole finder that uses the ptolemy hole finder to find the holes at medium magnification.'
    reference: str = 'https://arxiv.org/abs/2112.01534'
    kwargs: Optional[Dict[str, Any]] = { 
        'model_path': Path(__file__).resolve().parents[1] / 'weights/211026_unet_9x64_ep6.torchmodel',
        'cuda': False,
        'height': 1024,
    }

    def find_holes(self,image):
        exposure = ptolemy_find_holes(image, **self.kwargs)
        return np.array([exposure.crops.center_coords.y*exposure.scale,exposure.crops.center_coords.x*exposure.scale],dtype=int).transpose() , {'lattice_angle': exposure.rot_ang_deg}      

    def run(self, montage, create_targets_method=create_targets_from_center)-> Tuple[List[Target], bool, Dict]:
        """Where the main logic for the algorithm is"""
        ptolemy_image_coords, additional_outputs = self.find_holes(montage.image)
        targets = create_targets_method(ptolemy_image_coords,montage)
        return targets, True, additional_outputs
