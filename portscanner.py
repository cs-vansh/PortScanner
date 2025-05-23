import socket
import sys
import threading
from datetime import datetime

import ipaddress # used for IP validation

#Top 8344 ports
from top_ports import TopN_Ports
progress_count = 0;
open_ports = []

progress_lock = threading.Lock()  # Lock for printing progress 


def tcp_scan_for_range(host, start_port,end_port, total_ports):
    global progress_count

    for port in range(start_port, end_port + 1):
        sock = None # helps in finally block for checking sock
        try:
            #socket.socket() takes 2 args AddressFamily(AF) and SocketType.
            #socket.AF_INET is used for IPv4 addresses. socket.SOCK_STREAM is used for TCP.
            #use socket.AF_INET6 for IPv6 addresses. use socket.SOCK_DGRAM for UDP.
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(Timeout_value)  # Set timeout so it doesn't hang
            result = sock.connect_ex((host, port))
            if result == 0: #if connection is successful, connect_ex returns 0. Else a non-zero error code is returned which can be used to determine the cause of error.
                try:
                    service_name = socket.getservbyport(port, 'tcp')
                except :
                    service_name = "Unknown"
                open_ports.append(f"TCP Port {port}: OPEN - Service: {service_name}")
            
        except socket.gaierror:
            print("Host could not be resolved.")
            sys.exit()

        except socket.error:
            print("Could not connect to server.")
            sys.exit()
            
        except Exception as e:
            print(f"Error scanning TCP port {port}: {e}")
            
        finally:
            if sock:
                sock.close()
            with progress_lock:
                progress_count += 1
                percent = (progress_count / total_ports) * 100
                print(f"{percent:.1f}% done", end='\r')         

def tcp_scan_top_n(host, start_index,end_index,total_ports):
    global progress_count
    
    for port in TopN_Ports[start_index:end_index+1]:
        sock=None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(Timeout_value)  # Set timeout so it doesn't hang
            result = sock.connect_ex((host, port))
            if result == 0:
                try:
                    service_name = socket.getservbyport(port, 'tcp')
                except:
                    service_name = "Unknown"
                
                open_ports.append(f"TCP Port {port}: OPEN - Service: {service_name}")
            
        except socket.gaierror:
            print("Host could not be resolved.Exiting...")
            sys.exit()

        except socket.error:
            print("Could not connect to server.Exiting...")
            sys.exit()
            
        except Exception as e:
            print(f"Error scanning TCP port {port}: {e}")
        
        finally:
            if sock:
                sock.close()

            with progress_lock:
                progress_count += 1
                percent = (progress_count / total_ports) * 100
                print(f"{percent:.1f}% done", end='\r')
            
