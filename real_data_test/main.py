#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GPS_Rx_sim
# Author: dinanbai
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from fft_corr import fft_corr  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import main_epy_block_1 as epy_block_1  # embedded python block
import main_epy_block_3 as epy_block_3  # embedded python block
import numpy as np
import sip



class main(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "GPS_Rx_sim", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GPS_Rx_sim")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "main")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.bit_rate = bit_rate = 1023000
        self.samp_rate_usrp = samp_rate_usrp = sps*bit_rate
        self.samp_rate = samp_rate = 16367600
        self.IF = IF = 4130400

        ##################################################
        # Blocks
        ##################################################

        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'IF band')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'baseband')
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, 'Tab 2')
        self.top_layout.addWidget(self.tab)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            (1023*2), #size
            samp_rate/4, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1.set_y_axis((-60), (-20))
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_1.set_fft_window_normalized(False)



        labels = ['after filtering', 'before filtering', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.qwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._qtgui_freq_sink_x_0_1_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-60), (-20))
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['after filtering', 'before filtering', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0_0_0_0 = filter.interp_fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (samp_rate/4),
                2000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0_0 = filter.interp_fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (samp_rate/4),
                2000,
                window.WIN_HAMMING,
                6.76))
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(4, 0.25*np.array([1,1,1,1]))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.fft_corr_0_0_4 = fft_corr(
            sps=4,
        )
        self.fft_corr_0_0_3 = fft_corr(
            sps=4,
        )
        self.fft_corr_0_0_2 = fft_corr(
            sps=4,
        )
        self.fft_corr_0_0_1 = fft_corr(
            sps=4,
        )
        self.fft_corr_0_0_0 = fft_corr(
            sps=4,
        )
        self.fft_corr_0_0 = fft_corr(
            sps=4,
        )
        self.fft_corr_0 = fft_corr(
            sps=4,
        )
        self.epy_block_3 = epy_block_3.blk(sps=sps, fine_search_loopN=6, waiting_loopN=12)
        self.epy_block_1 = epy_block_1.blk(sps=sps, fine_search_loopN=6)
        self.blocks_vector_to_stream_2_2 = blocks.vector_to_stream(gr.sizeof_float*1, (1023*sps))
        self.blocks_vector_to_stream_2_1_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, (1023*sps))
        self.blocks_vector_to_stream_2_1_0 = blocks.vector_to_stream(gr.sizeof_float*1, (1023*sps))
        self.blocks_vector_to_stream_2_1 = blocks.vector_to_stream(gr.sizeof_float*1, (1023*sps))
        self.blocks_vector_to_stream_2_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, (1023*sps))
        self.blocks_vector_to_stream_2_0 = blocks.vector_to_stream(gr.sizeof_float*1, (1023*sps))
        self.blocks_vector_to_stream_2 = blocks.vector_to_stream(gr.sizeof_float*1, (1023*sps))
        self.blocks_vector_to_stream_1_2 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, (sps*1023))
        self.blocks_vector_to_stream_1_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, (sps*1023))
        self.blocks_vector_to_stream_1_0_1_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, (sps*1023))
        self.blocks_vector_to_stream_1_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, (sps*1023))
        self.blocks_vector_to_stream_1_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, (sps*1023))
        self.blocks_vector_to_stream_1_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, (sps*1023))
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, (sps*1023))
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((-1))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'I:\\GPS_Rx\\Data\\May15_2008_Guildford_DataSet1.dat', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, IF, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, IF, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_1, 'request_data'), (self.epy_block_3, 'request_data'))
        self.msg_connect((self.epy_block_1, 'PRN_ref_update'), (self.epy_block_3, 'PRN_ref_update'))
        self.msg_connect((self.epy_block_1, 'mode_update'), (self.epy_block_3, 'mode_update'))
        self.msg_connect((self.epy_block_1, 'freqlist_update'), (self.epy_block_3, 'freqlist_update'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.fft_corr_0, 0))
        self.connect((self.blocks_vector_to_stream_1_0, 0), (self.fft_corr_0_0, 0))
        self.connect((self.blocks_vector_to_stream_1_0_0, 0), (self.fft_corr_0_0_1, 0))
        self.connect((self.blocks_vector_to_stream_1_0_1, 0), (self.fft_corr_0_0_3, 0))
        self.connect((self.blocks_vector_to_stream_1_0_1_0, 0), (self.fft_corr_0_0_4, 0))
        self.connect((self.blocks_vector_to_stream_1_1, 0), (self.fft_corr_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_1_2, 0), (self.fft_corr_0_0_2, 0))
        self.connect((self.blocks_vector_to_stream_2, 0), (self.fft_corr_0, 1))
        self.connect((self.blocks_vector_to_stream_2_0, 0), (self.fft_corr_0_0, 1))
        self.connect((self.blocks_vector_to_stream_2_0_0, 0), (self.fft_corr_0_0_2, 1))
        self.connect((self.blocks_vector_to_stream_2_1, 0), (self.fft_corr_0_0_0, 1))
        self.connect((self.blocks_vector_to_stream_2_1_0, 0), (self.fft_corr_0_0_3, 1))
        self.connect((self.blocks_vector_to_stream_2_1_0_0, 0), (self.fft_corr_0_0_4, 1))
        self.connect((self.blocks_vector_to_stream_2_2, 0), (self.fft_corr_0_0_1, 1))
        self.connect((self.epy_block_3, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.epy_block_3, 1), (self.blocks_vector_to_stream_1_0, 0))
        self.connect((self.epy_block_3, 3), (self.blocks_vector_to_stream_1_0_0, 0))
        self.connect((self.epy_block_3, 5), (self.blocks_vector_to_stream_1_0_1, 0))
        self.connect((self.epy_block_3, 6), (self.blocks_vector_to_stream_1_0_1_0, 0))
        self.connect((self.epy_block_3, 2), (self.blocks_vector_to_stream_1_1, 0))
        self.connect((self.epy_block_3, 4), (self.blocks_vector_to_stream_1_2, 0))
        self.connect((self.epy_block_3, 7), (self.blocks_vector_to_stream_2, 0))
        self.connect((self.epy_block_3, 7), (self.blocks_vector_to_stream_2_0, 0))
        self.connect((self.epy_block_3, 7), (self.blocks_vector_to_stream_2_0_0, 0))
        self.connect((self.epy_block_3, 7), (self.blocks_vector_to_stream_2_1, 0))
        self.connect((self.epy_block_3, 7), (self.blocks_vector_to_stream_2_1_0, 0))
        self.connect((self.epy_block_3, 7), (self.blocks_vector_to_stream_2_1_0_0, 0))
        self.connect((self.epy_block_3, 7), (self.blocks_vector_to_stream_2_2, 0))
        self.connect((self.fft_corr_0, 0), (self.epy_block_1, 0))
        self.connect((self.fft_corr_0_0, 0), (self.epy_block_1, 1))
        self.connect((self.fft_corr_0_0_0, 0), (self.epy_block_1, 2))
        self.connect((self.fft_corr_0_0_1, 0), (self.epy_block_1, 3))
        self.connect((self.fft_corr_0_0_2, 0), (self.epy_block_1, 4))
        self.connect((self.fft_corr_0_0_3, 0), (self.epy_block_1, 5))
        self.connect((self.fft_corr_0_0_4, 0), (self.epy_block_1, 6))
        self.connect((self.fir_filter_xxx_0, 0), (self.epy_block_3, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_1, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.low_pass_filter_0_0_0_0, 0), (self.blocks_float_to_complex_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "main")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate_usrp(self.sps*self.bit_rate)
        self.epy_block_1.sps = self.sps
        self.epy_block_3.sps = self.sps

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.set_samp_rate_usrp(self.sps*self.bit_rate)

    def get_samp_rate_usrp(self):
        return self.samp_rate_usrp

    def set_samp_rate_usrp(self, samp_rate_usrp):
        self.samp_rate_usrp = samp_rate_usrp

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.samp_rate/4), 2000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.samp_rate/4), 2000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/4)

    def get_IF(self):
        return self.IF

    def set_IF(self, IF):
        self.IF = IF
        self.analog_sig_source_x_0.set_frequency(self.IF)
        self.analog_sig_source_x_0_0.set_frequency(self.IF)




def main(top_block_cls=main, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
