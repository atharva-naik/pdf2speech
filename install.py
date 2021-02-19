# run this script to install everything
import os
import distro
import platform 
from colors import color
from interface import BANNER

print(color(BANNER, fg='red', style='bold'))
print(color("setting up pdf2speech", fg='blue', style='bold'))

# map package panagers to distros and get system dependencies
PACKAGE_MANAGER_MAP = {'Ubuntu':'apt', 'Debian':'apt', '':''}
SYSTEM_DEPS = [i.strip() for i in open("system.deps", "r").read().strip('\n').split('\n')]

# if you are on a Linux distro
if platform.system() == 'Linux':
    distro = distro.linux_distribution()[0]
    pkg_man = PACKAGE_MANAGER_MAP.get(distro)
    
    if pkg_man:
        os.system(f'sudo {pkg_man} update')
        for dep in SYSTEM_DEPS:
            os.system(f'sudo {pkg_man} install {dep}')

# if you are on MacOS or Windows
elif platform.system() in ['Darwin', 'Windows']:
    # install homebrew
    BREW_INSTALLED = os.system("brew help")
    if not(BREW_INSTALLED):
        if platform.system() == 'Darwin':
            os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
        else: 
            os.system('mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew')

    for dep in SYSTEM_DEPS:
        os.system(f"brew install {dep}")

# if you are on some other platform
else:
    print(color("sorry your OS is not supported! :(", fg='red', style='bold'))

# install python dependencies
os.system('pip install -r requirements.txt')