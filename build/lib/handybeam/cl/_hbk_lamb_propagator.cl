// This is the kernel for generating lambert sampling grid coordinates.

__kernel void _hbk_lamb_propagator(
            __global float *cl_out_buffer,                      // This is the output buffer for the sampling grid coordinates and pressure values. 
            __global float *cl_tx_element_array_descriptor,     // This is the input buffer for the tx elements.           
            float radius,                                       // This is the radius of the hemisphere.
            float N,                                            // This is the length of the square grid that gets projected to the hemisphere.
            float density,                                      // This defines the density of the sampling grid.
            float x0, float y0, float z0,                       // These are the coordinates of the origin.
            unsigned int tx_count                               // This is the number of transducers.
          )
          {

            // Get thread coordinates in the computational grid. 

            unsigned int idx_x = get_global_id(0);    

            unsigned int idx_y = get_global_id(1);

            // Define variables for Lambert projection
          
            float x_base = (-1 + density * idx_x ) * root_2;
            float y_base = (-1 + density * idx_y ) * root_2;
            
            float rho = sqrt(x_base * x_base + y_base * y_base);
            float c = 2 * asin(0.5*rho);

            float phi = asin(cos(c)) / rho;
            float l = atan2( (x_base * sin(c)), -y_base*sin(c));
            float cos_phi = cos(phi);

            // Store coordinates 

            float pixel_z_coordinate = radius * sin(phi);
            float pixel_x_coordinate = radius * cos(l) * cos_phi;
            float pixel_y_coordinate = radius * sin(l) * cos_phi;

            // Make comparison to ignore points with z < 0. 
            
            unsigned int comparator =  pixel_z_coordinate < 0;
            
            // Output these pixel coordinates.

            if (comparator) return;

            // Each thread is responsible for looping through the transducers to determine the field at a single
            // sampling point.

            // Initialise pressure values

            float pressure_re = (float)0.0;
            float pressure_im = (float)0.0;

            // Iterate through the transducers.
            unsigned int tx_idx = 0;
              
              
            for (tx_idx=0; tx_idx<tx_count; tx_idx++)
                { 

                // Unpack the tx array descriptor - load data from global memory into registers, hopefully through a cache and broadcast.
                
                unsigned int tx_pointer_base = 16 * tx_idx;

                float tx_x = cl_tx_element_array_descriptor[tx_pointer_base + 0];
                float tx_y = cl_tx_element_array_descriptor[tx_pointer_base + 1];
                float tx_z = cl_tx_element_array_descriptor[tx_pointer_base + 2];
                
                float tx_xnormal = cl_tx_element_array_descriptor[tx_pointer_base + 3];
                float tx_ynormal = cl_tx_element_array_descriptor[tx_pointer_base + 4];
                float tx_znormal = cl_tx_element_array_descriptor[tx_pointer_base + 5];
                
                float directivity_phase_poly1_c1 = cl_tx_element_array_descriptor[tx_pointer_base + 6];
                
                float directivity_amplitude_poly2_c0 = cl_tx_element_array_descriptor[tx_pointer_base + 7];
                float directivity_amplitude_poly2_c1 = cl_tx_element_array_descriptor[tx_pointer_base + 8];
                float directivity_amplitude_poly2_c2 = cl_tx_element_array_descriptor[tx_pointer_base + 9];

                float tx_amp = cl_tx_element_array_descriptor[tx_pointer_base + 10];
                float tx_phase = cl_tx_element_array_descriptor[tx_pointer_base + 11];
                
                // Calculate the distance from this transducer to the sampling point.

                float delta_x = pixel_x_coordinate - tx_x;
                float delta_y = pixel_y_coordinate - tx_y;
                float delta_z = pixel_z_coordinate - tx_z;

                float recp_distance = rsqrt(delta_x*delta_x + delta_y*delta_y + delta_z*delta_z);

                // There can be no output inside a transducer.

                if (medium_wavenumber<recp_distance)
                 {
                  pressure_re = NAN;
                  pressure_im = NAN;
                  break; 
                 }

                // Now calculate the cosine of angle using the normal.

                float cosine_of_angle_to_normal =  ( delta_x*tx_xnormal + delta_y*tx_ynormal + delta_z * tx_znormal ) * recp_distance ;

                // The is no signal behind the transducer.

                if (cosine_of_angle_to_normal<0.0)
                 {
                  pressure_re = NAN;
                  pressure_im = NAN;
                  break; 
                 }
                
                // Calculate the phase distance shift 

                float phase_distance_shift = (float) tau  * medium_wavenumber * (1.0 / recp_distance);

                float phase_distance_shift_wrapped = fmod(phase_distance_shift, (float) tau);

                // Calculate amplitude distance drop 

                float amplitude_distance_drop = recp_distance * ( (float) 1.0 / medium_wavenumber);

                // Apply the HN50 directivity function here
               
                float ca = 1.0 - cosine_of_angle_to_normal;
                
                // Calculate this first so that the register holding directivity_phase_poly1_c1 can be released for ca2

                float directivity_phase = directivity_phase_poly1_c1 * ca;

                // Ca2 is simply ca^2

                float ca2 = ca*ca;
                float directivity_amplitude_drop =            \
                        directivity_amplitude_poly2_c0        \
                      + directivity_amplitude_poly2_c1 * ca   \
                      + directivity_amplitude_poly2_c2 * ca2;


                float rx_amplitude = tx_amp   * amplitude_distance_drop * directivity_amplitude_drop;
                float rx_phase     = tx_phase + phase_distance_shift_wrapped  + directivity_phase;
               
                // Accumulate result
            
                pressure_re = pressure_re + native_cos(rx_phase) * rx_amplitude;
                pressure_im = pressure_im + native_sin(rx_phase) * rx_amplitude;
            
            } 

                // Output these pixel coordinates so that we can double check they match up with the python code. 
              
            unsigned int output_pointer_base = 5 * idx_x + (5 * N * idx_y );
                          
            cl_out_buffer[output_pointer_base+0] = pixel_x_coordinate;
            cl_out_buffer[output_pointer_base+1] = pixel_y_coordinate;
            cl_out_buffer[output_pointer_base+2] = pixel_z_coordinate;
            cl_out_buffer[output_pointer_base+3] = pressure_re;
            cl_out_buffer[output_pointer_base+4] = pressure_im;

            }

