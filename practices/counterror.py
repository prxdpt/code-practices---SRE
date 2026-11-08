import re
from collections import defaultdict

def analyze_error_logs(log_file_path):
    """
    Analyze Nginx/Apache access logs for 4xx and 5xx errors.
    Returns top 5 IP addresses generating the most errors.
    """
    
    # Regex patterns for common log formats
    # Nginx/Apache Combined Log Format: IP - - [timestamp] "method path protocol" status size "referer" "user-agent"
    # Pattern captures: IP and status code
    log_pattern = re.compile(
        r'^(\S+) '                      # IP address
        r'\S+ \S+ '                     # identd, userid
        r'\[[^\]]+\] '                  # timestamp
        r'"[^"]*" '                     # request line
        r'(\d{3}) '                     # status code
    )
    
    error_count_by_status = defaultdict(int)
    error_count_by_ip = defaultdict(int)
    total_errors = 0
    total_lines = 0
    
    print(f"Reading log file: {log_file_path}")
    
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total_lines += 1
            
            match = log_pattern.match(line)
            if not match:
                continue
            
            ip_address = match.group(1)
            status_code = match.group(2)
            
            # Check for 4xx or 5xx errors
            if status_code.startswith('4') or status_code.startswith('5'):
                error_count_by_status[status_code] += 1
                error_count_by_ip[ip_address] += 1
                total_errors += 1
    
    print(f"\nProcessed {total_lines} log entries")
    print(f"Found {total_errors} error entries (4xx/5xx)\n")
    

    print("ERROR COUNT BY STATUS CODE")

    sorted_statuses = sorted(error_count_by_status.items(), 
                            key=lambda x: x[1], 
                            reverse=True)
    
    for status, count in sorted_statuses:
        percentage = (count / total_errors * 100) if total_errors > 0 else 0
        print(f"Status {status}: {count:>8} errors ({percentage:>5.2f}%)")
    
    # Display top 5 IP addresses
    print("\n" + "=" * 60)
    print("TOP 5 IP ADDRESSES GENERATING ERRORS")
    print("=" * 60)
    
    top_ips = sorted(error_count_by_ip.items(), 
                    key=lambda x: x[1], 
                    reverse=True)[:5]
    
    for rank, (ip, count) in enumerate(top_ips, 1):
        percentage = (count / total_errors * 100) if total_errors > 0 else 0
        print(f"{rank}. {ip:<15} {count:>8} errors ({percentage:>5.2f}%)")
    
    return {
        'total_lines': total_lines,
        'total_errors': total_errors,
        'error_by_status': dict(sorted_statuses),
        'top_ips': top_ips
    }


# Usage
if __name__ == "__main__":
    
    log_file = "access.log"
    
    try:
        results = analyze_error_logs(log_file)
    except FileNotFoundError:
        print(f"Error: File '{log_file}' not found")
    except Exception as e:
        print(f"Error processing log file: {e}")