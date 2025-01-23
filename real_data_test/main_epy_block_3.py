import numpy as np
from gnuradio import gr
import copy
import pmt

class blk(gr.basic_block):
    def __init__(self, sps=4,fine_search_loopN = 6,waiting_loopN = 0):
        gr.basic_block.__init__(
            self,
            name="Clip and Process Vector",  # Block name
            in_sig=[np.complex64],           # Streaming input
            out_sig=[(np.complex64, sps * 1023),
                     (np.complex64, sps * 1023),
                     (np.complex64, sps * 1023),
                     (np.complex64, sps * 1023),
                     (np.complex64, sps * 1023),
                     (np.complex64, sps * 1023),
                     (np.complex64, sps * 1023),
                     (np.float32, sps*1023),
                     ]  # Output fixed-size vector
        )
        self.sps = sps
        self.chunk_size = sps * 1023  # Fixed vector size
        self.fine_search_loopN = fine_search_loopN
        self.state = 0
        self.num_channels = 7
        self.Nloop = 0
        self.PRN_ref = [1]
        self.mode = 0 # 0: cold start # 1: tracking mode
        self.reg = [0+0j]*self.chunk_size
        self.PRN_local = [0] * self.chunk_size
        self.freq_search_list = [-1500,-1000,-500,0,500,1000,1500]
        self.load_data = 0
        self.fs = self.sps*1.023e6
        self.track_loopN = 0
        self.waiting_loopN = waiting_loopN
        

        self.message_port_register_in(pmt.intern("request_data"))
        self.set_msg_handler(pmt.intern("request_data"), self.handle_request_data)
        self.message_port_register_in(pmt.intern("mode_update"))
        self.set_msg_handler(pmt.intern("mode_update"), self.handle_mode_update)
        self.message_port_register_in(pmt.intern("freqlist_update"))
        self.set_msg_handler(pmt.intern("freqlist_update"), self.handle_freqlist_update)
        self.message_port_register_in(pmt.intern("PRN_ref_update"))
        self.set_msg_handler(pmt.intern("PRN_ref_update"), self.handle_PRN_ref_update)
        
    def generate_prn_code(self,sv):
        """Generate GPS Satellite PRN Code (C/A Code)
        
        :param int sv: satellite code (1-32)
        :returns list: PRN code for chosen satellite
        """
        SV = {
            1: [2,6], 2: [3,7], 3: [4,8], 4: [5,9], 5: [1,9], 
            6: [2,10], 7: [1,8], 8: [2,9], 9: [3,10], 10: [2,3],
            11: [3,4], 12: [5,6], 13: [6,7], 14: [7,8], 15: [8,9],
            16: [9,10], 17: [1,4], 18: [2,5], 19: [3,6], 20: [4,7],
            21: [5,8], 22: [6,9], 23: [1,3], 24: [4,6], 25: [5,7],
            26: [6,8], 27: [7,9], 28: [8,10], 29: [1,6], 30: [2,7],
            31: [3,8], 32: [4,9]
        }

        def shift(register, feedback, output):
            """Perform shift register operation"""
            out = [register[i-1] for i in output]
            out = sum(out) % 2 if len(out) > 1 else out[0]
            fb = sum(register[i-1] for i in feedback) % 2
            register[1:] = register[:-1]
            register[0] = fb
            return out

        G1 = [1] * 10
        G2 = [1] * 10
        ca = []

        for _ in range(1023):
            g1 = shift(G1, [3,10], [10])
            g2 = shift(G2, [2,3,6,8,9,10], SV[sv])
            ca.append((g1 + g2) % 2)

        ca = np.array(ca,dtype = np.float32)
        return ca
    
    def handle_request_data(self, msg):
        # Check if the message is a PMT pair
        if pmt.is_pair(msg):
            key = pmt.car(msg)  # Extract the key
            value = pmt.cdr(msg)  # Extract the value

            # Check the key and process the value
            if pmt.symbol_to_string(key) == "load_data" and pmt.is_number(value):
                self.load_data = pmt.to_double(value)  # Convert to Python float
                # print(f"Received load_data: {self.load_data}")
            else:
                self.load_data = 0
        else:
            self.load_data = 0

    def handle_PRN_ref_update(self, msg):
        # Check if the message is a PMT pair
        # Process the "freqlist_update" message
        if pmt.is_pair(msg):
            key = pmt.car(msg)
            value = pmt.cdr(msg)

            if pmt.symbol_to_string(key) == "PRN_ref" and pmt.is_f32vector(value):
                self.PRN_ref = np.array(pmt.f32vector_elements(value))
                # print(f"updated PRN ref = {self.PRN_ref[0]}")
                PRN_local = self.generate_prn_code(self.PRN_ref[0])
                PRN_local = 2*PRN_local - 1
                PRN_local = np.repeat(PRN_local, self.sps)
                self.PRN_local = PRN_local
            else:
                print("Invalid key or value in the PRN_ref_update message")
        else:
            print("Message on freqlist_update is not a PMT pair")

    def handle_mode_update(self, msg):
        # Check if the message is a PMT pair
        if pmt.is_pair(msg):
            key = pmt.car(msg)  # Extract the key
            value = pmt.cdr(msg)  # Extract the value

            # Check the key and process the value
            if pmt.symbol_to_string(key) == "mode" and pmt.is_number(value):
                self.mode = pmt.to_double(value)  # Convert to Python float
                #print("tracking mode starts")
            else:
                self.mode= 0
        else:
            self.mode = 0

    def handle_freqlist_update(self, msg):
        # Process the "freqlist_update" message
        if pmt.is_pair(msg):
            key = pmt.car(msg)
            value = pmt.cdr(msg)

            if pmt.symbol_to_string(key) == "freq_search_list" and pmt.is_f32vector(value):
                self.freq_search_list = np.array(pmt.f32vector_elements(value))
            else:
                print("Invalid key or value in the freqlist_update message")
        else:
            print("Message on freqlist_update is not a PMT pair")



    def general_work(self, input_items, output_items):
        # Just for simulation test
        if self.Nloop <= self.waiting_loopN:
            if len(input_items[0]) < self.chunk_size: # wait for enough data to load
                return 0
            else:
                self.consume(0,self.chunk_size)
                self.Nloop += 1
                print(self.Nloop)
                return 0
        # end

        
        if self.mode == 0: # Cold start mode
            if self.state == 1:  # register mode (or sleeping mode)
                if self.load_data == 0:
                    self.consume(0,self.chunk_size)
                    return 0
                elif self.load_data == 1: # the processor requests data
                    # print(f"Received frequency list: {freq_search_list}")
                    for ii in range(self.num_channels):
                        freq_shift = np.exp(-1j * 2 * np.pi * self.freq_search_list[ii] * np.arange(1023*4) / (self.fs))
                        output_items[ii][0,:] = self.reg * freq_shift
                    output_items[self.num_channels][0,:] = self.PRN_local[:]
                    self.load_data = 0
                    self.consume(0, self.chunk_size)
                    return 1
            
            elif self.state == 0: # cold start first loop, save data into register
                if len(input_items[0]) < self.chunk_size: # wait for enough data to load
                    return 0
                # once get enough data, store one chunck (4*1023 samples) into the register
                # Clip the first `sps * 1023` samples
                # only for the first run
                # print('first loop, PRN ref = ',self.PRN_ref[0])
                clipped_data = input_items[0][:self.chunk_size]
                self.reg = copy.deepcopy(clipped_data)
                PRN_local = self.generate_prn_code(self.PRN_ref[0])
                PRN_local = 2*PRN_local - 1
                PRN_local = np.repeat(PRN_local, self.sps)
                self.PRN_local = PRN_local
                
                # load freq LO vector to the register
                for ii in range(self.num_channels):
                    freq_shift = np.exp(-1j * 2 * np.pi * self.freq_search_list[ii] * np.arange(1023*self.sps) / self.fs)
                    output_items[ii][0,:] = self.reg * freq_shift
                output_items[self.num_channels][0,:] = self.PRN_local[:]
                # print('registers loaded')

                self.consume(0, self.chunk_size)
                self.state = 1

                return 1

        elif self.mode == 1:
            # print("Traking Mode")
            if len(input_items[0]) < self.chunk_size: # wait for one code length data to load
                return 0
            else:
                if self.track_loopN == 0:
                    print(f'Tracking starts, lock on PRN {self.PRN_ref[0]},central dopp={self.freq_search_list[3]},dopp re={self.freq_search_list[3]-self.freq_search_list[2]}')
                clipped_data = input_items[0][:self.chunk_size]
                for ii in range(self.num_channels):
                    freq_shift = np.exp(-1j * 2 * np.pi * self.freq_search_list[ii] * np.arange(1023*self.sps) / self.fs)
                    output_items[ii][0,:] = clipped_data* freq_shift
                output_items[self.num_channels][0,:] = self.PRN_local
                self.consume(0, self.chunk_size)
                self.track_loopN += 1
                if self.track_loopN % 1000 == 0:
                    print(f"Time Passed {self.track_loopN/1000} sec")
                return 1
