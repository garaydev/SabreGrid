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
__version__ = "0.01341"

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
    import operator
    from collections import OrderedDict
    from os.path import join
    import shutil
    import psutil
    import usb
    import pymongo
    import bottle
    import SGFileEntity
    from pymongo import MongoClient
except ImportError:
    # check if required dependencies have been installed
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)

def install_and_import(package):
    """Attempt to import and install packages using importlib functionality"""
    if not check_module_exists(package):
        try:
            importlib.import_module(package)
        except ImportError:
            pip.main(['install', package])
        finally:
            globals()[package] = importlib.import_module(package)
        
def check_module_exists(name):
    """Import package installation function"""
    pkg_loader = importlib.find_loader(name)
    found = pkg_loader is not None
    return found 

def GetFilesBySize(dirChk):
    """Return size of files by size based on getsize() byte size"""
    getallFiles = []
    formFiles = []
    for (dirpath, dirs, files) in os.walk(dirChk):
      for f in files:
           fp = os.path.join(dirpath, f)
           getallFiles.append([f, os.path.getsize(fp), itemCreatedTime(fp)])
    if(getallFiles is not None):
      sortedFiles = sorted(getallFiles, key=operator.itemgetter(1),reverse=True)
      for index,fi in enumerate(sortedFiles,start=1):
          fSize = fi[1]
          fName = fi[0]
          fTime = fi[2]
          formatedSize = best_unit_size(fSize)
          formFiles.append([index,fName,formatedSize,fTime])
    if(formFiles is not None and len(formFiles) > 0):
        return formFiles

def MonitorCheckDirSize(dirChk,msgPrint=False,formatSize=False):
    """Return total size of dirs and sub-dirs"""
    totalSize = 0
    fileList = os.listdir(dirChk)
    if os.path.exists(dirChk):
            for dirpath, dirnames, filenames in os.walk(dirChk):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    totalSize += os.path.getsize(fp)
            if(formatSize):
                formatDirSize = best_unit_size(totalSize)
    else:
        print('ERROR: specified path "' + dirChk + '" does not exist......')
        return totalSize

    if(msgPrint):
        return 'Size of the "' + str(dirChk) + '" dir is ' + str(formatDirSize) + '.'
    if(formatSize):
        return formatDirSize
    else:
        return totalSize


def best_unit_size(bytes_size):
    """Format a total size of getsize() Metric prefix"""
    if(str(bytes_size).isnumeric):
       oneUnitRnd = 1024
       metrics = [('KB',1), ('MB',2), ('GB',3),('TB',4), ('PB',5)]
       for met in metrics:
           bytes_size /= oneUnitRnd
           if bytes_size < oneUnitRnd:
                return '{0} {1}'.format(round(bytes_size,1), met[0])
    else:
         return '0 KB'

def itemAccessedTime(dir):
    """Last time a directory/file was accessed"""
    if os.path.exists(dir):
        AccessedTime = time.ctime(os.path.getatime(dir))
        return AccessedTime
    else:
        return 0

def itemModifiedTime(dir):
    """Last time a directory/file was modified/changed"""
    if os.path.exists(dir):
        modTime = time.ctime(os.path.getmtime(dir))
        return modTime
    else:
        return 0

def itemCreatedTime(dir):
    """Non-unix time when directory/file was created"""
    if os.path.exists(dir):
        createTime = time.ctime(os.path.getctime(dir))
        return createTime
    else:
        return 0


def number_of_files(dir):
    """Number of files found in directory"""
    if not os.path.exists(dir):
        num_of_files = len(glob("*"))
        print('LOG: A total of ' + num_of_files + ' exists in dir ' + dir )
    else:
        print('ERROR: Error finding dir/file')

