import time

def check_hash_is_written(hash_values, file_path_to_hash_values):
    with open("hash/hashes.txt", "r") as read_hashes:
        # Check if the file_name obtained is inside the hash file
        line = next((l for l in read_hashes if file_path_to_hash_values[0:-9] in l), None)
        if line is None:
            print(">>>>>>>>>>>>>>> " + file_path_to_hash_values[0:-9] + " is missing!")
            # # Read the file_path_to_hash_values
            # with open(file_path_to_hash_values, "r") as to_write_hash_value:
            #     missing_hash = to_write_hash_value.read()
            # # Write the missing hash values to file
            # with open("hash/hashes.txt", "a+") as write_hashes:
            #     write_hashes.write(missing_hash + "\n")
            # time.sleep(10)
            return False
        else:
            print(hash_values[65:] + " is written!")
            return True