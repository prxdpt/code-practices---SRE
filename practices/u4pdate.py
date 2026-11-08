def mew(file_path, key, value):
    
    with open(file_path, "r") as f:
        lines = f.readlines()
        
    with open(file_path, "w") as f:

        for i in lines:
            if key in i:
                f.write(key + "=" + value + "\n")

            else:
                f.write(i)

mew("server.conf", "LEVEL", "DEBUG")