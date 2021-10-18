for i in range(1,11):
    print("Generating file_" + str(i) + "...")
    with open("/samba/enclave/verify_hash/request_hash/file_" + str(i) + ".txt", "w+") as out_file:
        out_file.write(str(i))