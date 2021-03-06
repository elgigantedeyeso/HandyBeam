## Imports

import cmocean
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import matplotlib.pylab as pl
import numpy as np
import vispy
from vispy import io, plot as vp
from vispy import app, scene, io

amplitude_colormap = cmocean.cm.haline
phase_colormap = cmocean.cm.phase

## Functions

def axisEqual3D(ax):
    '''

    makes the proportions of the distances equal - taken from

    https://stackoverflow.com/questions/8130823/set-matplotlib-3d-plot-aspect-ratio

    :param ax:
    :return:
    '''
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

def tx_array_basic(tx_array=None, filename=None, figsize=(4, 3), dpi=150, show=True):
    """ visualize the transmitter array, with dots where elements are located.

    :param handybeam.tx_array.TxArray tx_array: reference to the array descriptor to visualize.
    :param filename: if set, save the figure contents to a file using :code:`plt.savefig(filename)`. If unset, do nothing.
    :param figsize: figure size for the :code:`plt.figure(figsize=xxx)` command.
    :param dpi: resolution for the :code:`plt.figure(dpi=xxx)` command.
    :param show: if True, call :code:`plt.show()`. If false, do not do that and return the handle to :code:`plt.figure()` object instead. Default: :code:`True`
    :return: handle to the plt.figure object if show==False. Nothing otherwise.
    """

    hf = plt.figure(figsize=figsize, dpi=dpi)
    plt.plot(tx_array.tx_array_element_descriptor[:, 0]*1e3, tx_array.tx_array_element_descriptor[:, 1]*1e3, 'o')
    plt.grid(True)
    plt.axis('equal')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.title(tx_array.name)

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        if show:
            plt.show()
        else:
            return hf


def visualise_flat_tx_array(world = None,filename = None, figsize=[15,10], dpi=150 ):
    ''' Create a figure with plot of the location of the array's elements.

    .. warning::

        This is Sal's method -- do not use for Jurek's scripts, as it might be incompatible.

    .. warning::

        Depreciated. Use :meth:`handybeam.visualize.tx_array_basic` instead.


    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam.world class.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.
    
    '''

    los = dict()

    los['figure'] = plt.figure(figsize=figsize, dpi=dpi)
    los['figure'].plot(world.tx_array.tx_array_element_descriptor[:,0]*1e3, world.tx_array.tx_array_element_descriptor[:,1]*1e3, 'o')
    los['figure'].grid()
    los['figure'].axis('equal')
    los['figure'].xlabel('x [mm]')
    los['figure'].ylabel('y [mm]')
    los['figure'].title(world.tx_array.__str__())
    los['figure'].show()

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualise_sampling_grid(sampler=None, filename=None, figsize=[15,10], dpi=150):

    '''
        
    This method visualises the location of the transducers.

    Parameters
    ----------
    
    world : handybeam_core.world
            An instance of the handybeam.world class.
    sampler : handybeam.sampler
            An instance of one of the handybeam sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.
    '''
    los = dict()

    x_points = sampler.coordinates[:,:,0]
    y_points = sampler.coordinates[:,:,1]
    z_points = sampler.coordinates[:,:,2]

    los['figure'] = plt.figure(figsize=figsize, dpi=dpi)
    los['axes'] = Axes3D(los['figure'])
    los['axes'].scatter(x_points,y_points,z_points)
 
    los['axes'].set_zlabel('z [m]',FontSize  = 15 )
    los['axes'].set_ylabel('y [m]',FontSize  = 15 )
    los['axes'].set_xlabel('x [m]',FontSize  = 15 )

    los['axes'].legend(prop={'size': 15})
    los['axes'].set_title('Sampling grid coordinates', FontSize = 15)

    axisEqual3D(los['axes'])

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()




