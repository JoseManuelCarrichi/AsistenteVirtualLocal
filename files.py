def write_file(data, filename, filetype):
    with open("{}.{}".format(filename, filetype), "a") as file:
        file.write(data)