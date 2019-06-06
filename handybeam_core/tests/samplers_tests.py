## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam_core directory

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir)
sys.path.append('../.')


## Class


class SamplersTests(unittest.TestCase):

    def setUp(self):

        self.abstract_sampler = None
        self.clist_sampler = None
        self.hexagonal_sampler = None
        self.lambert_sampler = None
        self.rectilinear_sampler = None

    def tearDown(self):

        del self.abstract_sampler
        del self.clist_sampler
        del self.hexagonal_sampler
        del self.lambert_sampler
        del self.rectilinear_sampler
    
    def test_import(self):

        module_name_1 = 'handybeam_core.samplers'
        module_name_2 = 'handybeam_core.samplers.abstract_sampler'
        module_name_3 = 'handybeam_core.samplers.clist_sampler'
        module_name_4 = 'handybeam_core.samplers.hexagonal_sampler'
        module_name_5 = 'handybeam_core.samplers.lambert_sampler'
        module_name_6 = 'handybeam_core.samplers.rectilinear_sampler'


        import handybeam_core.samplers
        import handybeam_core.samplers.abstract_sampler
        import handybeam_core.samplers.clist_sampler
        import handybeam_core.samplers.hexagonal_sampler
        import handybeam_core.samplers.lambert_sampler
        import handybeam_core.samplers.rectilinear_sampler


        fail = False

        if  module_name_1 not in sys.modules or \
            module_name_2 not in sys.modules or \
            module_name_3 not in sys.modules or \
            module_name_4 not in sys.modules or \
            module_name_5 not in sys.modules or \
            module_name_6 not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam_core.world
        import handybeam_core.samplers.abstract_sampler
        import handybeam_core.samplers.clist_sampler
        import handybeam_core.samplers.hexagonal_sampler
        import handybeam_core.samplers.lambert_sampler
        import handybeam_core.samplers.rectilinear_sampler

        world = handybeam_core.world.World()
        self.abstract_sampler = handybeam_core.samplers.abstract_sampler.AbstractSampler(parent = world)
        self.clist_sampler = handybeam_core.samplers.clist_sampler.ClistSampler(parent = world)
        self.hexagonal_sampler = handybeam_core.samplers.hexagonal_sampler.HexagonalSampler(parent = world)
        self.lambert_sampler = handybeam_core.samplers.lambert_sampler.LambertSampler(parent = world)
        self.rectilinear_sampler = handybeam_core.samplers.rectilinear_sampler.RectilinearSampler(parent = world)

        fail = True

        if isinstance(self.abstract_sampler,handybeam_core.samplers.abstract_sampler.AbstractSampler)     and \
           isinstance(self.clist_sampler, handybeam_core.samplers.clist_sampler.ClistSampler)             and \
           isinstance(self.hexagonal_sampler, handybeam_core.samplers.hexagonal_sampler.HexagonalSampler) and \
           isinstance(self.lambert_sampler, handybeam_core.samplers.lambert_sampler.LambertSampler)       and \
           isinstance(self.rectilinear_sampler, handybeam_core.samplers.rectilinear_sampler.RectilinearSampler):
            
            fail = False

        self.assertEqual(fail,False)




## Script 

if __name__ == '__main__':

    unittest.main()