def visualise_sampling_grid_and_array(
        world=None,
        sampler=None,
        filename=None,
        figsize=(4, 3),
        dpi=150):
    """visualises the location of the sampling grid points and the transducers.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam.world class.
    sampler : handybeam.sampler
            An instance of one of the handybeam sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.
    """

    los = dict()

    sg_x_points = sampler.coordinates[:, :, 0]
    sg_y_points = sampler.coordinates[:, :, 1]
    sg_z_points = sampler.coordinates[:, :, 2]

    arr_x_points = world.tx_array.tx_array_element_descriptor[:,0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:,1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:,2]

    norm_axis_x = [-sampler.normal_vector[0]*k*0.1 + sampler.origin[0] for k in range(2)]
    norm_axis_y = [-sampler.normal_vector[1]*k*0.1 + sampler.origin[1] for k in range(2)]
    norm_axis_z = [-sampler.normal_vector[2]*k*0.1 + sampler.origin[2] for k in range(2)]

    par_axis_x = [sampler.parallel_vector[0]*k*0.1 + sampler.origin[0] for k in range(2)]
    par_axis_y = [sampler.parallel_vector[1]*k*0.1 + sampler.origin[1] for k in range(2)]
    par_axis_z = [sampler.parallel_vector[2]*k*0.1 + sampler.origin[2] for k in range(2)]

    vec_x_2 = [sampler.vector_2[0]*k*0.1 + sampler.origin[0] for k in range(2)]
    vec_y_2 = [sampler.vector_2[1]*k*0.1 + sampler.origin[1] for k in range(2)]
    vec_z_2 = [sampler.vector_2[2]*k*0.1 + sampler.origin[2] for k in range(2)]

    los['figure'] = plt.figure(figsize=figsize, dpi=dpi)
    los['axes'] = Axes3D(los['figure'])

    sampling_points = los['axes'].scatter(sg_x_points,sg_y_points,sg_z_points,'b')
    array_points = los['axes'].scatter(arr_x_points,arr_y_points,arr_z_points,'r')
    line_normal = los['axes'].plot(norm_axis_x,norm_axis_y,norm_axis_z,color='k')
    line_par_1 = los['axes'].plot(par_axis_x,par_axis_y,par_axis_z,color='r')
    line_uv_2 = los['axes'].plot(vec_x_2,vec_y_2,vec_z_2,color='b')

    sampling_points.set_label('Sampling points')
    array_points.set_label('Tranducers')
 
    los['axes'].set_zlabel('z [m]',FontSize  = 20 )
    los['axes'].set_ylabel('y [m]',FontSize  = 20 )
    los['axes'].set_xlabel('x [m]',FontSize  = 20 )
    los['axes'].legend(prop={'size': 15},loc ='center left')

    los['axes'].set_title('Sampling grid and array coordinates', FontSize = 20)

    axisEqual3D(los['axes'])

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

# ====================================================================================================
# ====================================================================================================
# ====================================================================================================
# ====================================================================================================
# ====================================================================================================