"""            
def udp_scan_for_range(host, start_port, end_port):

    print(f"\nStarting UDP Scan on {host} from port {start_port} to {end_port}...\n")
    for port in range(start_port, end_port + 1):
        sock=None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(Timeout_value)  # Short timeout for UDP

            # Send empty UDP packet
            # b'' is empty byte string, b formatting used for byte strings
            sock.sendto(b'', (host, port))

            try:
                # _ is for ignoring the senders address (ip and port) which we already have
                data, _ = sock.recvfrom(1024)  # Try to receive a response, max of 1024 bytes
                try:
                    service_name = socket.getservbyport(port, 'udp')
                except:
                    service_name = "Unknown"
                
                print(f"UDP Port {port}: OPEN (received data) - Service:{service_name}")
            except socket.timeout:
                print(f"UDP Port {port}: OPEN|FILTERED (no response)")
            except Exception as e:
                print(f"UDP Port {port}: CLOSED or FILTERED (error: {e})")
            
        except socket.gaierror:
            print("Host could not be resolved.Exiting...")
            sys.exit()

        except socket.error:
            print("Could not connect to server.Exiting...")
            sys.exit()
            
        except Exception as e:
            print(f"Error scanning UDP port {port}: {e}")
        
        finally:
            if sock:
                sock.close()

def udp_scan_top_n(host, start_port, end_port):  

    print(f"\nStarting UDP Scan on {host} for {n} topmost ports...\n")

    for port in TopN_Ports[start_port:end_port+1]:
        sock=None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(Timeout_value)  # Short timeout for UDP

            # Send empty UDP packet
            # b'' is empty byte string, b formatting used for byte strings
            sock.sendto(b'', (host, port))

            try:
                # _ is for ignoring the senders address (ip and port) which we already have
                data, _ = sock.recvfrom(1024)  # Try to receive a response, max of 1024 bytes
                try:
                    service_name = socket.getservbyport(port, 'udp')
                except:
                    service_name = "Unknown"
                
                print(f"UDP Port {port}: OPEN (received data) - Service:{service_name}")
            except socket.timeout:
                print(f"UDP Port {port}: OPEN|FILTERED (no response)")
            except Exception as e:
                print(f"UDP Port {port}: CLOSED or FILTERED (error: {e})")
            
        except socket.gaierror:
            print("Host could not be resolved.Exiting...")
            sys.exit()

        except socket.error:
            print("Could not connect to server.Exiting...")
            sys.exit()
            
        except Exception as e:
            print(f"Error scanning UDP port {port}: {e}")
        
        finally:
            if sock:
                sock.close()
"""
            
def protocol_menu():
    return 'TCP'
"""
    while True:
        print("\nChoose an option: \n")
        print("1. Scan TCP ports\n")
        print("2. Scan UDP ports\n")
        
        protocol_choice = int(input("Enter your choice: "))
        if(protocol_choice != 1 and protocol_choice != 2):
            print("Invalid choice. Try again.")
        elif(protocol_choice == 1):
            return 'TCP'
        elif(protocol_choice == 2):
            return 'UDP'
"""
    
