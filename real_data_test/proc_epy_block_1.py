"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,sps=4, fine_search_loopN = 6):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Central_Processor',   # will show up in GRC
            in_sig=[np.complex64]*7,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sps = sps
        self.N_channel = 7
        self.fine_search_loopN = fine_search_loopN
        self.fd_init = 0
        self.del_f_init = 500
        self.fdp = 0        # updated central fd 
        self.del_fp = 500    # updated search resolution 
        self.coarse_search_fd = [self.fd_init,
                                 self.fd_init + self.N_channel*self.del_f_init,
                                 -self.fd_init - self.N_channel*self.del_f_init,
                                 self.fd_init + 2*self.N_channel*self.del_f_init,
                                 -self.fd_init - 2*self.N_channel*self.del_f_init
                                 ]
        self.PRN_search_list = [0]
        self.coarse_search_step = 0
        self.PRN_code_len = 1023
        self.PRN_ref = [1]*7
        self.flag = 0         # system flag
        self.search_state = 0 # 0: coarse search; 1: fine search
        self.search_loopN = 0 # counting how many loops are used in the DDM search
        self.mode = 0         # 0: cold start 1: tracking mode

        self.track_PRN = 0
        self.track_delay = 0
        self.track_doppler = 0
        self.track_phase = 0
        self.PRN_peak_SNR = 0
        self.track_del_doppler = 10

        self.track_loopN = 0

        
        self.message_port_register_out(pmt.intern("request_data"))
        self.message_port_register_out(pmt.intern("freqlist_update"))
        self.message_port_register_out(pmt.intern("PRN_ref_update"))
        self.message_port_register_out(pmt.intern("mode_update"))


    def general_work(self, input_items, output_items):

        chunk_size = self.sps * self.PRN_code_len  # Number of samples to process per call

        if self.mode == 0: # Cold start mode

            if self.flag == 1:
                self.consume_each(len(input_items[0]))
                return 0
            
            if len(input_items[0]) < chunk_size:
                return 0
            freq_search_list = self.fdp + (np.array(range(self.N_channel))-3) * self.del_fp

            DDM = np.array([input_items[ch][:chunk_size] for ch in range(self.N_channel)])
            DDM_abs = np.abs(DDM)
            DDM_abs[DDM_abs == 0] = np.nan
            max_idx = np.argmax(DDM_abs)
            peak_magnitude = DDM_abs.flat[max_idx]
            peak_channel, peak_delay = np.unravel_index(max_idx, DDM_abs.shape)
            delay = peak_delay / self.sps  # Convert sample index to chip delay
            doppler = freq_search_list[peak_channel]  # Doppler shift
            phase = np.angle(DDM[peak_channel][peak_delay])

            flattened_map = DDM_abs.flatten()
            avg_signal = np.nanmean(flattened_map[flattened_map != peak_magnitude])  # Exclude the peak
            std_signal = np.nanstd(flattened_map[flattened_map != peak_magnitude])
            snr_avg = 10 * np.log10(peak_magnitude / avg_signal)
            snr_std = (peak_magnitude - avg_signal) / std_signal
            # print(f"snr_avg = {snr_avg}, snr_std = {snr_std}")
            
            # Check if the peak is valid (SNR > 4 dB)
            # print(f"################# PRN = {self.PRN_ref[0]}, Search Loop = {self.search_loopN} ##############")
            if self.search_state == 0: 
                
                if snr_avg > 6 and snr_std > 7:
                    print(f"PRN {self.PRN_ref[0]} Coarse Search Starts")
                    # Generate a refined Doppler frequency search list around the detected Doppler
                    self.fdp = doppler
                    self.del_fp = self.del_fp/3
                    self.search_state = 1 # switch to fine resolution search     
                    self.coarse_search_step = 0 # reset the coarse search counting
                    print(f"Coarse Search Found: Delay={delay:.2f} chips, Doppler={doppler:.2f} Hz, SNR={snr_avg:.2f} dB")
                    print(f"Coarse Search Phase: {phase/np.pi*180} deg")       
                    print(f"PRN {self.PRN_ref[0]} Fine Search Starts")   
                else:
                    self.coarse_search_step += 1
                    if self.coarse_search_step <= len(self.coarse_search_fd)-1:
                        self.fdp = self.coarse_search_fd[self.coarse_search_step]
                        self.del_fp = self.del_f_init
                    else:
                        print(f"PRN {self.PRN_ref[0]} not found\n")
                        self.coarse_search_step = 0 # reset coarse search counting to 0
                        self.search_state = 0
                        self.fdp = self.fd_init
                        self.del_fp = self.del_f_init

                        self.PRN_ref = [x+1 for x in self.PRN_ref]
                        if self.PRN_ref[0] >= 33:
                            self.mode = 1
                            mode_msg = pmt.cons(pmt.intern("mode"), pmt.from_float(self.mode))
                            self.message_port_pub(pmt.intern('mode_update'),mode_msg)
                            print('Enter Tracking Mode \n')
                            return 0
                        else:   
                            PRN_search_pmt = pmt.init_f32vector(self.N_channel, self.PRN_ref)
                            message_PRN_ref = pmt.cons(pmt.intern("PRN_ref"), PRN_search_pmt)
                            self.message_port_pub(pmt.intern('PRN_ref_update'),message_PRN_ref)


            elif self.search_state == 1: # fine resolution fd search
                
                self.search_loopN += 1
                self.fdp = doppler
                self.del_fp = self.del_fp/3

                if self.search_loopN >= self.fine_search_loopN: # each fine search loop iterates N times
                                                                # Then switch to the next PRN
                    
                    print(f"Fine Search Found: Delay={delay:.2f} chips, Doppler={doppler:.2f} Hz, SNR={snr_avg:.2f} dB")
                    print(f"find Search Phase: {phase/np.pi*180} deg\n")
                    # update the PRN search parameters
                    if snr_std > self.PRN_peak_SNR:
                        self.PRN_peak_SNR = snr_std
                        self.track_delay = peak_delay
                        self.track_doppler = doppler
                        self.track_phase = phase
                        self.track_PRN = self.PRN_ref[0]

                    self.search_state = 0   # reset the coarse search mode
                    self.fdp = self.fd_init
                    self.del_fp = self.del_f_init
                    self.search_loopN = 0    
                    self.PRN_ref = [x+1 for x in self.PRN_ref]
                    if self.PRN_ref[0] >= 33: # the end of PRN search, switch to tracking mode              
                        self.mode = 1
                        self.PRN_ref = [1]*7
                        return 0
                    else: # if it is not the end of the PRN search, feedback the PRN to correlator unit                        
                        PRN_search_pmt = pmt.init_f32vector(7, self.PRN_ref)
                        message_PRN_ref = pmt.cons(pmt.intern("PRN_ref"), PRN_search_pmt)
                        self.message_port_pub(pmt.intern('PRN_ref_update'),message_PRN_ref)
                        
                                        

            refined_doppler_list = self.fdp + (np.array(range(self.N_channel))-3) * self.del_fp
            refined_doppler_list = refined_doppler_list.tolist()

            freq_search_pmt = pmt.init_f32vector(7, refined_doppler_list)
            message4 = pmt.cons(pmt.intern("freq_search_list"), freq_search_pmt)
            self.message_port_pub(pmt.intern('freqlist_update'), message4)

            message1 = pmt.cons(pmt.intern("load_data"), pmt.from_float(1))
            self.message_port_pub(pmt.intern('request_data'),message1)

                


            
            # Consume all input samples
            self.consume_each(chunk_size)
            return 0
        
        elif self.mode == 1: # tracking mode
            # write the tracking lock loops here
            if len(input_items[0]) < chunk_size:
                return 0
            doppler_search = self.track_doppler+ (np.array(range(self.N_channel))-3) * self.track_del_doppler
            if self.track_loopN == 0: # first tracking loop
                if self.track_PRN != 0:
                    # update Local PRN
                    
                    track_PRN = [self.track_PRN]*7    
            
                    PRN_search_pmt = pmt.init_f32vector(7, track_PRN)
                    message_PRN_ref = pmt.cons(pmt.intern("PRN_ref"), PRN_search_pmt)
                    self.message_port_pub(pmt.intern('PRN_ref_update'),message_PRN_ref)
                    # update LO freq
                    freq_search_pmt = pmt.init_f32vector(7, doppler_search)
                    message4 = pmt.cons(pmt.intern("freq_search_list"), freq_search_pmt)
                    self.message_port_pub(pmt.intern('freqlist_update'), message4)

                    self.track_loopN += 1
                # else: # restart the searching
                #     self.mode = 0
                #     mode_msg = pmt.cons(pmt.intern("mode"), pmt.from_float(self.mode))
                #     self.message_port_pub(pmt.intern('mode_update'),mode_msg)
                #     self.fdp = self.fd_init
                #     self.del_fp = self.del_f_init
            else: # start with the 2nd loop of tracking
                DDM = np.array([input_items[ch][:chunk_size] for ch in range(self.N_channel)])
                DDM_abs = np.abs(DDM)
                DDM_abs[DDM_abs == 0] = np.nan
                max_idx = np.argmax(DDM_abs)
                peak_magnitude = DDM_abs.flat[max_idx]
                peak_channel, peak_delay = np.unravel_index(max_idx, DDM_abs.shape)
                delay = peak_delay / self.sps  # Convert sample index to chip delay
                doppler = doppler_search[peak_channel]  # Doppler shift
                phase = np.angle(DDM[peak_channel][peak_delay])

                flattened_map = DDM_abs.flatten()
                avg_signal = np.nanmean(flattened_map[flattened_map != peak_magnitude])  # Exclude the peak
                std_signal = np.nanstd(flattened_map[flattened_map != peak_magnitude])
                snr_avg = 10 * np.log10(peak_magnitude / avg_signal)
                snr_std = (peak_magnitude - avg_signal) / std_signal

                # update tracking central dopp and delta_dopp
                doppler_search_new = self.track_doppler+ (np.array(range(self.N_channel))-3) * self.track_del_doppler
            
                freq_search_pmt = pmt.init_f32vector(7, doppler_search_new)
                message4 = pmt.cons(pmt.intern("freq_search_list"), freq_search_pmt)
                self.message_port_pub(pmt.intern('freqlist_update'), message4)

                self.track_loopN += 1

            self.consume_each(len(input_items[0]))
            return 0
        

        
        
        
        # # # update doppler searching range
        # if self.search_loopN == 2:
            
        #     self.search_loopN = 0 # end search, and shift to next PRN
        #     self.fdp = self.fd_init # initialize dopp search range
        #     self.del_fp = self.del_f_init
        #     self.flag = 1 # end search (later change it to end after 32 PRN are all searched)
        #     message3 = pmt.cons(pmt.intern("load_data"), pmt.from_float(0))
        #     self.message_port_pub(pmt.intern('request_data'),message3)
        # else:
        #     self.search_loopN += 1
        #     self.fdp = -1300 #freq_search_max
        #     self.del_fp = 100
        #     message3 = pmt.cons(pmt.intern("load_data"), pmt.from_float(1))
        #     self.message_port_pub(pmt.intern('request_data'),message3)

        #     freq_search_list = self.fdp + (np.array(range(num_channels))-3) * self.del_fp
        #     freq_search_pmt = pmt.init_f32vector(7, freq_search_list)
        #     message4 = pmt.cons(pmt.intern("freqlist_update"), freq_search_pmt)
        #     self.message_port_pub(pmt.intern('freqlist_update'), message4)

        return 0
