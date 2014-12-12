import os
import zipfile
import glob
import datetime
import telnetlib
import time

print("Starting backup...")
hosts = ["192.168.1.1"]
user = "UserName"
passw = "PassWord"
loc = "/mnt/backup"
date = str(datetime.date.today())
hosts_ok =0
count =0

print("Removing all old backup files")
for fl in glob.glob("/srv/tftp/*.cfg"):
    os.remove(fl)
print("Done.")
print("Backing up all given hosts")
for n in hosts:

    tn = telnetlib.Telnet(n)
    tn.read_until("Username: ")
    tn.write(user + "\r\n")
    tn.read_until("Password: ")
    tn.write(passw + "\r\n")
    tn.read_until("*",2)
    tn.write("backup startup-configuration to YOURTFTPSERVERHERE "+n+".cfg\r\n")
    read = tn.read_until("*",2)
    if read.__contains__("00009K"):
        hosts_ok=hosts_ok+1
    else:
        print "Error on host: "+n
    count=count+1
    print("Hosts complete: "+str(count)+"/"+str(len(hosts)))


print("Zipping up this stuff...")

target_dir = '/srv/tftp'
zip = zipfile.ZipFile(loc+"/"+date+'.zip', 'w', zipfile.ZIP_DEFLATED)
rootlen = len(target_dir) + 1
for base, dirs, files in os.walk(target_dir):
   for file in files:
      fn = os.path.join(base, file)
      zip.write(fn, fn[rootlen:])
print("Moving this zipfile to: "+loc)

print("Deleting zip files older than 10 days")

now = time.time()
cutoff = now - (7 * 86400)

files = os.listdir(loc)
for xfile in files:
        if os.path.isfile( loc + xfile ):
                t = os.stat( loc + xfile )
                c = t.st_ctime

                if c < cutoff:
                        os.remove(loc + xfile)

print("Done.")


print("Config backup completed: "+str(hosts_ok)+"/"+str(len(hosts))+" hosts ok.")