def visualize_3D_only_alpha(world=None,
                            samplers=(),
                            filename=None,
                            figsize=(4, 3),
                            dpi=150,
                            transparent_threshold=0.1,
                            opaque_threshold=0.2,
                            max_display_points_per_axis=80):
    """ visualizes location of the probe, phase on the probe, and any compatible samplers, in a single figure

    .. Note: the opaque_threshold must be larger than transparent_threshold, or the result is undefined

    Examples:

    .. image:: _static/example_visualize_3D_only_alpha_01.png

    .. image:: _static/example_visualize_3D_only_alpha_02.png

    Parameters
    ----------

    world: handybeam.world.World
        An instance of the handybeam.world class.
    samplers: world.samplers.abstract_sampler
        list of samplers to include. Note that this has to be a list.
        If set to None, samplers are loaded from the world.
    filename: string
        if set, image is saved to the file named. Do not forget to add the extension, e.g. :code:`.png`
    figsize: tuple
        size of the figure in inches
    dpi: integer
        resolution of the figure, in points per inch
    transparent_threshold: float
        value of 0-1, or beyond - (after-normalization) pressure values below this threshould will be transparent.
        Use values less then zero to make zero-pressure somewhat opaque
    opaque_threshold: float
        value of 0-1, or beyond - (after-normalization) pressure values above this threshould will be opaque.
        Values in between transparent* and opaque* are interpolated for varied alpha.
        Use values of more than unity to make the peak-pressure somewhat transparent

    """

    hf = plt.figure(figsize=figsize, dpi=dpi)
    ha = Axes3D(hf)

    # plot the array first so that it is covered later
    arr_x_points = world.tx_array.tx_array_element_descriptor[:, 0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:, 1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:, 2]
    # keep track of xmax and xmin
    xmax = np.max(arr_x_points)
    xmin = np.min(arr_x_points)
    ymax = np.max(arr_y_points)
    ymin = np.min(arr_y_points)
    zmax = np.max(arr_z_points)
    zmin = np.min(arr_z_points)

    array_points = ha.scatter(
        arr_x_points,
        arr_y_points,
        arr_z_points,
        c=world.tx_array.tx_array_element_descriptor[:, 11],
        cmap=phase_colormap, marker=",")

    if samplers is None:
        print('samplers is not none.')
        samplers = world.samplers

    for idx, sampler in enumerate(samplers):

        if len(sampler.coordinates.shape) == 3:  # surface sampler, 2D list of points
            sg_x_points = sampler.coordinates[:, :, 0]
            sg_y_points = sampler.coordinates[:, :, 1]
            sg_z_points = sampler.coordinates[:, :, 2]
        else:  # a clist sampler, 1D list of points
            # numpy.expand_dims
            sg_x_points = sampler.coordinates[:, 0]
            sg_y_points = sampler.coordinates[:, 1]
            sg_z_points = sampler.coordinates[:, 2]

        xmax = np.max((xmax, np.max(sg_x_points)))
        xmin = np.min((xmin, np.min(sg_x_points)))
        ymax = np.max((ymax, np.max(sg_y_points)))
        ymin = np.min((ymin, np.min(sg_y_points)))
        zmax = np.max((zmax, np.max(sg_z_points)))
        zmin = np.min((zmin, np.min(sg_z_points)))

        pressure_field = np.nan_to_num(np.abs(sampler.pressure_field))
        pressure_field_peak = np.max(pressure_field)

        # If there are a lot of points in the sampling grid then just display a subset of them.
        if len(sg_x_points) > max_display_points_per_axis:
            stepper = int(np.ceil(len(sg_x_points) / max_display_points_per_axis))

            sg_x_points = sg_x_points[0::stepper]
            sg_y_points = sg_y_points[0::stepper]
            sg_z_points = sg_z_points[0::stepper]
            pressure_field = pressure_field[0::stepper]

        # prepare transparency map
        # r=ravelled (1d-ized)
        pressure_field_r = np.nan_to_num(np.abs(
            pressure_field)).ravel()  # note that this is the already-reduced-resolution version of pressure_field
        pressure_field_peak = np.max(pressure_field_r)
        pressure_field_normalized_r = pressure_field_r * (1.0 / pressure_field_peak)
        pressure_field_alpha_r = np.minimum(1.0, np.maximum(0, (pressure_field_normalized_r - transparent_threshold) / (
                    opaque_threshold - transparent_threshold)))
        # print(f'pressure_field_normalized_r.shape = {pressure_field_normalized_r.shape}')
        pressure_field_colors_r = amplitude_colormap(pressure_field_normalized_r)
        # print(f'pressure_field_colors_r.shape = {pressure_field_colors_r.shape}')
        pressure_field_colors_r[:, 3] = pressure_field_alpha_r

        sampling_points_amp = ha.scatter(
            sg_x_points,
            sg_y_points,
            sg_z_points,
            c=pressure_field_colors_r,
            marker="o")

    ha.set_xlabel('x-dimension[m]\npassive aperture')
    ha.set_ylabel('y-dimension[m]\nactive aperture')
    ha.set_zlabel('z-dimension[m]\ntarget depth')

    # plt.axes('equal')
    # create equal axes
    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([xmax - xmin, ymax - ymin, zmax - zmin]).max()
    Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (xmax + xmin)
    Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (ymax + ymin)
    Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (zmax + zmin)
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ha.plot([xb], [yb], [zb], 'w')

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualize_3D_only(world=None,
                      samplers=(),
                      alpha=0.01,
                      filename=None,
                      figsize=(4, 3),
                      dpi=150):
    """ visualizes location of the probe, phase on the probe, and any compatible samplers, in a single figure

    Parameters
    ----------

    world: handybeam.world.World
        An instance of the handybeam.world class.
    samplers: world.samplers.abstract_sampler
        list of samplers to include. Note that this has to be a list.
        If set to None, samplers are loaded from the world.
    filename: string
        if set, image is saved to the file named. Do not forget to add the extension, e.g. :code:`.png`
    figsize: tuple
        size of the figure in inches
    dpi: integer
        resolution of the figure, in points per inch

    """

    hf = plt.figure(figsize=figsize, dpi=dpi)
    ha = Axes3D(hf)

    # plot the array first so that it is covered later
    arr_x_points = world.tx_array.tx_array_element_descriptor[:, 0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:, 1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:, 2]
    # keep track of xmax and xmin
    xmax = np.max(arr_x_points)
    xmin = np.min(arr_x_points)
    ymax = np.max(arr_y_points)
    ymin = np.min(arr_y_points)
    zmax = np.max(arr_z_points)
    zmin = np.min(arr_z_points)

    array_points = ha.scatter(
        arr_x_points,
        arr_y_points,
        arr_z_points,
        c=world.tx_array.tx_array_element_descriptor[:, 11],
        cmap=phase_colormap, marker=",")

    if samplers is None:
        print('samplers is not none.')
        samplers = world.samplers

    for idx, sampler in enumerate(samplers):

        if len(sampler.coordinates.shape) == 3:  # surface sampler, 2D list of points
            sg_x_points = sampler.coordinates[:, :, 0]
            sg_y_points = sampler.coordinates[:, :, 1]
            sg_z_points = sampler.coordinates[:, :, 2]
        else:  # a clist sampler, 1D list of points
            # numpy.expand_dims
            sg_x_points = sampler.coordinates[:, 0]
            sg_y_points = sampler.coordinates[:, 1]
            sg_z_points = sampler.coordinates[:, 2]


        xmax = np.max((xmax, np.max(sg_x_points)))
        xmin = np.min((xmin, np.min(sg_x_points)))
        ymax = np.max((ymax, np.max(sg_y_points)))
        ymin = np.min((ymin, np.min(sg_y_points)))
        zmax = np.max((zmax, np.max(sg_z_points)))
        zmin = np.min((zmin, np.min(sg_z_points)))
        pressure_field = np.nan_to_num(sampler.pressure_field)
        # If there are a lot of points in the sampling grid then just display a subset of them.

        if len(sg_x_points) > 50:
            stepper = int(np.ceil(len(sg_x_points) / 50))

            sg_x_points = sg_x_points[0::stepper]
            sg_y_points = sg_y_points[0::stepper]
            sg_z_points = sg_z_points[0::stepper]
            pressure_field = pressure_field[0::stepper]


        sampling_points_amp = ha.scatter(
            sg_x_points,
            sg_y_points,
            sg_z_points,
            c=np.abs(pressure_field).ravel(),
            cmap=amplitude_colormap, marker="o", alpha=alpha)


    ha.set_xlabel('x-dimension[m]\npassive aperture')
    ha.set_ylabel('y-dimension[m]\nactive aperture')
    ha.set_zlabel('z-dimension[m]\ntarget depth')

    # plt.axes('equal')
    # create equal axes
    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([xmax - xmin, ymax - ymin, zmax - zmin]).max()
    Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (xmax + xmin)
    Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (ymax + ymin)
    Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (zmax + zmin)
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ha.plot([xb], [yb], [zb], 'w')

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()




