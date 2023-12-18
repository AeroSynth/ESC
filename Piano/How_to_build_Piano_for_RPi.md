# Eugene Science Center Piano Setup
---

**PC:**  Raspberry Pi 4

**OS:**  'Raspian' 32-bit Linux OS code name 'Buster'.

This is a legacy OS and not the most recent.  Do not install the updated OS, code name 'bullseye' until this has been tested.

**Sound Card**  M-Audio Fast Track.  Attach to an available USB connector

**Programming Language:  Python 3.7.**  Note that later versions of Raspian use Python 3.9, but system was not tested.

An Internet connection (WiFi) is required to complete the setup procedure

After the OS is installed, perform the following Steps:
### Step 1:  Install Python Libraries.
Install the python libraries (an internet connection is required):

 1. matplotlib (will also install matplotlib)
 2. sounddevice

You can do this in Thonny (Tools-->Manage Packages)
It can take several minutes, especially when installing numpy. Thonny comes pre-installed with Raspian.

To install matplotlib.

    >sudo apt-get update  
    >sudo pip3 install matplotlib
To install SoundDevice.

    >sudo pip3 install sounddevice

### Step 2: Install the RAMDISK

This is needed to reduce the amount of logging writes to the SD card, which is not reliable.

Go to the pi home directory:

    >cd /home/pi

Clone the log2ram git repository:

    >git clone https://github.com/azlux/log2ram.git

Change directory to the downloaded repository folder:

    >cd log2ram

Make the installation script executable:

    >chmod +x install.sh

Install it:

    >sudo ./install.sh
Change the log size value to 128M (as of Jan 2023, this is already done for you):

    >sudo nano /etc/log2ram.conf

Save the file (CTRL-X, yes, ENTER), then reboot:

    >sudo reboot
To check if it is working, use

    >df -h

This should show the new disk

In addition to this, check with

    >mount

This should show our mount point:

    >log2ram on /var/log type tmpfs (rw,nosuid,nodev,noexec,relatime,size=131072k,mode=755)
The log is written once a day.  To see this, look at install.sh for the cron entries.


### Step 3:  Set up to automatically run the application on boot.
Create a '.desktop' File

You do not need root-level access to modify your profile's (user's) autostart and .desktop files. In fact, it is recommended that you do not use sudo, as you may affect the permissions of the file (e.g. the file would be owned by root) and make them unable to be executed by autostart (which has user-level permissions).

Open a terminal, and execute the following commands to create an autostart directory (if one does not already exist) and edit a .desktop file:

    >mkdir /home/pi/.config/autostart
    >nano /home/pi/.config/autostart/ESC_Piano.desktop
Note that the autostart directory may already exist.  
You can use the file manager and text editor as well if you don't like using the command line editor, 'nano'.
Copy and paste the following text into the newly created *ESC_Piano.desktop* file.

    [Desktop Entry]
    Type=Application
    Name=ESC_Piano autostart
    Comment=Path=/home/pi/ESC-RPi
    Comment= Dual screen display for piano microphones
    Exec = lxterminal -e 'cd /home/pi/ESC-RPi && /usr/bin/python3 ESC_Piano.py'
Make the file executable.

    >chmod +x ESC_Piano.desktop

### Step 4.  Install Software

Create a directory */home/pi/ESC_RPi*  
Place ESC_Piano.py in the that directory.  
With luck, reboot and it should work.
