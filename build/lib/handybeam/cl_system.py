## Imports

import configparser
import os
import pyopencl as cl
import numpy as np
import handybeam

## Global variables

cl_config_file_name = 'cl_platform_config.ini'
""" string: constant, file name to store the configuration of the OpenCL subsystem.
"""


def print_all_info_of_device(use_platform=0, use_device=0):
    """ print lots of information about the selected device in given platform

    uses :code:`dir(device)` to get a list properties, and then, queries them

    :param use_platform:
    :param use_device:
    :return:
    """
    device0 = cl.get_platforms()[use_platform].get_devices()[use_device]
    for idx, thing in enumerate(dir(device0)):
        print('idx:{}, thing:{}'.format(idx, thing))
        try:
            print(eval("device0.{}".format(thing)))
        except Exception as einstance:
            print('Throws error')
            print(einstance)
        print('-----')


class OpenCLSystem():
    """ DESCRIPTION HERE

    .. ToDo::

        docs...


    """

    def __init__(self,
                 parent=None,
                 use_config_file=True,
                 use_this_config_file_full_path=None,
                 use_platform=0,
                 use_device=2,
                 print_feedback=False):
        """ DESCRIPTION HERE

        Parameters
        ----------

        parent :  DESCRIPTION HERE
        use_config_file : DESCRIPTION HERE
        use_this_config_file_full_path : DESCRIPTION HERE
        use_platform : DESCRIPTION HERE
        use_device : DESCRIPTION HERE
        print_feedback : DESCRIPTION HERE

        """

        self.parent = parent

        self.__kernel_sources = {
                                    'cl/_hbk_clist_propagator.cl',
                                    'cl/_hbk_rect_propagator.cl',
                                    'cl/_hbk_hex_propagator.cl',
                                    'cl/_hbk_lamb_propagator.cl',
                                    'cl/_hbk_sf_solver.cl',
                                    'cl/_hbk_xy_translator.cl',
                                    'cl/_hbk_xyz_translator.cl',
                                }
                                
        self.use_config_file = use_config_file
        self.use_this_config_file_full_path = use_this_config_file_full_path
        self.use_platform = use_platform
        self.use_device = use_device
        self.print_feedback = print_feedback
        self.compiled_kernels = None
        self.platforms = None
        self.device = None
        self.devices = None
        self.context = None
        self.queue = None

        self.checks_and_feedback()
 
    def checks_and_feedback(self):
        """DESCRIPTION HERE

        """

        if self.print_feedback:
            print('cl_system.__init__: parent is {}'.format(self.parent))

        this_folder = os.path.dirname(os.path.abspath(__file__))

        if self.print_feedback:
            print('cl_system.__init__: this_folder is {}'.format(this_folder))

        use_platform = self.use_platform
        use_device = self.use_device

        if self.print_feedback:
            print('cl_system.__init__: got use_platform={}, use_device={}'.format(use_platform, use_device))

        os.environ["PYOPENCL_COMPILER_OUTPUT"] = "1"

        self.platforms = cl.get_platforms()
        self.platform = self.platforms[use_platform]
        self.devices = self.platform.get_devices()
        self.device = self.devices[use_device]
        self.context = cl.Context(devices=[self.device])
        self.queue = cl.CommandQueue(self.context, device=self.device,
                                     properties=cl.command_queue_properties.PROFILING_ENABLE)

        if self.print_feedback:
            print('. Compiling kernels...', end='')
       
        entire_source_text = ''

        constants_path = os.path.join(this_folder,'cl/constants.cl')

        if self.parent is not None:
            with open(constants_path,'w') as f:

                f.write('\n#define tau ' + str(2*np.pi) + 'f\n')
                f.write('#define root_2 ' + str(1.4142135623730951) + 'f\n')
                f.write('#define pi_over_2 ' + str(1.5707963267948966) + 'f\n')
                f.write('#define medium_wavelength ' + str(self.parent.medium_wavelength) + 'f\n')
                f.write('#define medium_wavenumber ' + str(self.parent.medium_wavenumber) + 'f\n')
                f.write('#define translation_medium_wavenumber ' + str(self.parent.medium_wavenumber * 2*np.pi) + 'f\n')
                f.write('#define emission_frequency ' + str(self.parent.frequency) + '\n')

        with open(constants_path,'r') as f:
            kernel_text = f.read()

        entire_source_text += kernel_text

        for source_file in self.__kernel_sources:
            kernel_source_file_name = os.path.join(this_folder, source_file)
            with open(kernel_source_file_name,'r') as f:
                kernel_text = f.read()

            entire_source_text += kernel_text

        combined_kernels_filename = os.path.join(this_folder, 'combined_kernels.tmp.cl')

        with open(combined_kernels_filename,'w') as f:
            
            combined_kernels_file_length = f.write(entire_source_text)
        
        if self.print_feedback:
            print(' {:0.0f}kB sources... '.format(combined_kernels_file_length / 1024), end='')
        
        # self.print_current_device(endtype='')
        self.compiled_kernels = cl.Program(self.context, entire_source_text).build()

        if self.print_feedback:
            print(', done.')


    def print_cl_platforms(self):
        """DESCRIPTION HERE

        """
     
        platforms = cl.get_platforms()

        for platform_idx, platform in enumerate(platforms):
            print('------------')
            print('platform: {}, name = {}'.format(platform_idx, platform.name))
            devices = platform.get_devices()
            for device_idx, device in enumerate(devices):
                print('--- platform {}, device {} : name= {}'.format(platform_idx, device_idx, device.name))


    def select_cl_platform(self,use_platform=0, use_device=0):
        """Save a selected platform and device index to a configuration file. This config file will then be read on next startup.

        Parameters
        ----------

        use_platform : integer
            platform ID
        use_device : integer
            device ID for given platform ID

        """

        cl_config = configparser.ConfigParser()
        cl_config.add_section('what_to_use')
        cl_config.set('what_to_use', 'use_platform', '{}'.format(use_platform))
        cl_config.set('what_to_use', 'use_device', '{}'.format(use_device))

        this_folder = os.path.dirname(os.path.abspath(__file__))
        config_file_name = os.path.join(this_folder, cl_config_file_name)
        with open(config_file_name, 'w') as out:
            cl_config.write(out)

    def print_current_device(self, endtype='\n'):
        """ prints the name of the current device

        :param endtype: leave default to add newline at the end. set to :code:`` to ommit the newline.
        :return: just prints.
        """
        print('Current compute device:{}'.format(self.device.name), end=endtype)


