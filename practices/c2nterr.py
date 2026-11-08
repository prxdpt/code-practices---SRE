import re 
from collections import defaultdict


def goon(rizz):

    mew = re.compile(


        r'^(\S+) '                      # IP address
        r'\S+ \S+ '                     # identd, userid
        r'\[[^\]]+\] '                  # timestamp
        r'"[^"]*" '                     # request line
        r'(\d{3}) '

    )

    ip_address_error = defaultdict(int)
    status_code_error = defaultdict(int)

    total_errors = 0
    total_lines = 0




    with open(rizz, 'r') as nga:
        for john in nga:
            total_lines +=1


            match = mew.match(john)
            if not match:
                continue

            ip_address = match.group(1)
            status_code = match.group(2)

            if status_code.startswith('4') or status_code.startswith('5'):
                status_code_error[status_code] += 1
                ip_address_error[ip_address] += 1
                total_errors += 1



    skibidi = sorted(status_code_error.items(), key = lambda x: x[1], reverse = True)
    tralala  = sorted(ip_address_error.items(), key = lambda x: x[1], reverse = True)


    return {"status_error": skibidi, "ip_error": tralala}

x = goon("server.log")

print(x)
            