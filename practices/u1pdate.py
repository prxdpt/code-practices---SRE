def update(file_path, key, value):

    with open(file_path, "r") as f:
        lines = f.readlines()

    with open(file_path, "w") as f:
        for l in lines:
            if key in l:
                f.write(key + "=" + value + "\n")
            else:
                f.write(l)


update("server.conf", "PORT", "9020") 