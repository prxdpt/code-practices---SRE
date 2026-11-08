import re 
from collections import defaultdict


def resolve(file):

    patt = re.compile(

        r'^(\S+) '                      # IP address
        r'\S+ \S+ '                     # identd, userid
        r'\[[^\]]+\] '                  # timestamp
        r'"[^"]*" '                     # request line
        r'(\d{3}) '

    )

    ip_error = defaultdict(int)
    status_error = defaultdict(int)
    error = 0 
    lines = 0


    with open(file, 'r') as f:
        for line in f:
            lines += 1


            match = patt.match(line)
            if not match:
                continue

            ip_address = match.group(1)
            status_code = match.group(2)

            if status_code.startswith('4') or status_code.startswith('5'):
                status_error[status_code] += 1 
                ip_error[ip_address] += 1
                error +=1


    sort1 = sorted(status_error.items(), key =lambda x: x[1], reverse=True)
    sort2 = sorted(ip_error.items(),  key =lambda x: x[1], reverse=True)

    return {"a": sort1, "b": sort2, "c":error}
x = resolve("server.log")

print(x)