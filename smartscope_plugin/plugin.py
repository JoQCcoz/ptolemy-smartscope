from Smartscope.lib.Datatypes.base_plugin import Finder, TargetClass
from typing import Optional, Dict, Any
import sys
from pathlib import Path


class PtolemyPlugin(Finder):
    # importPaths: Union[str, List] = [os.path.join(__file__,'../')]
    kwargs: Optional[Dict[str, Any]] = { 
        'model_path': Path(__file__).resolve().parents[1] / 'weights/211026_unet_9x64_ep6.torchmodel',
        'cuda': False
    }

    def run(self, *args, **kwargs):
        """Where the main logic for the algorithm is"""
        from .wrapper import ptolemy_find_holes 
        
        
        exposure = ptolemy_find_holes(*args,**kwargs, **self.kwargs)
        print(exposure.__dict__)
        # module = importlib.import_module(self.module)
        # function = getattr(module, self.method)
        # output = function(*args, **kwargs, **self.kwargs)
        output = 'hello'
        print(output)
        return output
