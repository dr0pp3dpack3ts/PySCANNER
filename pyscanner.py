import pyfiglet
import socket
import os
import sys
import subprocess
import threading
import time
from datetime import datetime
from queue import Queue

subprocess.call('clear', shell=True)

ascii_banner = pyfiglet.figlet_format("PySCANNER")
print(ascii_banner)

# .45 took 159 seconds (and missed a port)
# .25 took 87 seconds
# .15 took 54 seconds
socket.setdefaulttimeout(0.55)
 
# lock thread during print so we get cleaner outputs
print_lock = threading.Lock()

discovered_ports = []
 
# notify user
target = input('Target: ')
 
# convert to ip, if they give us a name
# this requires that it actually resolves
t_IP = socket.gethostbyname(target)
print ('Scanning Host for Open Ports: ', t_IP)
 
 
# define our port scan process
def portscan(port):
 
   # create socket object
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   # try to connect
   try:
      # create/open connection
      conx = s.connect((t_IP, port))
      
      # don't let thread contention screw up printing
      with print_lock:
         print("port {} is open".format(port))
         discovered_ports.append(str(port))
      
      # close out that connection
      conx.close()
   except:
      pass
 
# threader thread pulls worker from queue and processes
def threader():
   while True:
      # gets worker from queue
      worker = q.get()
      # run job with savailable worker in queue (thread)
      portscan(worker)
 
      # complete with the job, shut down thread?
      q.task_done()
 
# create queue and threader      
q = Queue()
 
# start time
startTime = time.time()
 
# 100 threads took 172 seconds
# 200 threads took 87 seconds   
for x in range(200):
   # thread id
   t = threading.Thread(target = threader)
   
   # classifying as a daemon, so they will die when the main dies
   t.daemon = True
   
   # begins, must come after daemon definition
   t.start()
 
# this is the range or variable passed to the worker pool   
for worker in range(1, 65535):
   q.put(worker)
 
# wait until thrad terminates   
q.join()
 
 
# ok, give us a final time report
runtime = float("%0.2f" % (time.time() - startTime))
print("Run Time: ", runtime, "seconds")


print("nmap -p{ports} -sVC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target))
nmap = "nmap -p{ports} -sVC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)

def automate():
       choice = '0'
       while choice =='0':
          print("Run nmap? y or n.")
          print("-" * 60)
          choice = input("Option Selection: ")
          if choice == "y":
             try:
                print(nmap)
                os.mkdir(target)
                os.chdir(target)
                os.system(nmap)
                #convert = "xsltproc "+target+".xml -o "+target+".html"
                #os.system(convert)
                t3 = datetime.now()
                print("-" * 60)
                print("Press enter to quit...")
                input()
             except FileExistsError as e:
                print(e)
                exit()
          elif choice == "n":
             sys.exit()
             automate()
automate()
