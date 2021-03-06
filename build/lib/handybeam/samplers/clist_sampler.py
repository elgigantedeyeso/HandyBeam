## Imports

import numpy as np
from handybeam.samplers.abstract_sampler import AbstractSampler

# Class

class ClistSampler(AbstractSampler):

    '''
    ---------------------------------------------
    ClistSampler
    ---------------------------------------------
    
    This is the general sampling grid class. It takes a list of sampling points
    and samples the acoustic field at these points.

    '''

    def __init__(self,parent=None, local_work_size = (128,1,1)):

        '''
        ---------------------------------------------
        __init__(parent)
        ---------------------------------------------
        
        This method intialises an instance of the ClistSampler class.

        Parameters
        ----------

        parent : handybeam_core.world.World
                This is an instance of the handybeam world class. 
        local_work_size : tuple
                This sets the local work size for the GPU, not recommended to change unless the user
                has experience with OpenCL and pyopencl.

        '''
        
        super(ClistSampler,self).__init__()

        self.world = parent  
        self.pressure_field = None
        self.coordinates = np.zeros((0,3),dtype = np.float32)
        self.no_points = None
        self.local_work_size = local_work_size

    def find_clist_grid_volume(self):
        
        '''
        ---------------------------------------------
        find_clist_grid_volume()
        ---------------------------------------------
        
        This method finds the volume of the requested sampling grid.

        '''

        # Find the distance along the x-axis.

        x_min = np.min(self.coordinates[:,0])
        x_max = np.max(self.coordinates[:,0])
        x_length = x_max - x_min

        # Find the distance along the y-axis.

        y_min = np.min(self.coordinates[:,1])
        y_max = np.max(self.coordinates[:,1])
        y_length = y_max - y_min

        # Find the distance along the z-axis.

        z_min = np.min(self.coordinates[:,2])
        z_max = np.max(self.coordinates[:,2])
        z_length = z_max - z_min

        # Find the volume.

        self.volume = x_length * y_length * z_length

    def add_sampling_points(self, x_list, y_list, z_list):

        '''
        ---------------------------------------------
        add_sampling_points(x_list,y_list,z_list)
        ---------------------------------------------
        
        This method adds the requested sampling points to the sampler object. 

        Parameters
        ----------

        x_list : numpy array
                This is an array containing the x-coordinates of the requested
                sampling points.
        y_list : numpy array
                This is an array containing the y-coordinates of the requested
                sampling points.
        z_list : numpy array
                This is an array containing the z-coordinates of the requested
                sampling points.

        '''

        self.coordinates = np.column_stack([x_list,y_list, z_list])
        self.coordinates = self.coordinates.astype(np.float32)

    def clear_data(self):

        '''
        ---------------------------------------------
        clear_data ()
        ---------------------------------------------
        
        This method clears the data assigned to the object.

        '''

        self.coordinates = np.zeros((0,3),dtype = np.float32)
        self.pressure_field = None

    def propagate(self, print_performance_feedback=False):

        '''
        ---------------------------------------------
        propagate(print_performance_feedback)
        ---------------------------------------------
        
        This method calls the clist_propagator to propagate the acoustic field to 
        the desired sampling points.

        Parameters
        ----------

        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        '''

        kernel_output = self.parent.propagator.clist_propagator(
                                                        tx_array=self.parent.tx_array,
                                                        sampling_point_list=self.coordinates,
                                                        local_work_size= self.local_work_size,
                                                        print_performance_feedback=print_performance_feedback
                                                    )
        self.pressure_field = np.nan_to_num(kernel_output[:,0] + np.complex(0,1) * kernel_output[:,1])
        
        self.no_points = len(self.coordinates[:,0])
