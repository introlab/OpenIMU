#TODO Compile liquid-dsp lib
message(STATUS "building liquid-dsp library wrapper")

#Added a selection of DSP functions taken from
#liquid-dsp library

include_directories(
    liquid-dsp/include
    ${CMAKE_CURRENT_BINARY_DIR}
    )

add_definitions(-DNothing)

configure_file(config.h.in config.h)

#Base directory where liquid-dsp files are
set(liquid-dsp-src-dir liquid-dsp/src)

#TODO REMOVE UNWANTED FILES?
set(liquid-dsp-srcs
    ${liquid-dsp-src-dir}/libliquid.c
    ${liquid-dsp-src-dir}/agc/src/agc_crcf.c
    ${liquid-dsp-src-dir}/agc/src/agc_rrrf.c
    ${liquid-dsp-src-dir}/audio/src/cvsd.c
    ${liquid-dsp-src-dir}/buffer/src/bufferf.c
    ${liquid-dsp-src-dir}/buffer/src/buffercf.c
    ${liquid-dsp-src-dir}/channel/src/channel_cccf.c
    ${liquid-dsp-src-dir}/dotprod/src/dotprod_cccf.mmx.c
    ${liquid-dsp-src-dir}/dotprod/src/dotprod_crcf.mmx.c
    ${liquid-dsp-src-dir}/dotprod/src/dotprod_rrrf.mmx.c
    ${liquid-dsp-src-dir}/dotprod/src/sumsq.mmx.c
    ${liquid-dsp-src-dir}/equalization/src/equalizer_cccf.c
    ${liquid-dsp-src-dir}/equalization/src/equalizer_cccf.c
    ${liquid-dsp-src-dir}/equalization/src/equalizer_rrrf.c
    ${liquid-dsp-src-dir}/fec/src/crc.c
    ${liquid-dsp-src-dir}/fec/src/fec.c
    ${liquid-dsp-src-dir}/fec/src/fec_conv.c
    ${liquid-dsp-src-dir}/fec/src/fec_conv_poly.c
    ${liquid-dsp-src-dir}/fec/src/fec_conv_pmatrix.c
    ${liquid-dsp-src-dir}/fec/src/fec_conv_punctured.c
    ${liquid-dsp-src-dir}/fec/src/fec_golay2412.c
    ${liquid-dsp-src-dir}/fec/src/fec_hamming74.c
    ${liquid-dsp-src-dir}/fec/src/fec_hamming84.c
    ${liquid-dsp-src-dir}/fec/src/fec_hamming128.c
    ${liquid-dsp-src-dir}/fec/src/fec_hamming1511.c
    ${liquid-dsp-src-dir}/fec/src/fec_hamming3126.c
    ${liquid-dsp-src-dir}/fec/src/fec_hamming128_gentab.c
    ${liquid-dsp-src-dir}/fec/src/fec_pass.c
    ${liquid-dsp-src-dir}/fec/src/fec_rep3.c
    ${liquid-dsp-src-dir}/fec/src/fec_rep5.c
    ${liquid-dsp-src-dir}/fec/src/fec_rs.c
    ${liquid-dsp-src-dir}/fec/src/fec_secded2216.c
    ${liquid-dsp-src-dir}/fec/src/fec_secded3932.c
    ${liquid-dsp-src-dir}/fec/src/fec_secded7264.c
    ${liquid-dsp-src-dir}/fec/src/interleaver.c
    ${liquid-dsp-src-dir}/fec/src/packetizer.c
    ${liquid-dsp-src-dir}/fec/src/sumproduct.c
    ${liquid-dsp-src-dir}/fft/src/fftf.c
    ${liquid-dsp-src-dir}/fft/src/spgramcf.c
    ${liquid-dsp-src-dir}/fft/src/spgramf.c
    ${liquid-dsp-src-dir}/fft/src/fft_utilities.c
    ${liquid-dsp-src-dir}/filter/src/bessel.c
    ${liquid-dsp-src-dir}/filter/src/butter.c
    ${liquid-dsp-src-dir}/filter/src/cheby1.c
    ${liquid-dsp-src-dir}/filter/src/cheby2.c
    ${liquid-dsp-src-dir}/filter/src/ellip.c
    ${liquid-dsp-src-dir}/filter/src/filter_rrrf.c
    ${liquid-dsp-src-dir}/filter/src/filter_crcf.c
    ${liquid-dsp-src-dir}/filter/src/filter_cccf.c
    ${liquid-dsp-src-dir}/filter/src/firdes.c
    ${liquid-dsp-src-dir}/filter/src/firdespm.c
    ${liquid-dsp-src-dir}/filter/src/fnyquist.c
    ${liquid-dsp-src-dir}/filter/src/gmsk.c
    ${liquid-dsp-src-dir}/filter/src/group_delay.c
    ${liquid-dsp-src-dir}/filter/src/hM3.c
    ${liquid-dsp-src-dir}/filter/src/iirdes.pll.c
    ${liquid-dsp-src-dir}/filter/src/iirdes.c
    ${liquid-dsp-src-dir}/filter/src/lpc.c
    ${liquid-dsp-src-dir}/filter/src/rcos.c
    ${liquid-dsp-src-dir}/filter/src/rkaiser.c
    ${liquid-dsp-src-dir}/filter/src/rrcos.c
    ${liquid-dsp-src-dir}/framing/src/bpacketgen.c
    ${liquid-dsp-src-dir}/framing/src/bpacketsync.c
    ${liquid-dsp-src-dir}/framing/src/bpresync_cccf.c
    ${liquid-dsp-src-dir}/framing/src/bsync_rrrf.c
    ${liquid-dsp-src-dir}/framing/src/bsync_crcf.c
    ${liquid-dsp-src-dir}/framing/src/bsync_cccf.c
    ${liquid-dsp-src-dir}/framing/src/detector_cccf.c
    ${liquid-dsp-src-dir}/framing/src/framedatastats.c
    ${liquid-dsp-src-dir}/framing/src/framesyncstats.c
    ${liquid-dsp-src-dir}/framing/src/framegen64.c
    ${liquid-dsp-src-dir}/framing/src/framesync64.c
    ${liquid-dsp-src-dir}/framing/src/flexframegen.c
    ${liquid-dsp-src-dir}/framing/src/flexframesync.c
    ${liquid-dsp-src-dir}/framing/src/gmskframegen.c
    ${liquid-dsp-src-dir}/framing/src/gmskframesync.c
    ${liquid-dsp-src-dir}/framing/src/msourcecf.c
    ${liquid-dsp-src-dir}/framing/src/ofdmflexframegen.c
    ${liquid-dsp-src-dir}/framing/src/ofdmflexframesync.c
    ${liquid-dsp-src-dir}/framing/src/presync_cccf.c
    ${liquid-dsp-src-dir}/framing/src/symstreamcf.c
    ${liquid-dsp-src-dir}/framing/src/symtrack_cccf.c
    ${liquid-dsp-src-dir}/framing/src/qdetector_cccf.c
    ${liquid-dsp-src-dir}/framing/src/qpacketmodem.c
    ${liquid-dsp-src-dir}/framing/src/qpilotgen.c
    ${liquid-dsp-src-dir}/framing/src/qpilotsync.c
    ${liquid-dsp-src-dir}/math/src/poly.c
    ${liquid-dsp-src-dir}/math/src/polyc.c
    ${liquid-dsp-src-dir}/math/src/polyf.c
    ${liquid-dsp-src-dir}/math/src/polycf.c
    ${liquid-dsp-src-dir}/math/src/math.c
    ${liquid-dsp-src-dir}/math/src/math.bessel.c
    ${liquid-dsp-src-dir}/math/src/math.gamma.c
    ${liquid-dsp-src-dir}/math/src/math.complex.c
    ${liquid-dsp-src-dir}/math/src/math.trig.c
    ${liquid-dsp-src-dir}/math/src/modular_arithmetic.c
    ${liquid-dsp-src-dir}/math/src/windows.c
    ${liquid-dsp-src-dir}/matrix/src/matrix.c
    ${liquid-dsp-src-dir}/matrix/src/matrixf.c
    ${liquid-dsp-src-dir}/matrix/src/matrixc.c
    ${liquid-dsp-src-dir}/matrix/src/matrixcf.c
    ${liquid-dsp-src-dir}/matrix/src/smatrix.common.c
    ${liquid-dsp-src-dir}/matrix/src/smatrixb.c
    ${liquid-dsp-src-dir}/matrix/src/smatrixf.c
    ${liquid-dsp-src-dir}/matrix/src/smatrixi.c
    ${liquid-dsp-src-dir}/modem/src/ampmodem.c
    ${liquid-dsp-src-dir}/modem/src/cpfskdem.c
    ${liquid-dsp-src-dir}/modem/src/cpfskmod.c
    ${liquid-dsp-src-dir}/modem/src/fskdem.c
    ${liquid-dsp-src-dir}/modem/src/fskmod.c
    ${liquid-dsp-src-dir}/modem/src/gmskdem.c
    ${liquid-dsp-src-dir}/modem/src/gmskmod.c
    ${liquid-dsp-src-dir}/modem/src/modemf.c
    ${liquid-dsp-src-dir}/modem/src/modem_utilities.c
    ${liquid-dsp-src-dir}/modem/src/modem_apsk_const.c
    ${liquid-dsp-src-dir}/modem/src/modem_arb_const.c
    ${liquid-dsp-src-dir}/multichannel/src/firpfbch_crcf.c
    ${liquid-dsp-src-dir}/multichannel/src/firpfbch_cccf.c
    ${liquid-dsp-src-dir}/multichannel/src/ofdmframe.common.c
    ${liquid-dsp-src-dir}/multichannel/src/ofdmframegen.c
    ${liquid-dsp-src-dir}/multichannel/src/ofdmframesync.c
    ${liquid-dsp-src-dir}/nco/src/nco_crcf.c
    ${liquid-dsp-src-dir}/nco/src/nco.utilities.c
    ${liquid-dsp-src-dir}/optim/src/chromosome.c
    ${liquid-dsp-src-dir}/optim/src/gasearch.c
    ${liquid-dsp-src-dir}/optim/src/gradsearch.c
    ${liquid-dsp-src-dir}/optim/src/optim.common.c
    ${liquid-dsp-src-dir}/optim/src/qnsearch.c
    ${liquid-dsp-src-dir}/optim/src/utilities.c
    ${liquid-dsp-src-dir}/quantization/src/compand.c
    ${liquid-dsp-src-dir}/quantization/src/quantizercf.c
    ${liquid-dsp-src-dir}/quantization/src/quantizerf.c
    ${liquid-dsp-src-dir}/quantization/src/quantizer.inline.c
    ${liquid-dsp-src-dir}/random/src/rand.c
    ${liquid-dsp-src-dir}/random/src/randn.c
    ${liquid-dsp-src-dir}/random/src/randexp.c
    ${liquid-dsp-src-dir}/random/src/randweib.c
    ${liquid-dsp-src-dir}/random/src/randgamma.c
    ${liquid-dsp-src-dir}/random/src/randnakm.c
    ${liquid-dsp-src-dir}/random/src/randricek.c
    ${liquid-dsp-src-dir}/random/src/scramble.c
    ${liquid-dsp-src-dir}/sequence/src/bsequence.c
    ${liquid-dsp-src-dir}/sequence/src/msequence.c
    ${liquid-dsp-src-dir}/utility/src/bshift_array.c
    ${liquid-dsp-src-dir}/utility/src/byte_utilities.c
    ${liquid-dsp-src-dir}/utility/src/msb_index.c
    ${liquid-dsp-src-dir}/utility/src/pack_bytes.c
    ${liquid-dsp-src-dir}/utility/src/shift_array.c
    ${liquid-dsp-src-dir}/vector/src/vectorf_add.port.c
    ${liquid-dsp-src-dir}/vector/src/vectorf_norm.port.c
    ${liquid-dsp-src-dir}/vector/src/vectorf_mul.port.c
    ${liquid-dsp-src-dir}/vector/src/vectorf_trig.port.c
    ${liquid-dsp-src-dir}/vector/src/vectorcf_add.port.c
    ${liquid-dsp-src-dir}/vector/src/vectorcf_norm.port.c
    ${liquid-dsp-src-dir}/vector/src/vectorcf_mul.port.c
    ${liquid-dsp-src-dir}/vector/src/vectorcf_trig.port.c
    #Auto generated config.h
    ${CMAKE_CURRENT_BINARY_DIR}/config.h

)

add_library(liquid-dsp STATIC ${liquid-dsp-srcs} config.h.in)
set_property(TARGET liquid-dsp PROPERTY C_STANDARD 99)

set(LIQUIDDSP_INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/liquid-dsp/include CACHE INTERNAL "doc string")
set(LIQUIDDSP_LIBS liquid-dsp CACHE INTERNAL "doc string")

