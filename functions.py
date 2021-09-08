import psutil
import string
import subprocess
import os
import sys


def get_NSSTART():
    try:
    	cmd = "(cd ~/Docker/Call-Of-Duty/Normal-Server/ ; ./cod4.sh)"
    	os.system(cmd)
    	return(True)
    except Exception as e:
    	return(False)
    	
def get_NSSTATUS():
	found = False
	cmd = "screen -ls"
	result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	value = result.stdout.read()
	resArray = value.splitlines()
	for x in range(1,(len(resArray)-1)):
		screen = resArray[x].split()
		finalscreen = screen[0]
		finalscreen = finalscreen[5:len(finalscreen)].decode("utf-8")
		if finalscreen == "Cod4Normal":
			found = True
	if found == True:
		return(True)
	else: 
		return(False)

	


def get_CPU():
    frequency = psutil.cpu_freq()
    percent = psutil.cpu_percent(interval=None)
    combined = 'Current CPU Readings: \nLoad: {0}% \nClock: {1.current}MHz'.format(
        percent, frequency)
    return(combined)


def get_RAM():
    total = int(round((psutil.virtual_memory().total)/1024/1024/1024))
    free = round(((psutil.virtual_memory().available)/1024/1024/1024), 2)
    inuse = round(((psutil.virtual_memory().used)/1024/1024/1024), 2)
    combined = "Current Memory Readings: \nTotal Memory: {0}GB\nCurrently In Use: {1}GB\nFree Memory : {2}GB".format(
        total, inuse, free)
    return(combined)


def get_DISK(path):
    total = int((psutil.disk_usage(path).total)/1024/1024/1024)
    free = int((psutil.disk_usage(path).free)/1024/1024/1024)
    used = int((psutil.disk_usage(path).used)/1024/1024/1024)
    combined = "{3} Drive Readings: \nTotal Capacity: {0}GB\nCurrently In Use: {1}GB\nFree Space : {2}GB".format(
        total, used, free, path)
    return(combined)

def get_LinDISK(path):
    cmd = "df / -h"
    result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    value = result.stdout.read().decode("utf-8")
    dskArray = value.splitlines()
    for x in range(1,(len(dskArray))):
        dskItems = dskArray[x].split()
        diskvalue = dskItems[0].split('/')[2]
        if path == diskvalue:
            combined = "{4} Drive Readings: \nTotal Capacity: {0}GB\nCurrently In Use: {1}GB\nFree Space: {2}GB\nPercentage : {3}%".format(
        dskItems[1][0:(len(dskItems[1])-1)], dskItems[2][0:(len(dskItems[2])-1)], dskItems[3][0:(len(dskItems[3])-1)], dskItems[4][0:(len(dskItems[4])-1)],path)
    return(combined)

        
     

def get_Drives():
    disks = []
    drives = []
    disks = psutil.disk_partitions(all=False)
    for d in disks:
        if(d.fstype=="NTFS"):
            drives.append(d.device[0:2])    
    return(drives)

def get_LinDrives():
    diskPaths = []
    cmd = "df / -h"
    result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    value = result.stdout.read().decode("utf-8")
    dskArray = value.splitlines()
    for x in range(1,(len(dskArray))):
        dskItems = dskArray[x].split()
        diskPath = dskItems[0].split('/')[2]
        diskPaths.append(diskPath)
    return(diskPaths)   


def get_NETWORKIO():
    return(psutil.net_io_counters())


def get_NETWORKCONNECTIONS():
    return(psutil.net_connections())
