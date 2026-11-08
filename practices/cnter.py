import re
from collections import defaultdict


def analyse(file_path):

    pattern = re.compile(

        r'^(\S+) '                      # IP address
        r'\S+ \S+ '                     # identd, userid
        r'\[[^\]]+\] '                  # timestamp
        r'"[^"]*" '                     # request line
        r'(\d{3}) '
    )

    status_code_error = defaultdict(int)
    ip_address_error = defaultdict(int)
    errors = 0
    total_lines = 0


    with open(file_path, 'r') as f:
        for l in f:
            total_lines += 1

            match = pattern.match(l)
            if not match:
                continue

            ip_address = match.group(1)
            status_code = match.group(2)


            if status_code.startswith('4') or status_code.startswith('5'):
                status_code_error[status_code] += 1
                ip_address_error[ip_address] +=1
                errors += 1


    status_sort = sorted(status_code_error.items(),key = lambda x: x[1], reverse = True)
    ip_sort = sorted(ip_address_error.items(),key = lambda x: x[1], reverse = True)

    return {"status_errors": status_sort, "ip_errors": ip_sort}

x = analyse("server.log")

print(x)






    