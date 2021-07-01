import psutil


def get_CPU():
    frequency = psutil.cpu_freq()
    percent = psutil.cpu_percent(interval=None)
    combined = 'Current CPU Readings: \nLoad: {0}% \nClock: {1.current}MHz'.format(
        percent, frequency)
    return(combined)


def get_RAM():
    total = int((psutil.virtual_memory().total)/1024/1024/1014)
    free = int((psutil.virtual_memory().available)/1024/1024/1014)
    inuse = int(total-free)
    combined = "Current Memory Readings: \nTotal Memory: {0}GB\nCurrently In Use: {1}GB\nFree Memory : {2}GB".format(
        total, inuse, free)
    return(combined)


def get_DISK(path):
    return(psutil.disk_usage(path))


def get_NETWORKIO():
    return(psutil.net_io_counters())


def get_NETWORKCONNECTIONS():
    return(psutil.net_connections())
