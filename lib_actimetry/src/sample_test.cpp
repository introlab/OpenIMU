#include "gtest/gtest.h"
#include <string>


#include <math.h>
#include "kfr/all.hpp"



#include "liquid.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_spline.h>


namespace {

    //SimpleTest1
    TEST(Sample, SimpleTest1) {
      std::string myString;
      EXPECT_EQ(0, myString.size());
    }

#if 1
    //KFRTest1
    TEST(KFR, Resample) {

        //Will use namespace kfr
        using namespace kfr;

        constexpr size_t input_sr  = 100;
        constexpr size_t output_sr = 50;

        //1Hz sine signal to be generated
        constexpr fbase frequency = 1.0;
        const univector<fbase, input_sr * 2> o1 = sine(counter(0,1.0/input_sr) * 2.0 * constants<fbase>::pi * frequency);

        println("input_signal");
        println(o1.size());
        println(o1);

        //allocation of output vector
        univector<fbase> resampled(o1.size() * output_sr / input_sr * 2);

        //Resampler
        auto r = resampler<fbase>(resample_quality::normal, output_sr, input_sr, 1.0, 0.49);

        println("output_signal");
        //Resample & get size
        const size_t destsize = r(resampled.data(), o1);
        println(destsize);
        println(resampled);

    }
#endif

#if 0
    //LIQUID
    TEST(LIQUID, Interpolate) {
        // options
        unsigned int k=4;                   // samples/symbol
        unsigned int m=3;                   // filter delay
        float As = 60.0f;                   // filter stop-band attenuation
        unsigned int num_data_symbols=100;   // number of data symbols

        // derived values
        unsigned int num_symbols = num_data_symbols + 2*m;  // compensate for filter delay
        unsigned int num_samples = k*num_symbols;



        float input_signal_sine_1hz_100[100] = {
            0, 0.0627905,  0.125333,  0.187381,   0.24869,  0.309017,  0.368125,   0.42578,
             0.481754,  0.535827,  0.587786,  0.637425,  0.684548,  0.728969,  0.770513,  0.809017,
             0.844327,  0.876306,  0.904826,  0.929776,  0.951056,  0.968583,  0.982288,  0.992116,
             0.998027,  0.999999,  0.998027,  0.992116,  0.982288,  0.968583,  0.951056,  0.929776,
             0.904826,  0.876306,  0.844327,  0.809017,  0.770513,  0.728969,  0.684548,  0.637425,
             0.587786,  0.535827,  0.481754,   0.42578,  0.368125,  0.309017,   0.24869,  0.187381,
             0.125333, 0.0627905,         0,    -0.063, -0.125333, -0.187381,  -0.24869, -0.309017,
            -0.368125,  -0.42578, -0.481754, -0.535827, -0.587786, -0.637425, -0.684548, -0.728969,
            -0.770513, -0.809017, -0.844327, -0.876306, -0.904826, -0.929776, -0.951056, -0.968583,
            -0.982288, -0.992116, -0.998027, -0.999999, -0.998027, -0.992116, -0.982288, -0.968583,
            -0.951056, -0.929776, -0.904826, -0.876306, -0.844327, -0.809017, -0.770513, -0.728969,
            -0.684548, -0.637425, -0.587786, -0.535827, -0.481754,  -0.42578, -0.368125, -0.309017,
             -0.24869, -0.187381, -0.125333,    -0.063 };


        liquid_float_complex x[num_symbols];   // input symbols
        liquid_float_complex y[num_samples];   // output samples


        memset(x,0,num_symbols * sizeof(liquid_float_complex));
        memset(y,0,num_samples * sizeof(liquid_float_complex));

        for (auto i = 0; i < num_data_symbols; i++)
        {
            x[i].real = input_signal_sine_1hz_100[i];
            x[i].imag = 0;
        }

        // create interpolator from prototype
        firinterp_crcf q = firinterp_crcf_create_kaiser(k,m,As);

        // interpolate symbols
        for (auto i=0; i<num_symbols; i++)
              firinterp_crcf_execute(q, x[i], &y[k*i]);


        // destroy interpolator object
        firinterp_crcf_destroy(q);

        // print results to screen
        printf("x(t) :\n");
        for (auto i=0; i<num_symbols; i++)
            printf("  x(%4u) = %8.4f + j*%8.4f;\n", i, x[i].real, x[i].imag);

        printf("y(t) :\n");
        for (auto i=0; i<num_samples; i++) {
            printf("  y(%4u) = %8.4f + j*%8.4f;", i, y[i].real, y[i].imag);
            if ( (i >= k*m) && ((i%k)==0))
                printf(" **\n");
            else
                printf("\n");
        }

    }



