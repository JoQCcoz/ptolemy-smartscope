
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import numpy as np
import torch
import os

from Smartscope.lib.Datatypes.base_plugin import Finder
from Smartscope.lib.image.target import Target
from Smartscope.lib.image.targets import Targets

from ..ptolemy.algorithms import BadMedMagError
from .wrapper import ptolemy_find_holes , load_model


class PtolemyHoleFinder(Finder):
    name:str = 'Ptolemy hole finder'
    description: str = 'Hole finder that uses the ptolemy hole finder to find the holes at medium magnification.'
    reference: str = 'https://arxiv.org/abs/2112.01534'
    kwargs: Optional[Dict[str, Any]] = { 
        'model_path': Path(__file__).resolve().parents[1] / 'weights/211026_unet_9x64_ep6.torchmodel',
        'cuda': False if eval(os.getenv('FORCE_CPU')) else torch.cuda.is_available() ,
        'preload_weights': True,
        'height': 1024,
    }
    segmenter: Any = None

    def find_holes(self,image):
        exposure = ptolemy_find_holes(image, model_path=self.kwargs['model_path'],segmenter=self.segmenter,cuda=self.kwargs['cuda'],height=self.kwargs['height'])
        return np.array([exposure.crops.center_coords.y*exposure.scale,exposure.crops.center_coords.x*exposure.scale],dtype=int).transpose() , {'lattice_angle': exposure.rot_ang_deg}      

    def run(self, montage, create_targets_method=Targets.create_targets_from_center)-> Tuple[List[Target], bool, Dict]:
        """Where the main logic for the algorithm is"""
        if self.kwargs['preload_weights'] and self.segmenter is None:
            print('loading model on first use')
            self.segmenter = load_model(self.kwargs['model_path'], self.kwargs['cuda'])
        try:
            ptolemy_image_coords, additional_outputs = self.find_holes(montage.image)
            targets = create_targets_method(ptolemy_image_coords,montage)
            success = True
        except BadMedMagError as err:
            print(f'Could not find holes. {err}')
            targets = []
            success = False
        return targets, success, additional_outputs
