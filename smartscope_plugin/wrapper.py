import sys
# print(sys.path)
# sys.path.insert(0, '/opt/smartscope/ptolemy/')
from ptolemy.images import Exposure
import ptolemy.algorithms as algorithms
import ptolemy.models as models
import torch
from Smartscope.lib.image_manipulations import fourier_crop


# class SmartScopePtolemy:


def ptolemy_find_holes(montage, model_path='weights/211026_unet_9x64_ep6.torchmodel', cuda=True, height=1024) -> Exposure:
    ex = Exposure(fourier_crop(montage.image,height=height), scale=montage.shape_x/height)

    segmenter = algorithms.UNet_Segmenter(64, 9, model_path=model_path, dim_mult_of=1024, cuda=cuda)
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