    //LIQUID
    TEST(LIQUID, Resample) {
        float input_signal_sine_1hz_100[100] = {
            0, 0.0627905,  0.125333,  0.187381,   0.24869,  0.309017,  0.368125,   0.42578,
             0.481754,  0.535827,  0.587786,  0.637425,  0.684548,  0.728969,  0.770513,  0.809017,
             0.844327,  0.876306,  0.904826,  0.929776,  0.951056,  0.968583,  0.982288,  0.992116,
             0.998027,  0.999999,  0.998027,  0.992116,  0.982288,  0.968583,  0.951056,  0.929776,
             0.904826,  0.876306,  0.844327,  0.809017,  0.770513,  0.728969,  0.684548,  0.637425,
             0.587786,  0.535827,  0.481754,   0.42578,  0.368125,  0.309017,   0.24869,  0.187381,
             0.125333, 0.0627905,         0,    -0.063, -0.125333, -0.187381,  -0.24869, -0.309017,
            -0.368125,  -0.42578, -0.481754, -0.535827, -0.587786, -0.637425, -0.684548, -0.728969,
            -0.770513, -0.809017, -0.844327, -0.876306, -0.904826, -0.929776, -0.951056, -0.968583,
            -0.982288, -0.992116, -0.998027, -0.999999, -0.998027, -0.992116, -0.982288, -0.968583,
            -0.951056, -0.929776, -0.904826, -0.876306, -0.844327, -0.809017, -0.770513, -0.728969,
            -0.684548, -0.637425, -0.587786, -0.535827, -0.481754,  -0.42578, -0.368125, -0.309017,
             -0.24869, -0.187381, -0.125333,    -0.063 };

        float output_signal[50] = {0};

        /*
        for (auto i = 0; i < 100; i++)
            std::cout << input_signal_sine_1hz_100[i] << std::endl;
        */
        float r           = 0.5f;   // resampling rate (output/input)
        unsigned int m    = 3;     // resampling filter semi-length (filter delay)
        float As          = 60.0f;  // resampling filter stop-band attenuation [dB]
        float bw          = 0.45f;  // resampling filter bandwidth
        unsigned int npfb = 64;     // number of filters in bank (timing resolution)
        unsigned int n    = 100;    // number of input samples

        // number of input samples (zero-padded)
        unsigned int nx = n + m;

        // output buffer with extra padding for good measure
        unsigned int y_len = (unsigned int) ceilf(1.1 * nx * r) + 4;

        // create resampler
        resamp_crcf q = resamp_crcf_create(r,m,bw,As,npfb);

        //input and output arrays
        liquid_float_complex x[nx];
        liquid_float_complex y[y_len];

        // Set values to zero
        memset(x,0,nx * sizeof(liquid_float_complex));
        memset(y,0,y_len * sizeof(liquid_float_complex));

        //Fill signal, complex form
        for (auto i = 0; i < 100; i++)
        {
            x[i].real = input_signal_sine_1hz_100[i];
            x[i].imag = 0;
        }

        unsigned int ny = 0;

        // execute on block of samples
        resamp_crcf_execute_block(q, x, nx, y, &ny);

        std::cout << "Output samples : " << ny << std::endl;

        //Fill signal, complex form
        for (auto i = 0; i < ny; i++)
        {
            std::cout << y[i].real <<" +i"<<y[i].imag << std::endl;
        }

        // clean up allocated objects
        resamp_crcf_destroy(q);

    }
#endif

#if 0
    //GSL
    TEST(GSL, Interpolation) {

        int i;
          double xi, yi, x[10], y[10];

          printf ("#m=0,S=2\n");

          for (i = 0; i < 10; i++)
            {
              x[i] = i + 0.5 * sin (i);
              y[i] = i + cos (i * i);
              printf ("%g %g\n", x[i], y[i]);
            }

          printf ("#m=1,S=0\n");

          {
            gsl_interp_accel *acc
              = gsl_interp_accel_alloc ();
            gsl_spline *spline
              = gsl_spline_alloc (gsl_interp_cspline, 10);

            gsl_spline_init (spline, x, y, 10);

            for (xi = x[0]; xi < x[9]; xi += 0.001)
              {
                yi = gsl_spline_eval (spline, xi, acc);
                printf ("%g %g\n", xi, yi);
              }
            gsl_spline_free (spline);
            gsl_interp_accel_free (acc);
          }
    }
 #endif

}

