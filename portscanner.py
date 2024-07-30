import socket
import sys
import threading
from datetime import datetime

def portscanner(remoteServer, start_port, end_port):
    try:
        for port in range(start_port, end_port + 1):
            
            #socket.socket() takes 2 args AddressFamily(AF) and SocketType.
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET is used for IPv4 addresses. socket.SOCK_STREAM is used for TCP.
            #use socket.AF_INET6 for IPv6 addresses. use socket.SOCK_DGRAM for UDP.
            
            result = sock.connect_ex((remoteServer, port))
            
            if result == 0:  #if connection is successful, connect_ex returns 0. Else a non-zero error code is returned which can be used to determine the cause of error.
                try:
                    service_name = socket.getservbyport(port)
                except:
                    service_name = "Unknown"
                print("Port {}: Open - Service: {}".format(port, service_name))
                
            sock.close()
            
    except KeyboardInterrupt:
        print("You stopped the program execution using Keyboard.")
        sys.exit()
        
    except socket.gaierror:
        print("Host could not be resolved.")
        sys.exit()

    except socket.error:
        print("Could not connect to server.")
        sys.exit()
        
remoteServer = input("Enter a remote host to scan:")

start_port = int(input("Enter the starting port: "))
end_port = int(input("Enter the ending port: "))

print ("Starting to Scan ", remoteServer)
print()

#date and time of when the scan starts
t1=datetime.now()

# Number of threads for concurrent scanning
num_threads = 10


total_ports = end_port - start_port + 1

# Calculate the number of ports per thread
ports_per_thread = total_ports // num_threads

# Any ports left to be scanned
extra_ports = total_ports % num_threads

threads = []

current_start_port = start_port

for i in range(num_threads):
    current_end_port = current_start_port + ports_per_thread - 1
    if i < extra_ports:
        current_end_port += 1
    thread = threading.Thread(target=portscanner, args=(remoteServer, current_start_port, current_end_port))
    thread.start()
    threads.append(thread)
    current_start_port = current_end_port + 1

for thread in threads:
    thread.join()

t2 = datetime.now()

total= t2-t1

print()
print("Scanning completed in: ", total)