def GetSpecificFileTotals(dirChk,fileType='.mp3',msgPrint=False):
    """Get mp3 file total"""
    count = 0
    prntMsg = msgPrint 
    typeLocator = str.lower(fileType)
    for (dirname, dirs, files) in os.walk(dirChk):
       for filename in files:
          if filename.endswith(typeLocator) :
               count = count + 1
    if(prntMsg):
        return '"'+ str.upper(typeLocator) +'" Files: ' + str(count)
    else:
        return str(count)

def FormatTime(sendTime):
    """Formatt Time to standard SG format."""
    formattedTime = time.strptime(sendTime,'%Y-%m-%d %I:%M.%S')
    return formattedTime

def fileLogMessages(fpath,msg,cOutMsg=False,cOutMsgDate=False):
    """Write to Log File"""
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

def moveFileToDest(moveFile,checkDir,tempDropDir):
    """ Moves a file to it's designated location."""
    try:
        fileCheck_Name = moveFile[1]
        fileCheck_Size = moveFile[2]
        parentPath = os.path.join(os.getcwd(), checkDir)
        if(os.path.isdir(parentPath)):
            fpath = os.path.join(parentPath, fileCheck_Name)
            if(os.path.isfile(fpath)):
                if(os.path.isdir(tempDropDir)):
                    dest = os.path.join(tempDropDir,fileCheck_Name)
                    if not os.path.exists(dest):
                        shutil.move(fpath, dest)
                        return True
    except e:
        return false

def insertSGFilesDoc(sgFileObj):
    try:
        connection = pymongo.MongoClient("mongodb://localhost")

        db = connection.SGFiles
        sgFilesColl = db.SGFiles 

        doc = {'FileEntityName':sgFileObj.FileName,'FileEntitySizeFormmated':sgFileObj.FileSize,'FileEntityCreatedTime':sgFileObj.FileCreatedDate}
        item = sgFilesColl.find_one()
        return True
    except Exception as e:
        print(('SGFile insert failed! Hard!'), e)
        return False

def fillSGFilesEntity(fName,fSizeFormated,fTime):
    sgF = SGFileEntity(SGFileEntity,fName,fSizeFormated,fTime)
    if sgF is not None:
        return sgF
    else:
        return None

def SabreGridIntro():
    """Print the welcome message"""
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

##Schedule

##
## Single .py file, break out into modules later
##

if __name__ == '__main__':
    SabreGridIntro()

# initilize prefix variables
msgLog = 'LOG: '
msgError = 'ERROR: '
mgsTrace = 'TRACE: '
checkFileType = '.mp3'

# initilize sched obj
s = sched.scheduler(time.time, time.sleep)

# initilize module dependency names
print(msgLog + 'initializing dependencies.....')
dependencies = ['twisted','datetime','sched', 'time','psutil','pymongo','bottle']



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
sgDefaultLogDirName = 'SG_Log'
sgLogFilePrefix = 'sgDailyLog'
sgCheckDir = 'SG_Videos'
# initilize log path variable, to be set later
sgLogPath = ''
sgTempDropDir = 'Q:\Industry_Works\SabreTest'
sgDefaultCheckDir = 'SG_Videos'
sgMinDiskSpace = 40.0
sgCheckDirLimit =  20973617.0

# dir checks and creates
if not os.path.exists(sgDefaultLogDirName):
    print(msgLog + sgDefaultLogDirName + ' dir does not exist. Creating "' + sgDefaultLogDirName + '" under ' + curDir + ' .....')
    os.makedirs(sgDefaultLogDirName)
else:
    print(msgLog + sgDefaultLogDirName + ' dir already exists. Continue dir setup.....')

## Setup Log directory date file
if os.path.exists(sgDefaultLogDirName):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    sgdayLogFileName = sgDefaultLogDirName + '/' + sgLogFilePrefix + '_' + str(nowDate) +'.txt'
    if not os.path.isfile(sgdayLogFileName):
        print(msgLog + 'A log file with a name of "' + sgdayLogFileName + '" does not exist. Creating now.....Created!')
        sgLogPath = sgdayLogFileName
        logFile = open(sgLogPath, mode='at', encoding='utf-8')
        logFile.close()
    else:
        print(msgLog + 'A log file with a name of "' + sgdayLogFileName + '" already exists. Appending to this log file....')
        sgLogPath = sgdayLogFileName
        logFile = open(sgLogPath, mode='at', encoding='utf-8')
        logFile.close()
        