def print_sysinfo():
    """Prints condensed OpenCL system information.

    """
    cl.get_platforms()
    print('--system info--')
    print('current folder: ', os.getcwd())
    print('------------')
    print('platforms:')
    for idxp, platform in enumerate(cl.get_platforms()):
        print(idxp, " ->", platform.name)
        print('------------')
        print('devices:')
        # print the devices in the system, marking out the selected one.
        for idxd, qdevice in enumerate(platform.get_devices()):
            print(idxd, ' -> ', end='')
            print('           ', end='')
            print(qdevice.name)
        print('------------')
        print('')
        print("Machine capabilities:")
        for idx, device in enumerate(platform.get_devices()):
            print('')
            print("-------------------- device {}: ----------------".format(idx))
            print("|   Name: ", device.name)
            print("| Memory: ", device.global_mem_size / 1024 / 1024 / 1024, "GB")
            print("|threads: ", device.max_compute_units)
            print("|  clock: ", device.max_clock_frequency, "MHz")
            print("|version: ", device.version, " ")
            print("--------------------------------------------------- ")

    print('------------')
    print('compiled kernels:')
    all_kernels = self.compiled_kernels.all_kernels()
    # pylint: disable=C0200
    for idx in range(len(all_kernels)):
        print(idx, '->',
              all_kernels[idx].function_name,
              '(', all_kernels[idx].num_args, 'arguments )')



