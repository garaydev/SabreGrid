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
__version__ = "0.01338"

# global imports
try:
    import importlib
    import pip
    import sys
    import os
    import sched
    import time
    import glob
    import datetime
    import sched
    import collections
    from collections import OrderedDict
    from os.path import join
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
    totalSize = 0
    fileList = os.listdir(dirChk)
    if os.path.exists(dirChk):
            for dirpath, dirnames, filenames in os.walk(dirChk):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    totalSize += os.path.getsize(fp)
            formatDirSize = best_unit_size(totalSize)
            return 'Size of the "' + str(dirChk) + '" dir is ' + str(formatDirSize) + '.'
    else:
        print('ERROR: specified path "' + dirChk + '" does not exist......')
        return totalSize
    pass

##format a total size of getsize() Metric prefix
def best_unit_size(bytes_size):
    oneUnitRnd = 1024
    metrics = { 'KB', 'MB', 'GB','TB', 'PB'}
    for met in metrics:
        bytes_size /= oneUnitRnd
        if bytes_size < oneUnitRnd:
            return '{0} {1}'.format(round(bytes_size,1), met)

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

##get mp4 file total
def GetSpecificFileTotals(dirChk,fileType='.mp3'):
    count = 0
    typeLocator = str.lower(fileType)
    for (dirname, dirs, files) in os.walk(dirChk):
       for filename in files:
           if filename.endswith(typeLocator) :
               count = count + 1
    return '"'+ str.upper(typeLocator) +'" Files: ' + str(count)

##Write to Log File
def fileLogMessages(fpath,msg,cOutMsg=False,cOutMsgDate=False):
    if fpath is not None and len(fpath) > 0 and os.path.isfile(fpath):
        if msg is not None and len(msg) > 0:
                with open(fpath, mode='at', encoding='utf-8') as logFileWrite:
                    msgLogFile = 'LOG: '
                    now = datetime.datetime.now()
                    nowDate = now.strftime('%Y-%m-%d %I:%M.%S')
                    logFileWrite.write( msgLogFile + nowDate + ' : ' + msg + '\n')

        if(cOutMsg and cOutMsgDate):
            print(msgLogFile + ' ' + nowDate + ' : ' + msg)
        elif(cOutMsg):
            print(msgLogFile + ' : ' + msg)
        else:
            print('ERROR: Invalid Message. Not logged!')
    else:
        print('ERROR: Invalid directory path. Not logged!')

##Schedule

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
checkFileType = '.mp3'

# initilize sched obj
s = sched.scheduler(time.time, time.sleep)

# initilize module dependency names
print(msgLog + 'initializing dependencies.....')
dependencies = ['twisted','datetime','sched', 'time']

# initilize log path variable, to be set later
sgLogPath = ''

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
sgCheckDir = 'SG_Videos'
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
        print(msgLog + 'A log file with a name of "' + sgdayLogFileName + '" does not exist. Creating now.....')
        logFile = open(sgdayLogFileName, mode='at', encoding='utf-8')
        logFile.close()
    else:
        sgLogPath = sgdayLogFileName
        logFile = open(sgLogPath, mode='at', encoding='utf-8')
        logFile.close()
        print(msgLog + 'A log file with a name of "' + sgdayLogFileName + '" already exists. Appending to this log file....')

if sgCheckDir is not None and (len(sgCheckDir) > 0 and sgCheckDir.isspace() is False):
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

fileLogMessages(sgLogPath,GetSpecificFileTotals(sgCheckDir,checkFileType),True,True)
fileLogMessages(sgLogPath,MonitorCheckDirSize(sgCheckDir),True,True)

fileLogMessages(sgLogPath,GetSpecificFileTotals(sgCheckDir,checkFileType),True,True)
fileLogMessages(sgLogPath,MonitorCheckDirSize(sgCheckDir),True,True)

#reactor.callLater(3.5, f, fileLogMessages(sgLogPath,MonitorCheckDirSize(sgCheckDir),True,True))
#reactor.run()