if sgCheckDir is not None and (len(sgCheckDir) > 0 and sgCheckDir.isspace() is False):
    print(msgLog + 'Check directory defined. Defined as: "' + sgCheckDir + '"......')
else:
    print(msgLog + 'No valid Check directory specified....')
    print(msgLog + 'Using default check directory "' + sgDefaultCheckDir + '" instead.....')
    sgCheckDir = sgDefaultCheckDir

if not os.path.exists(sgCheckDir):
    print(msgLog + '"' + sgCheckDir + '" dir does not exist. Creating "' + sgCheckDir + '" under ' + curDir + ' .....')
    os.makedirs(sgCheckDir)
else:
    print(msgLog + '"' + sgCheckDir + '" dir already exists. Continue.....')

##setup twisted task(s)

fileLogMessages(sgLogPath,GetSpecificFileTotals(sgCheckDir,checkFileType,True),True,True)
fileLogMessages(sgLogPath,MonitorCheckDirSize(sgCheckDir,True,True),True,True)

fileLogMessages(sgLogPath,GetSpecificFileTotals(sgCheckDir,checkFileType,True),True,True)
fileLogMessages(sgLogPath,MonitorCheckDirSize(sgCheckDir,True,True),True,True)

tempDropAbsPath = os.path.abspath(sgTempDropDir)
tempDropDriveDic = os.path.splitdrive(tempDropAbsPath)
dropDri = tempDropDriveDic[0]
dropDrivePath = os.path.join(dropDri,'/') 
dropDiskUsage = psutil.disk_usage(dropDrivePath)
diskUsagePercent = dropDiskUsage.percent
dskParts = psutil.disk_partitions()
dskPartList = []
for parts in dskParts:
    dskPartList.append([parts.device,parts.fstype,parts.opts])

#base call for file transfer
currentCheckDirSize = 0
currentCheckDirSize = MonitorCheckDirSize(sgCheckDir,False,False)
listOfFiles = GetFilesBySize(sgCheckDir)

dirLimitFormatted = best_unit_size(sgCheckDirLimit)

print(msgLog + ' Checking if monitor directory is greater than ' + str(dirLimitFormatted) + '.')

while currentCheckDirSize > sgCheckDirLimit :
    if(diskUsagePercent >= sgMinDiskSpace):
        dirLimitForm = best_unit_size(sgCheckDirLimit)
        dirMontiorForm = best_unit_size(currentCheckDirSize)
        print(msgLog + ' Monitor Dir is ' + str(dirMontiorForm) + ' in size, which is greater than the set quota of ' + str(dirLimitForm) + '...Moving files to Drop Dir.')
        if(listOfFiles is not None):
            fileObj = listOfFiles[0]
            sgFileObj = fillSGFilesEntity(fileObj[1],fileObj[2],fileObj[3])
            insertedDoc = insertSGFilesDoc(sgFileObj)
            movedCheck = moveFileToDest(fileObj,sgCheckDir,sgTempDropDir)
            if(movedCheck):
                fileLogMessages(sgLogPath,'Moved ' + str(fileObj[1]) + ' of size ' + str(fileObj[2]) + ' to dir: ' + str(sgTempDropDir) + '.',True,True)
    else:
        print('Cannot move any files to that disk. The quota has been met.')
    currentCheckDirSize = 0
    currentCheckDirSize = MonitorCheckDirSize(sgCheckDir,False,False)
    listOfFiles = GetFilesBySize(sgCheckDir)

##mongob implementation required




#reactor.callLater(3.5, f, fileLogMessages(sgLogPath,MonitorCheckDirSize(sgCheckDir),True,True))
#reactor.run()
