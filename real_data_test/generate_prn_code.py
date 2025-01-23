def generate_prn_code(sv):
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

    return ca

