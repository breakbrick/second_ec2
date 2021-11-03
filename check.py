def check_hash_is_written(hash_values):
    with open("hash/hashes.txt", "r") as read_hashes:
        # Check if the file_name obtained is inside the hash file
        line = next((l for l in read_hashes if hash_values[65:] in l), None)
        if line is None:
            print(hash_values[65:] + " is missing!")
        else:
            print(hash_values[65:] + " is written!")