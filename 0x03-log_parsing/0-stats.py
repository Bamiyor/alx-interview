#!/usr/bin/python3
import sys
import signal

# Initialize metrics
total_file_size = 0
status_codes_count = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
lines_processed = 0

def print_statistics():
    """Prints the collected statistics."""
    global total_file_size, status_codes_count
    print(f"File size: {total_file_size}")
    for code in sorted(status_codes_count.keys()):
        if status_codes_count[code] > 0:
            print(f"{code}: {status_codes_count[code]}")

def signal_handler(sig, frame):
    """Handles the keyboard interruption signal."""
    print_statistics()
    sys.exit(0)

# Set up the signal handler for keyboard interruption
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        parts = line.split()
        
        # Validate and parse the line
        if len(parts) == 9 and parts[2] == '"GET' and parts[3] == '/projects/260' and parts[4] == 'HTTP/1.1"':
            try:
                status_code = int(parts[5])
                file_size = int(parts[6])
                
                # Update metrics
                total_file_size += file_size
                if status_code in status_codes_count:
                    status_codes_count[status_code] += 1
                lines_processed += 1
                
                # Print statistics after every 10 lines
                if lines_processed % 10 == 0:
                    print_statistics()
            except ValueError:
                # Skip lines with invalid integers
                continue
except KeyboardInterrupt:
    # Handle keyboard interruption during line processing
    print_statistics()
    sys.exit(0)
