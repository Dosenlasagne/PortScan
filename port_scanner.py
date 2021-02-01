import socket
import subprocess
import sys
from datetime import datetime
import argparse
from requests import get
import json

class colors_:
	RESET  = '\033[0m'
	R  = '\033[31m'
	G  = '\033[32m'
	BOLD = '\033[1m'

class port_scanner:
	def __init__():
		common_ports = {
		"20":"FTP Data",
		"21":"FTP Control",
		"22":"SSH",
		"23":"Telnet",
		"25":"SMTP",
		"53":"DNS",
		"67":"DHCP",
		"68":"DHCP",
		"69":"TFTP",
		"80":"HTTP",
		"110":"POP3",
		"161":"SNMP",
		"443":"SSL",}
		
		return common_ports
		
	def get_datetime():
		# get current datetime
		date_time = datetime.now()
		return date_time
		
	def clear():
		# Clear the screen
		subprocess.call('clear', shell=True)
		
	# input
	def input_host(Server):
		# get Hosts IP address 
		ServerIP = socket.gethostbyname(Server)
		
		return ServerIP
				
	def scan(host, port_range, common):
		data = list()
		temp = list()
		times = list()
		
		# banner
		print("-" * 28)
		print(" Scanning: ", host)
		print("-" * 28 + "\n")
		
		# get start time
		start_time = port_scanner.get_datetime()
		
		# get port range
		ports = port_range.split("-")
		
		try:
			# start port scanning
			for port in range(int(ports[0]), int(ports[1]) + 1):
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				re = sock.connect_ex((host, port))
				
				temp = []
				# output
				if re == 0:
					if str(port) in common:
						print(colors_.BOLD + " [" + colors_.G + "+" + colors_.RESET + colors_.BOLD + "] " + colors_.RESET + "Port {}:\t".format(port)+ colors_.G + "Open" + colors_.RESET  + "\t{}\t".format(common[str(port)]))
					else:
						print(colors_.BOLD + " [" + colors_.G + "+" + colors_.RESET + colors_.BOLD + "] " + colors_.RESET + "Port {}:\t".format(port) + colors_.G + "Open" + colors_.RESET)
					temp.append(str(port))
					temp.append("open")
					data.append(temp)
				else:
					if str(port) in common:
						print(" [" + colors_.R + "-" + colors_.RESET + "] " + "Port {}:\t".format(port)+ colors_.R + "Closed" + colors_.RESET + "\t{}\t".format(common[str(port)]))
					else:
						print(" [" + colors_.R + "-" + colors_.RESET + "] " + "Port {}:\t".format(port) + colors_.R + "Closed" + colors_.RESET)
					
					temp.append(str(port))
					temp.append("closed")
					data.append(temp)
					
				# close socket
				sock.close()
				
		# check if user cancels		
		except KeyboardInterrupt:
			port_scanner.clear()
			print("\n")
			print(colors_.BOLD + " [" + colors_.R + "-" + colors_.RESET + colors_.BOLD + "] " + colors_.RESET + colors_.R + "You pressed Ctrl+C" + colors_.RESET + "\n")
			sys.exit()
		
		# checks gateway error
		except socket.gaierror:
			port_scanner.clear()
			print("\n")
			print(colors_.BOLD + " [" + colors_.R + "-" + colors_.RESET + colors_.BOLD + "] " + colors_.RESET + colors_.R + "Host could not be resolved" + colors_.RESET + "\n")
			sys.exit()
		
		# checks socket error
		except socket.error:
			port_scanner.clear()
			print("\n")
			print(colors_.BOLD + " [" + colors_.R + "-" + colors_.RESET + colors_.BOLD + "] " + colors_.RESET + colors_.R + "Couldnt connect to server" + colors.RESET + "\n")
			sys.exit()
			
		# get endtime
		end_time = port_scanner.get_datetime()
		
		# calculating passed time
		duration = end_time - start_time
		
		times.append(start_time)
		times.append(end_time)
		times.append(duration)
		
		# output
		print("\n" + colors_.BOLD + " [" + colors_.G + "+" + colors_.RESET + colors_.BOLD + "] " + colors_.RESET + colors_.G + "Scanning Completed in: " + colors_.RESET + str(duration) + " seconds" + "\n") 
		
		# returns time stemps and collected data
		return times, data
		
		

if __name__ == "__main__":
	# add input arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--host", help = "Host to scan")
	parser.add_argument("-p", "--ports", help = "Ports to scan")
	parser.add_argument("-o", "--output", help = "Data saved in file")
	args = parser.parse_args()
	
	# gets public ip over ipify api
	ip = get("https://api.ipify.org").text
		
	# requests ip information data from ip-api
	url = "http://ip-api.com/json/" + str(ip)
	request_ip = get(url)
	
	# loads requested data in json format
	data = json.loads(request_ip.content)
	
	port_scanner.clear()
	
	#printing the requested data
	print("[" + colors_.G + "+" + colors_.RESET + "] IP\t\t", data["query"])
	print("[" + colors_.G + "+" + colors_.RESET + "] CITY\t", data["city"])
	print("[" + colors_.G + "+" + colors_.RESET + "] ISP\t\t", data["isp"])
	print("[" + colors_.G + "+" + colors_.RESET + "] LOC\t\t", data["country"])
	print("[" + colors_.G + "+" + colors_.RESET + "] REG\t\t", data["regionName"])
	print("[" + colors_.G + "+" + colors_.RESET + "] TIME\t", data["timezone"])
	print("[" + colors_.G + "+" + colors_.RESET + "] ZIP\t\t", data["zip"])
	print("[" + colors_.G + "+" + colors_.RESET + "] LAT\t\t", data["lat"])
	print("[" + colors_.G + "+" + colors_.RESET + "] LON\t\t", data["lon"])
	print("\n")
	
	# get IP
	host = port_scanner.input_host(args.host)
	
	# load port_data
	c_p = port_scanner.__init__()	
		
	# port scanning
	temp = port_scanner.scan(host, args.ports, c_p)
	
	# saving stuff in variables
	data = temp[1]
	times = temp[0]
	
	# creating output
	if args.output != None:
		with open(args.output, "w") as out:
			# writing time stemp in file
			out.write("start time:\t" + str(times[0]) + "\n")
			out.write("end time:\t" + str(times[1]) + "\n")
			out.write("duration:\t" + str(times[2]) + "\n\n")
			
			# writing data in file
			for element in data:
				line = "\t".join(element)
				
				if element[0] in c_p:
					out.write("port: " + line + "\t" + c_p[element[0]] + "\n")
				else:
					out.write("port: " + line + "\n")		
		
	else:
		pass
	
	
	
	
	
	
	
	
