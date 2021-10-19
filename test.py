import argparse
import os
import sys
from time import sleep

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

if input_delay is None:
    print("Generating files with no delay...")
    if input_action == "HASH_GEN":
        for i in range(1,input_num_files):
            print("Generating file_" + str(i) + "...")
            with open("/samba/enclave/hash_generation/file_" + str(i) + ".txt", "w+") as out_file:
                out_file.write(str(i))
    elif input_action == "VERIFY_HASH":
        for i in range(1,input_num_files):
            print("Generating file_" + str(i) + "...")
            with open("/samba/enclave/verify_hash/request_hash/file_" + str(i) + ".txt", "w+") as out_file:
                out_file.write(str(i))
else:
    print("Generating files with " + str(input_delay) + "s delay...")
    if input_action == "HASH_GEN":
        for i in range(1,input_num_files):
            print("Generating file_" + str(i) + "...")
            with open("/samba/enclave/hash_generation/file_" + str(i) + ".txt", "w+") as out_file:
                out_file.write(str(i))
        sleep(input_delay)
    elif input_action == "VERIFY_HASH":
        for i in range(1,input_num_files):
            print("Generating file_" + str(i) + "...")
            with open("/samba/enclave/verify_hash/request_hash/file_" + str(i) + ".txt", "w+") as out_file:
                out_file.write(str(i))
        sleep(input_delay)

# if sys.argv[1] == "sleep":
#     for i in range(1,51):
#         print("Generating file_" + str(i) + "...")
#         with open("/samba/enclave/verify_hash/request_hash/file_" + str(i) + ".txt", "w+") as out_file:
#             out_file.write(str(i))
#         sleep(0.5)
# elif sys.argv[1] == "nosleep":
#     for i in range(1,51):
#         print("Generating file_" + str(i) + "...")
#         with open("/samba/enclave/verify_hash/request_hash/file_" + str(i) + ".txt", "w+") as out_file:
#             out_file.write(str(i))