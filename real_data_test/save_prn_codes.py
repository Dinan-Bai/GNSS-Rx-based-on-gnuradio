import numpy as np
from generate_prn_code import generate_prn_code  # Ensure this module contains the PRN generation function


def save_prn_to_file(prn_number, directory="prn_files"):
    """
    Generate a PRN code and save it to a file.
    :param prn_number: PRN number to generate.
    :param directory: Directory to save the PRN files.
    """
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate PRN code
    prn_code = generate_prn_code(prn_number)
    prn_code = np.array(prn_code, dtype=np.int32)  # Ensure int32 type

    # Save to file
    filename = f"{directory}/prn_{prn_number}.dat"
    prn_code.tofile(filename)  # Save as binary
    print(f"Saved PRN {prn_number} to {filename}")

# Generate and save PRN codes for a range of numbers
if __name__ == "__main__":
    for prn in range(1, 33):  # Example: PRN numbers 1 to 32
        save_prn_to_file(prn,'./LUT')