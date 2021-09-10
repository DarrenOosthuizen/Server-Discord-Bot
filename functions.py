import psutil
import string
import subprocess
import os
import sys

#region Darren WOL Functions
def get_WOLAWAKE():
    cmd = "ping -c 2 192.168.0.116"
    result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    value = result.stdout.read().decode("utf-8")

    lines = value.splitlines()
    result = lines[5].split(',')[1][1:2]
    if result == '2':
        return(True)
    else:
        return(False)

def get_WOL():
    result = get_WOLAWAKE()
    if result == True:
        return("Darren-PC is already on!")
    else:
        cmd = ("sudo /home/flysubuntuadmin/WOL.sh")
        os.system(cmd)
        return("Waking up Darren-PC ")
#endregion

#region Public Server Functions
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
        finalscreen = screen[0].decode("utf-8")
        finalscreen = finalscreen.split('.')[1]
        if finalscreen == "Cod4Normal":
            found = True
    if found == True:
        return(True)
    else:
        return(False)


def get_NSSTOP():
    try:
        cmd = "screen -X -S Cod4Normal quit"
        os.system(cmd)
        result = get_NSSTATUS()
        if result == True:
            return(False)
        else:
            return(True)
    except Exception as e:
    	return(False)	

#endregion

#region Promod Server Functions
def get_PMSTART():
    try:
    	cmd = "(cd ~/Docker/Call-Of-Duty/Mods-Server/ ; ./promod.sh)"
    	os.system(cmd)
    	return(True)
    except Exception as e:
    	return(False)
    	
def get_PMSTATUS():
    found = False
    cmd = "screen -ls"
    result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    value = result.stdout.read()
    resArray = value.splitlines()
    for x in range(1,(len(resArray)-1)):
        screen = resArray[x].split()
        finalscreen = screen[0].decode("utf-8")
        finalscreen = finalscreen.split('.')[1]
        if finalscreen == "Cod4Promod":
            found = True
    if found == True:
        return(True)
    else:
        return(False)


def get_PMSTOP():
    try:
        cmd = "screen -X -S Cod4Promod quit"
        os.system(cmd)
        result = get_PMSTATUS()
        if result == True:
            return(False)
        else:
            return(True)
    except Exception as e:
    	return(False)	
#endregion

#region Ubuntu Server Functions
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
    dataNetwork = psutil.net_io_counters()
    dataSent = float(round(((dataNetwork.bytes_sent )/1024/1024),2))
    dataRecv = float(round(((dataNetwork.bytes_recv )/1024/1024), 2))
    print(dataRecv)
    packetsSent = dataNetwork.packets_sent
    packetsRecv = dataNetwork.packets_recv
    dataErrIn = dataNetwork.errin
    dataErrOut = dataNetwork.errout
    dataDropIn = dataNetwork.dropin
    dataDropOut = dataNetwork.dropout
    Combined = "Network Stats: \nData Sent: {0}MB \nDate Recieved: {1}MB \nPackets Sent: {2} \nPackets Recieved: {3} \nData Errors In: {4} \nData Errors Out: {5} \nSending Packets Dropped: {6} \nRecieving Packets Dropped: {7}".format(dataSent,dataRecv,packetsSent,packetsRecv,dataErrIn,dataErrOut,dataDropIn,dataDropOut)
    print(Combined)
    return(Combined)


def get_NETWORKCONNECTIONS():
    return(psutil.net_connections())

#endregion