def ports_menu():
    while True:
        print("\nChoose an option: \n")
        print("1. Do you want to specify a port range? \n")
        print("2. Do you want to scan most common n number of ports(Max: 8344)?")
        
        try:
            ports_choice = int(input("Enter your choice: "))
            
            if ports_choice != 1 and ports_choice != 2:
                print("Invalid choice. Try again.")

            elif ports_choice == 1:
                while True:    
                    start_port = int(input("Enter the starting port: "))
                    end_port = int(input("Enter the ending port: "))
                    if 0 <= start_port <= 65535 and 0 <= end_port <= 65535 and start_port <= end_port:
                            return [start_port, end_port]
                    else:
                        print("Invalid port range. Please enter values between 0 and 65535.")
                        
            elif ports_choice==2:
                while True:
                    try:
                        n = int(input("Enter the number of ports you want to scan: "))
                        if 1<= n <= 8344:
                            return n
                        else:
                            print("Enter a value between 1 and 8344. Try again.")
                    except:
                        print("Invalid input. Please enter numeric value.")
            else:
                print("Invalid choice. Try again.")
        
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            
def time_variable():
    global Timeout_value
    print('Port scanning is about maintaing the balance between time and accuracy. \n')
    print('You can set a timeout value for each port scan. \n')
    print('The timeout value can be set between 1 and 5. \n1 being fastest and least accurate.\n5 being slowest and most accurate. \n')
    
    while True:
        try:
            user_input = input("Enter the timeout value in seconds (between 1 and 5). Press Enter to use default value of 2: ")
            if user_input.strip()=="":
                Timeout_value = 2
                print("No input provided. Default timeout value set to 2 second.")
                break
            
            Timeout_value=int(user_input)
            if 1 <= Timeout_value <= 5:
                break  # Exit the loop if the value is valid
            else:
                print("Invalid input. Please enter a value between 1 and 5.")
                
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            
def number_of_threads():
    while True:
        try:
            user_input = input("Enter the number of threads you want to use (Press Enter to use default value of 10): ")
            if user_input.strip() == "":
                print("No input provided. Default number of threads set to 10.")
                return 10
            else:
                threads = int(user_input)
                if threads > 0:
                    return threads
                else:
                    print("Invalid input. Number of threads must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
def get_host():
    while True:
        try:
            remote_host = input("Enter a remote host IP address (IPv4) to scan: ")
            ip = ipaddress.ip_address(remote_host)
            if isinstance(ip, ipaddress.IPv4Address):  
                return remote_host
            else:
                print("The entered IP address is not an IPv4 address. Please enter a valid IPv4 address.")
        except ValueError:
            print("Not a valid IP address. Please enter a valid IPv4 address.")
            
def main():
    
    try:
        host = get_host()

        protocol_choice = protocol_menu()
        
        #ports_choice will be an array in case of port range 
        # it will be single value in case of top n ports scanning
        ports_choice = ports_menu()
        
        global Timeout_value
        
        #set Timeout_value's value
        time_variable()
        
        global thread_count
        thread_count = number_of_threads()
        
        start_time = datetime.now()

        # most common n ports
        if type(ports_choice) == int:
            
            # handling threading
            total_ports = ports_choice  
            ports_per_thread = total_ports // thread_count  
            extra_ports = total_ports % thread_count  
            
            threads = []
            current_start_index = 0 
            
            if protocol_choice == 'TCP':
                for i in range(thread_count):
                    current_end_index = current_start_index + ports_per_thread - 1
                    if i < extra_ports:
                        current_end_index += 1
                    
                    # Incase threads > ports to be scanned
                    if current_start_index > current_end_index:
                        continue  

                    thread = threading.Thread(
                        target=tcp_scan_top_n,
                        args=(host, current_start_index, current_end_index,total_ports)
                    )
                    thread.start()
                    threads.append(thread)
                    current_start_index = current_end_index + 1
            """
            elif protocol_choice == 'UDP':
                for i in range(thread_count):
                    current_end_index = current_start_index + ports_per_thread - 1
                    if i < extra_ports:
                        current_end_index += 1
                    thread = threading.Thread(
                        target=udp_scan_top_n,
                        args=(host, current_start_index, current_end_index)
                    )
                    thread.start()
                    threads.append(thread)
                    current_start_index = current_end_index + 1     
            """

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

        # port_range
        elif type(ports_choice) == list:
            
            # handling threading
            total_ports = ports_choice[1] - ports_choice[0] + 1
            
            # Calculate the number of ports per thread
            ports_per_thread = total_ports // thread_count
            # Any ports left to be scanned
            extra_ports = total_ports % thread_count
            threads = []
            current_start_port = ports_choice[0]

            if protocol_choice == 'TCP':
                for i in range(thread_count):
                    current_end_port = current_start_port + ports_per_thread - 1
                    if i < extra_ports:
                        current_end_port += 1
                        
                    # Incase threads > ports to be scanned
                    if current_start_port > current_end_port:
                        continue  

                    thread = threading.Thread(target=tcp_scan_for_range, args=(host, current_start_port, current_end_port,total_ports))
                    thread.start()
                    threads.append(thread)
                    current_start_port = current_end_port + 1
            """
            elif protocol_choice == 'UDP':
                for i in range(thread_count):
                    current_end_port = current_start_port + ports_per_thread - 1
                    if i < extra_ports:
                        current_end_port += 1
                    thread = threading.Thread(target=udp_scan_for_range, args=(host, current_start_port, current_end_port))
                    thread.start()
                    threads.append(thread)
                    current_start_port = current_end_port + 1
            """
            #for all threads to complete before moving ahead
            for thread in threads:
                thread.join()
        
        print()
        for entry in open_ports:
            print(entry)
                                    
        end_time = datetime.now()
        total_time = end_time - start_time
        print(f"\nScan completed in {total_time}")
        print()
        
    except KeyboardInterrupt:
        print("You stopped the program execution using Keyboard.Exiting...")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()
    
