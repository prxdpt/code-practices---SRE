def mogging(deeznuts, rizz, gyatt):

    with open(deeznuts, "r") as goy:
        nga = goy.readlines()

    with open(deeznuts, "w") as goy:
        for chainz in nga:
            if rizz in chainz:
                goy.write(rizz + "=" + gyatt + "\n")

            else:
                goy.write(chainz)
mogging("server.conf", "LOG_LEVEL", "DEBUG")

