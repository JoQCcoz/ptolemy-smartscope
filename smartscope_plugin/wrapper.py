import sys
# print(sys.path)
# sys.path.insert(0, '/opt/smartscope/ptolemy/')
from ..ptolemy.images import Exposure
from ..ptolemy import algorithms as algorithms
from ..ptolemy import models as models
import torch
from Smartscope.lib.image_manipulations import fourier_crop

def load_model(model_path, cuda=False):
    return algorithms.UNet_Segmenter(64, 9, model_path=model_path, dim_mult_of=1024, cuda=cuda)

def ptolemy_find_holes(image, model_path='weights/211026_unet_9x64_ep6.torchmodel', segmenter=None, cuda=False, height=1024) -> Exposure:
    ex = Exposure(fourier_crop(image,height=height), scale=image.shape[0]/height)
    if segmenter is None:
        segmenter = load_model(model_path,cuda)
    ex.make_mask(segmenter)
    processor = algorithms.MedMag_Process_Mask(edge_tolerance=100)
    ex.process_mask(processor)
    cropper = algorithms.MedMag_Process_Crops()
    ex.get_crops(cropper)
    return ex


def pltolemy_classify_holes(exposure: Exposure) -> Exposure:
    model = models.AveragePoolModel(4, 128)
    model.load_state_dict(torch.load('weights/211214_medmag_128x4_avgpool_e5.torchmodel'))
    wrapper = models.Wrapper(model)
    exposure.score_crops(wrapper, final=False)
    return exposure
