import sys
from time import sleep


if sys.argv[1] == "sleep":
    for i in range(1,51):
        print("Generating file_" + str(i) + "...")
        with open("/samba/enclave/verify_hash/request_hash/file_" + str(i) + ".txt", "w+") as out_file:
            out_file.write(str(i))
        sleep(0.5)
elif sys.argv[1] == "nosleep":
    for i in range(1,51):
        print("Generating file_" + str(i) + "...")
        with open("/samba/enclave/verify_hash/request_hash/file_" + str(i) + ".txt", "w+") as out_file:
            out_file.write(str(i))