# PortScanner
A multi-threaded Port Scanner made using `socket` and `threading` modules. Gives a list of open ports along with the services running on them.

**NOTE:** The service identification is based on standard port numbers using `socket.getservbyport`. This may not reflect the actual service if a non-standard service is running on a given port.

## Usage
1. Run the script.
2. Enter the IPv4 address or hostname of the target system.

3. Choose between:
   - Scanning a custom range of ports, or
   - Scanning the top N most common ports (up to 8344).

4. The scan begins and outputs:
   - Open ports
   - Associated service names (based on port numbers)


## Future Scope:
 - Complete & optimize UDP scanning (initial commented code present) 
 - IPv6 support 
 - Exporting scan results (CSV,JSON)
 - More precise service detection