def plot_1D_pressure_vs_angle(world=None,
                              angles=None,
                              pressure=None,
                              figsize=(4, 3),
                              dpi=150,
                              filename=None):
    hf = plt.figure(figsize=figsize, dpi=dpi)
    plt.plot(angles, pressure)

    plt.grid(True)
    plt.xlabel('angle from normal[rad]')
    plt.ylabel('pressure,linear[-]')
    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def plot_1D_pressure_vs_angle_db_normalized( world=None,
                                  angles=None,
                                  pressure=None,
                                  figsize=(4, 3),
                                  dpi=150,
                                  filename=None):
    hf = plt.figure(figsize=figsize, dpi=dpi)
    p_db = 20 * np.log10(np.abs(pressure))
    p_db = p_db - np.max(p_db)
    plt.plot(angles, p_db)
    plt.ylim(-40, 1)
    plt.grid(True)
    plt.xlabel('angle from normal[rad]')
    plt.ylabel('pressure, dB re max(p) [-]')
    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualise_all_in_one(world=None,sampler=None,filename=None,figsize=(16,9),dpi=80):
    
    '''visualises the amplitude and phase of the pressure field and the transducers.

    Parameters
    ----------

    world : handybeam.world.World
            An instance of the handybeam.world class.
    sampler : handybeam.sampler
            An instance of one of the handybeam sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.

    '''

    los = dict()

    sg_x_points = sampler.coordinates[:,:,0] 
    sg_y_points = sampler.coordinates[:,:,1] 
    sg_z_points = sampler.coordinates[:,:,2] 

    arr_x_points = world.tx_array.tx_array_element_descriptor[:,0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:,1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:,2]

    pressure_field = np.nan_to_num(sampler.pressure_field)
    
    # If there are a lot of points in the sampling grid then just display a subset of them.
    
    if len(sg_x_points) > 50:
        
        stepper = int(np.ceil(len(sg_x_points)/50))

        sg_x_points = sg_x_points[0::stepper]
        sg_y_points = sg_y_points[0::stepper]
        sg_z_points = sg_z_points[0::stepper]

        pressure_field = pressure_field[0::stepper]

    gs = gridspec.GridSpec(2, 2)    

    fig = pl.figure(figsize=figsize, dpi=dpi)

    los['amplitude'] = pl.subplot(gs[0, 0], projection='3d')
    los['phase'] = pl.subplot(gs[0, 1], projection='3d')
    los['trans_amp'] = pl.subplot(gs[1, 0])
    plt.axis('equal')
    los['trans_phase'] = pl.subplot(gs[1, 1])
    plt.axis('equal')
    
    sampling_points_amp = los['amplitude']\
        .scatter(
            sg_x_points,
            sg_y_points,
            sg_z_points,
            c=np.abs(pressure_field).ravel(),
            cmap=amplitude_colormap)

    array_points = los['amplitude']\
        .scatter(
            arr_x_points,
            arr_y_points,
            arr_z_points,
            c=world.tx_array.tx_array_element_descriptor[:, 11],
            cmap=phase_colormap,
            marker = ",")

    array_points.set_label('Transducer coordinates')
 
    los['amplitude'].set_zlabel('z [m]', FontSize=15)
    los['amplitude'].set_ylabel('y [m]', FontSize=15)
    los['amplitude'].set_xlabel('x [m]', FontSize=15)

    los['amplitude'].set_proj_type('persp')

    amp_cbar = plt.colorbar(
        sampling_points_amp,
        ax=los['amplitude'],
        cmap=amplitude_colormap)

    amp_cbar.ax.set_ylabel('SPL (Pa)', rotation=0, y=0, FontSize=15)

    los['amplitude'].set_title('Amplitude of the pressure field.', FontSize=15, y=1.08)
    los['amplitude'].legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2, prop={'size': 15})
    
    sampling_points_phase = los['phase']\
        .scatter(
            sg_x_points,
            sg_y_points,
            sg_z_points,
            c=np.angle(pressure_field).ravel(),
            cmap=phase_colormap)

    array_points = los['phase']\
        .scatter(
            arr_x_points,
            arr_y_points,
            arr_z_points,
            c=world.tx_array.tx_array_element_descriptor[:, 11],
            cmap=phase_colormap)

    array_points.set_label('Transducer coordinates')
 
    los['phase'].set_zlabel('z [m]', FontSize=15)
    los['phase'].set_ylabel('y [m]', FontSize=15)
    los['phase'].set_xlabel('x [m]', FontSize=15)

    los['phase'].set_proj_type('persp')

    phase_cbar = plt.colorbar(sampling_points_phase,ax = los['phase'],cmap = phase_colormap)
    phase_cbar.ax.set_ylabel('Radians',rotation = 0, y = 0,FontSize = 15)

    los['phase'].set_title('Phase of the pressure field.', FontSize = 15,y=1.08)
    los['phase'].legend(loc=9, bbox_to_anchor=(0.5, -0.01),ncol = 2,prop={'size': 15})

    axisEqual3D(los['amplitude'])
    axisEqual3D(los['phase'])

    x0 = np.min(arr_x_points)
    xmax = np.max(arr_x_points)

    y0 = np.min(arr_y_points)
    ymax = np.max(arr_y_points)

    transducer_amplitude_distribution = world.tx_array.tx_array_element_descriptor[:,10]
    transducer_phase_distribution =world.tx_array.tx_array_element_descriptor[:,11]

    trans_phase = los['trans_phase'].scatter(arr_x_points,arr_y_points,
                                c = world.tx_array.tx_array_element_descriptor[:,11],
                                cmap = phase_colormap,
                                s = 100)

    los['trans_phase'].set_ylabel('y [m]',FontSize  = 15 )
    los['trans_phase'].set_xlabel('x [m]',FontSize  = 15 )
    los['trans_phase'].set_title('Phase distribution at the transducer plane.', FontSize = 15)

    phase_cbar = plt.colorbar(trans_phase, ax = los['trans_phase'], cmap = phase_colormap)
    phase_cbar.ax.set_ylabel('Radians', rotation = 0, y = 0, FontSize = 15)

    trans_amp = los['trans_amp'].scatter(arr_x_points,arr_y_points,
                                c = world.tx_array.tx_array_element_descriptor[:,10],
                                cmap = amplitude_colormap,
                                s = 100)

    los['trans_amp'].set_ylabel('y [m]',FontSize  = 15 )
    los['trans_amp'].set_xlabel('x [m]',FontSize  = 15 )
    los['trans_amp'].set_title('Amplitude distribution at the transducer plane.', FontSize = 15)

    amp_cbar = plt.colorbar(trans_amp,ax = los['trans_amp'],cmap = amplitude_colormap)
    amp_cbar.ax.set_ylabel('SPL (Pa)',rotation = 0, y = 0,FontSize = 15)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace= 0.3, hspace=0.3)

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualise_translation(  world=None, original_pressure_field=None,
                            sampler=None,filename=None, figsize=(15, 10), dpi=150):

    '''
        
    This method visualises the effect of the (x-y) translation algorithm on the
    amplitude and phase of the acoustic field.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam.world class.
    original_pressure_field : numpy array
            A numpy array containing the propagated acoustic pressure field.
    sampler : handybeam.sampler
            An instance of one of the handybeam sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.

    '''

    los = dict()

    sg_x_points = sampler.coordinates[:, :, 0]
    sg_y_points = sampler.coordinates[:, :, 1]
    sg_z_points = sampler.coordinates[:, :, 2]

    arr_x_points = world.tx_array.tx_array_element_descriptor[:, 0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:, 1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:, 2]

    pressure_field_after = np.nan_to_num(sampler.pressure_field)
    
    # If there are a lot of points in the sampling grid then just display a subset of them.
    
    if len(sg_x_points) > 50:
        
        stepper = int(np.ceil(len(sg_x_points)/50))

        sg_x_points = sg_x_points[0::stepper]
        sg_y_points = sg_y_points[0::stepper]
        sg_z_points = sg_z_points[0::stepper]

        pressure_field_after = pressure_field_after[0::stepper]
        pressure_field_before = original_pressure_field[0::stepper]
   
    else:

        pressure_field_after = pressure_field_after
        pressure_field_before = original_pressure_field

  
    gs = gridspec.GridSpec(2, 2)    

    fig = pl.figure(figsize=figsize, dpi=dpi)

    los['amplitude_1'] = pl.subplot(gs[0, 0], projection='3d')
    los['phase_1'] = pl.subplot(gs[0, 1], projection='3d')

    # Plot original field amplitude.

    sampling_points_amp = los['amplitude_1'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.abs(pressure_field_before).ravel(),
                                cmap=amplitude_colormap)
    array_points = los['amplitude_1'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['amplitude_1'].set_zlabel('z [m]', FontSize=15)
    los['amplitude_1'].set_ylabel('y [m]', FontSize=15)
    los['amplitude_1'].set_xlabel('x [m]', FontSize=15)

    los['amplitude_1'].set_proj_type('persp')

    amp_cbar = plt.colorbar(sampling_points_amp, ax=los['amplitude_1'], cmap=amplitude_colormap)
    amp_cbar.ax.set_ylabel('SPL (Pa)', rotation=0, y=0, FontSize=15)

    los['amplitude_1'].set_title('Amplitude of the pressure field before translation.', FontSize=15, y=1.08)
    los['amplitude_1'].legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2, prop={'size': 15})
    
    # Plot original field phase.

    sampling_points_phase = los['phase_1'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.angle(pressure_field_before).ravel(),
                                cmap=phase_colormap)
    array_points = los['phase_1'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['phase_1'].set_zlabel('z [m]', FontSize=15)
    los['phase_1'].set_ylabel('y [m]', FontSize=15)
    los['phase_1'].set_xlabel('x [m]', FontSize=15)

    los['phase_1'].set_proj_type('persp')

    phase_cbar = plt.colorbar(sampling_points_phase, ax=los['phase_1'], cmap=phase_colormap)
    phase_cbar.ax.set_ylabel('Radians', rotation=0, y=0, FontSize=15)

    los['phase_1'].set_title('Phase of the pressure field before translation.', FontSize=15, y=1.08)
    los['phase_1'].legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2, prop={'size': 15})


    los['amplitude_2'] = pl.subplot(gs[1,0], projection = '3d')
    los['phase_2'] = pl.subplot(gs[1,1], projection='3d')

    # Plot translated field amplitude.

    sampling_points_amp = los['amplitude_2'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.abs(pressure_field_after).ravel(),
                                cmap=amplitude_colormap)
    array_points = los['amplitude_2'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['amplitude_2'].set_zlabel('z [m]', FontSize=15)
    los['amplitude_2'].set_ylabel('y [m]', FontSize=15)
    los['amplitude_2'].set_xlabel('x [m]', FontSize=15)

    los['amplitude_2'].set_proj_type('persp')

    amp_cbar = plt.colorbar(sampling_points_amp, ax=los['amplitude_2'], cmap=amplitude_colormap)
    amp_cbar.ax.set_ylabel('SPL (Pa)', rotation=0, y=0, FontSize=15)

    los['amplitude_2'].set_title('Amplitude of the pressure field after translation.', FontSize=15, y=1.08)
    los['amplitude_2'].legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2, prop={'size': 15})
    
    # Plot translated field phase.

    sampling_points_phase = los['phase_2'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.angle(pressure_field_after).ravel(),
                                cmap=phase_colormap)
    array_points = los['phase_2'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['phase_2'].set_zlabel('z [m]', FontSize=15 )
    los['phase_2'].set_ylabel('y [m]', FontSize=15 )
    los['phase_2'].set_xlabel('x [m]', FontSize=15 )

    los['phase_2'].set_proj_type('persp')

    phase_cbar = plt.colorbar(sampling_points_phase, ax=los['phase_2'], cmap=phase_colormap)
    phase_cbar.ax.set_ylabel('Radians', rotation=0, y=0, FontSize=15)

    los['phase_2'].set_title('Phase of the pressure field after translation.', FontSize = 15,y=1.08)
    los['phase_2'].legend(loc=9, bbox_to_anchor=(0.5, -0.01),ncol = 2,prop={'size': 15})

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualise_translation_3D(world = None,original_pressure_field = None,sampler = None,
        threshold = 50, colour_map = 'cubehelix'):

    '''
        
    This method visualises the effect of the (x-y) translation algorithm on the
    amplitude and phase of the acoustic field.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam.world class.
    original_pressure_field : numpy array
            A numpy array containing the propagated acoustic pressure field.
    sampler : handybeam.sampler
            An instance of one of the handybeam sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    threshold : float / int
            This sets the threshold for which sampling points are visualised in the image. It can
            be modified to ignore regions with pressure less than the threshold.
    colour_map : string
            This sets the colour map to be used in the visualisation. Please see
            https://github.com/vispy/vispy/blob/master/vispy/color/colormap.py#L348-L441.

    '''

    reshape_no = int(np.round(np.power(sampler.no_points, 1 / 3), 3))
    sampler_pressure_field_reshaped = sampler.pressure_field.reshape((reshape_no,
                                                       reshape_no,
                                                       reshape_no))
    original_pressure_field_reshaped = original_pressure_field.reshape((reshape_no,
                                                       reshape_no,
                                                       reshape_no))



    fig = vp.Fig(bgcolor='white', size=(2000, 2000), show=False)

    vol_data_before = np.abs(original_pressure_field_reshaped)
    vol_data_before = np.flipud(np.rollaxis(vol_data_before, 1))

    vol_data_before[vol_data_before < threshold] = 0
    vol_pw_before = fig[0, 0]
    vol_pw_before.volume(vol_data_before,cmap = colour_map)

    vol_data_after = np.abs(sampler_pressure_field_reshaped)
    vol_data_after = np.flipud(np.rollaxis(vol_data_after, 1))

    vol_data_after[vol_data_after < threshold] = 0
    vol_pw_after = fig[0, 1]
    vol_pw_after.volume(vol_data_after,cmap = colour_map)

    vol_pw_before.camera = scene.cameras.TurntableCamera(fov = 45)
    vol_pw_after.camera = scene.cameras.TurntableCamera(fov = 45)

    vol_pw_before.camera.link(vol_pw_after.camera)
    
    fig.show(run=True)
 
def visualise_3D(world = None, sampler = None,threshold = 50,colour_map = 'cubehelix'):
    """  show a 3D volume visualisation using VisPy

    :param world : handybeam.world.World
         the world from which to take the data

    :param sampler: handybeam.samplers.abstract_sampler
         the sampler from which to take the data

    :param threshold:
         threshold of visibility for volume visualisation

    :param colour_map:
         colour map for volume visualisation

    :return:
        creates the figure, and shows it.

    """

    fig = vp.Fig(bgcolor='white', size=(2000, 2000), show=False)

    reshape_no = int(np.round(np.power(sampler.no_points, 1 / 3), 3))
    sampler_pressure_field_reshaped = sampler.pressure_field.reshape((reshape_no,
                                                                        reshape_no,
                                                                        reshape_no))


    vol_data_after = np.abs(sampler_pressure_field_reshaped)
    vol_data_after = np.flipud(np.rollaxis(vol_data_after, 1))
    vol_data_after[vol_data_after < threshold] = 0
    vol_pw_after = fig[0, 0]
    vol_pw_after.volume(vol_data_after,cmap = colour_map)
    vol_pw_after.camera = scene.cameras.TurntableCamera(fov = 45)
     
    fig.show(run=True)

