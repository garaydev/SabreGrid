# global imports
import importlib
import pip
import sys
import os

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

# initilize module dependency names
print(msgLog + 'initializing dependencies.....')
dependencies = ['twisted']

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

# create directory log