def update(file_path, key, value):

    with open(file_path,"r") as goy:
        pels = goy.readlines()

    with open(file_path, "w") as goy:
        for slop in pels:
            if key in slop:
                goy.write(key + "=" + value + "\n")

            else:
                goy.write(slop)


update("server.conf", "MAX_CONNECTIONS", "800")
