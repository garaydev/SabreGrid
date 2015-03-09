#==============================================================================
#
#   SABREGRID - Control your Security Grid
#
#       Module 1.0 - Used to monitor defined directories
#       
#
#==============================================================================
__author__ = "@garaydev"
__license__ = "The MIT License (MIT)"
__date__ = "03/07/2015"
__version__ = "0.01337"

# global imports
try:
    import importlib
    import pip
    import sys
    import os
    import sched
    import time
    import twisted
    import glob
    import twisted.internet
    import datetime
    import sched
except ImportError:
    # check if required dependencies have been installed
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)

### import package installation function
def install_and_import(package):
    if not check_module_exists(package):
        try:
            importlib.import_module(package)
        except ImportError:
            pip.main(['install', package])
        finally:
            globals()[package] = importlib.import_module(package)

### import package installation function
def check_module_exists(name):
    pkg_loader = importlib.find_loader(name)
    found = pkg_loader is not None
    return found 

#montior size of specified checkdir
def MonitorCheckDirSize(dirChk):
    if os.path.exists(dirChk):
        currentChkDirSize = os.path.getsize(dirChk)
        #formatDirSize = best_unit_size(currentChkDirSize)
        return 'Size of ' + str(dirChk) + ' is ' + str(currentChkDirSize) + '.'
    else:
        print('ERROR: specified path "' + dirChk + '" does not exist......')
    pass

##format a total size of getsize() Metric prefix
def best_unit_size(bytes_size):
    for exp in range(0, 90, 10):
        bu_size = abs(bytes_size) / pow(2.0, exp)

        if int(bu_size) < 2 ** 10:
            unit = {0: "bytes", 10: "KiB", 20: "MiB", 30: "GiB", 40: "TiB",
                50: "PiB", 60: "EiB", 70: "ZiB", 80: "YiB"}[exp]
        break
    return {"s": bu_size, "u": unit, "b": bytes_size}

##last time a directory/file was accessed
def last_access(dir):
    if not os.path.exists(dir):
        lastA = ctime(os.path.getatime(dir))
        print('LOG: ' + dir + ' was last modified at ' + lastA )
    else:
        print('ERROR: Error finding dir/file')

##last time a directory/file was changed
def last_change(dir):
    if not os.path.exists(dir):
        lastC = ctime(os.path.getmtime(dir))
        print('LOG: ' + dir + ' was last modified at ' + lastC )
    else:
        print('ERROR: Error finding dir/file')

##Number of files found in directory
def number_of_files(dir):
    if not os.path.exists(dir):
        num_of_files = len(glob("*"))
        print('LOG: A total of ' + num_of_files + ' exists in dir ' + dir )
    else:
        print('ERROR: Error finding dir/file')

##
## Single .py file, break out into modules later
##

##print SabreLogo
print('\n')
print('________________________________________________________________')
print('  _____         ____  _____  ______ _____ _____  _____ _____ ' )
print(' / ____|  /\   |  _ \|  __ \|  ____/ ____|  __ \|_   _|  __ \ ')
print('| (___   /  \  | |_) | |__) | |__ | |  __| |__) | | | | |  | |')
print(' \___ \ / /\ \ |  _ <|  _  /|  __|| | |_ |  _  /  | | | |  | |')
print(' ____) / ____ \| |_) | | \ \| |___| |__| | | \ \ _| |_| |__| |')
print('|_____/_/    \_\____/|_|  \_\______\_____|_|  \_\_____|_____/ ')
print('\n')
print('\t\t CONTROL YOUR SECURITY GRID')
print('________________________________________________________________')
print('\n')

# initilize prefix variables
msgLog = 'LOG: '
msgError = 'ERROR: '
mgsTrace = 'TRACE: '

# initilize module dependency names
print(msgLog + 'initializing dependencies.....')
dependencies = ['twisted','datetime','sched', 'time']

# dependency checking
depenTotal = len(dependencies)
print(msgLog + 'total defined dependencies: ' + str(depenTotal))

print(msgLog + 'traverse ' + str(depenTotal) + ' dependencie(s) to be installed and imported.....')
for d in range(len(dependencies)):
    install_and_import(dependencies[d])

## print all packages installed
print(msgLog+ 'lisiting installed packages.....')
inst_pckgs = pip.get_installed_distributions()
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
     for i in inst_pckgs])
for ip in installed_packages_list:
        print('\t' + str(ip))

##location display
print(msgLog+ 'displaying working locations.....')
print('\t - Working Dir: ' + os.getcwd())
print('\t - Script Dir: ' + os.path.dirname(os.path.abspath(__file__)))
curDir = os.path.basename(os.path.normpath(os.getcwd()))
print('\t - Current Dir: ' + curDir)

##initilize paths
sgLogDirName = 'SG_Log'
sgLogFilePrefix = 'sgDailyLog'
sgCheckDir = '1a'
sgDefaultCheckDir = 'SG_Videos'

# dir checks and creates
if not os.path.exists(sgLogDirName):
    print(msgLog + sgLogDirName + ' dir does not exist.Creating' + sgLogDirName + ' under ' + curDir + ' .....')
    os.makedirs(sgLogDirName)
else:
    print(msgLog + sgLogDirName + ' dir already exists. Continue dir setup.....')

## Setup Log directory date file
if os.path.exists(sgLogDirName):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    sgdayLogFileName = sgLogDirName + '/' + sgLogFilePrefix + '_' + str(nowDate) +'.txt'
    if not os.path.isfile(sgdayLogFileName):
        logFile = open(sgdayLogFileName, 'a')
        logFile.close()
    else:
        print(msgLog + 'A log file with a name of "' + sgdayLogFileName + '" already exists. Appending to this log file....')

if sgCheckDir is not None and (len(sgCheckDir) > 0 and sgCheckDir.isalnum() and sgCheckDir.isspace() is False):
    print(msgLog + 'Check directory defined. Defined as: "' + sgCheckDir + '"......')
else:
    print(msgLog + 'No valid Check directory specified....')
    print(msgLog + 'Using default check directory "' + sgDefaultCheckDir + '" instead.....')
    sgCheckDir = sgDefaultCheckDir

if not os.path.exists(sgCheckDir):
    print(msgLog + '"' + sgCheckDir + '" dir does not exist.Creating ' + sgCheckDir + ' under ' + curDir + ' .....')
    os.makedirs(sgCheckDir)
else:
    print(msgLog + '"' + sgCheckDir + '" dir already exists. Continue.....')

##setup twisted task(s)
MonitorCheckDirSize(sgCheckDir)

if os.path.isfile(sgdayLogFileName):
    with open(sgdayLogFileName, 'a') as logFileWrite:
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        logFileWrite.write( mgsTrace  + ' ' + nowDate + ' : ' + MonitorCheckDirSize(sgCheckDir) + '\n')
        logFileWrite.close()

#reactor.callLater(3.5, f, MonitorCheckDirSize)
#reactor.run()