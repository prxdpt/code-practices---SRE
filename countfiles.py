import os

def list_files(path):
    try:
        files = os.listdir(path)
        return files, None
    except FileNotFoundError:
        return None, "File Not Found Error"

def main():
    paths = input("Give me paths by ,").split(",")

    for path in paths:
        files, error_message = list_files(path)

        if files:
            for file in files:
                print(file)

        else:
            print ({error_message})


if __name__ == "__main__":
    main()

# import os

# def list_files(path):
#     try:
#         files = os.listdir(path)
#         return files, None  # Return files and no error
#     except FileNotFoundError:
#         return None, "File Not Found Error"

# def main():
#     paths = input("Give me paths by ,").split(",")

#     for path in paths:
#         path = path.strip()  # Remove whitespace
#         files, error_message = list_files(path)

#         if files is not None:  # Check if we got files back
#             for file in files:
#                 print(file)
#         else:
#             print(error_message)  # No braces needed


# if __name__ == "__main__":
#     main()