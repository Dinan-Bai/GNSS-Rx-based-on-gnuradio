import numpy as np
from gnuradio import gr
# from generate_prn_code import generate_prn_code  # Ensure this module is accessible

class blk(gr.basic_block):
    def __init__(self, sps = 4, PRN_ref=[1], delay_range = [0,1], delay_re = 1,dopp_range=[-500,500], dopp_re = 50):
        """
        Parameters:
        prn_numbers: List of PRN numbers to generate and sum.
        ref_prn: The specific PRN number to output for reference.
        """
        gr.basic_block.__init__(self,
            name="GPS_Correlator2",
            in_sig=[np.complex64],
            out_sig = None )
            # out_sig=[(np.float32, 1023), (np.float32, 1023)])  # Two output ports

        self.PRN_ref = PRN_ref
        self.delay_range = delay_range
        self.delay_re = delay_re
        self.dopp_range = dopp_range
        self.dopp_re = dopp_re
        self.sps = sps
        self.chunk_size = sps*1023
        self.Nloop = 0

    

    def general_work(self, input_items, output_items):
        """
        Cross-correlate the received signal with the local PRN code and frequency shifts.
        """
        # Input signal
        if self.Nloop <= 5:
            if len(input_items[0]) < self.chunk_size: # wait for enough data to load
                return 0
            else:
                self.consume(0,self.chunk_size)
                self.Nloop += 1
                print(self.Nloop)
                return 0
            
        rx_signal = input_items[0]

        # Check if we have enough data to process 1 code cycle
        code_cycle_len = 1023 * self.sps # 1 PRN code cycle length
        if len(rx_signal) < code_cycle_len:
            return 0  # Not enough data, wait for more samples

        # Extract one PRN code cycle
        signal_cycle = rx_signal[:code_cycle_len]

        PRN_num = self.PRN_ref[0]
        PRN_fname = './LUT/prn_'+str(PRN_num)+'.dat'
        PRN_local = np.fromfile(PRN_fname, dtype=np.int32)
        PRN_local = 2*PRN_local - 1
        PRN_local = np.repeat(PRN_local, self.sps)


        # Delay-Doppler Map Initialization
        delay_steps = int((self.delay_range[1] - self.delay_range[0]) / self.delay_re)
        doppler_steps = int((self.dopp_range[1] - self.dopp_range[0]) / self.dopp_re)
        delay_doppler_map = np.zeros((delay_steps, doppler_steps), dtype=np.complex64)

        # Frequency step size (Hz)
        freq_step = self.dopp_re
        fs = self.sps * 1.023e6  # Sampling rate (4 x GPS chip rate)

        # Loop over delay and Doppler ranges
        for d_idx, delay in enumerate(range(self.delay_range[0], self.delay_range[1], self.delay_re)):
            # Apply delay (circular shift)
            shifted_prn = np.roll(PRN_local, delay)

            for f_idx, doppler in enumerate(range(self.dopp_range[0], self.dopp_range[1], freq_step)):
                # Generate Doppler frequency-shifted local PRN code
                freq_shift = np.exp(1j * 2 * np.pi * doppler * np.arange(code_cycle_len) / fs)
                doppler_prn = shifted_prn * freq_shift

                # Cross-correlation with the received signal
                correlation = np.dot(signal_cycle, np.conj(doppler_prn))
                delay_doppler_map[d_idx, f_idx] = correlation

            if d_idx % 10 == 0:
                print(f"Processed delay step {d_idx}/{delay_steps}")

        # Save the delay-Doppler map to a file
        np.savez_compressed(
            f"delay_doppler_map_prn_{PRN_num}.npz",  # Save as .npz file
            delay_doppler_map=delay_doppler_map,
            delay_range=self.delay_range,
            delay_re=self.delay_re,
            dopp_range=self.dopp_range,
            dopp_re=self.dopp_re
        )
        print("file saved!")

        # Consume the processed samples
        self.consume_each(code_cycle_len)


        return 0

