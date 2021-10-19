import argparse
import os
import sys
from time import sleep

class GenerateFiles():
    """Class to handle generation of files
    """

    def __init__(self, action, num_of_files, delay):
        self.action = action
        self.num_of_files = num_of_files
        self.delay = delay

    def generate_files(self):
        if self.delay is None:
            if self.action == "HASH_GEN":
                for i in range(0,self.num_of_files):
                    print("Generating file_" + str(i+1) + "...")
                    with open("/samba/enclave/hash_generation/file_" + str(i+1) + ".txt", "w+") as out_file:
                        out_file.write(str(i+1))
            elif self.action == "VERIFY_HASH":
                for i in range(0,self.num_of_files):
                    print("Generating file_" + str(i+1) + "...")
                    with open("/samba/enclave/verify_hash/request_hash/file_" + str(i+1) + ".txt", "w+") as out_file:
                        out_file.write(str(i+1))
        else:
            if self.action == "HASH_GEN":
                for i in range(0,self.num_of_files):
                    print("Generating file_" + str(i+1) + "...")
                    with open("/samba/enclave/hash_generation/file_" + str(i+1) + ".txt", "w+") as out_file:
                        out_file.write(str(i+1))
                    sleep(self.delay)
            elif self.action == "VERIFY_HASH":
                for i in range(0,self.num_of_files):
                    print("Generating file_" + str(i+1) + "...")
                    with open("/samba/enclave/verify_hash/request_hash/file_" + str(i+1) + ".txt", "w+") as out_file:
                        out_file.write(str(i+1))
                    sleep(self.delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Generate x number of files for testing.") 

    # Add the arguments
    parser.add_argument('--process',
                        metavar="HASH_GEN or VERIFY_HASH",
                        type=str,
                        required=True,
                        help='process to take: can be either HASH_GEN or VERIFY_HASH')

    parser.add_argument('--numOfFiles',
                        metavar="NUM_OF_FILES",
                        type=int,
                        required=True,
                        help='number of files to generate')

    parser.add_argument('--delay',
                        metavar="TIME_IN_SECONDS",
                        type=float,
                        help='delay in generating one file, in seconds')

    # Execute the parse_args() method
    args = parser.parse_args()

    input_action = args.process
    input_num_files = args.numOfFiles
    input_delay = args.delay

    # Call generate_files
    generate_files_obj = GenerateFiles(input_action, input_num_files, input_delay)
    generate_files_obj.generate_files()