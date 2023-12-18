# Eugene Science Center Piano Setup
---

**PC:**  Raspberry Pi 4

**OS:**  'Raspian' 32-bit Linux OS code name 'Buster'.

This is a legacy OS and not the most recent.  Do not install the updated OS, code name 'bullseye' until this has been tested.

**Sound Card**  M-Audio Fast Track.  Attach to an available USB connector

**Programming Language:  Python 3.7.**  Note that later versions of Raspian use Python 3.9, but system is not yet tested.

An Internet connection (WiFi) is required to complete the setup procedure

After the OS is installed, perform the following Steps:
### Step 1:  Install Python Libraries.
Install the following python libraries (an internet connection is required):  
-   matplotlib (will also install matplotlib)
-   sounddevice

You can do this in Thonny (Tools-->Manage Packages)
It can take several minutes, especially when installing matplotlib. Thonny comes pre-installed with Raspian.

To install matplotlib:

    >sudo apt-get update  
    >sudo pip3 install matplotlib
To install SoundDevice:

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
Copy and paste the following text into the newly created *ESC_Piano.desktop* file.  Save the file.

    [Desktop Entry]
    Type=Application
    Name=ESC_Piano autostart
    Comment=Path=/home/pi/ESC-RPi
    Comment= Dual screen display for piano microphones
    Exec = lxterminal -e 'cd /home/pi/ESC-RPi && sleep 1 && /usr/bin/python3 ESC_Piano.py'
>**Note:**  have to add bash sleep command else it won't work

Make the file executable.

    >chmod +x ESC_Piano.desktop

### Step 4.  Install Software

Create a directory */home/pi/ESC_RPi*  
Place ESC_Piano.py in the that directory.  
With luck, reboot and it should work.

---
## Optional:  Setting Up the Focusrite 2i2

**Experimental.**  Should be used with later version of Linux (e.g. Bullseye).

**Enable**

The driver is disabled by default and needs to be enabled at module load time with the device_setup=1 option to insmod/modprobe. Create a file /etc/modprobe.d/scarlett.conf containing the appropriate line for your device:

 
    2i2: options snd_usb_audio vid=0x1235 pid=0x8210 device_setup=1
    

**Check**

To see if the driver is present and enabled: 

    >dmesg | grep -i Scarlett -A 5 -B 5 

Scarlett should display information like:

    New USB device found, idVendor=1235, idProduct=8215, bcdDevice= 6.0b
    Product: Scarlett 18i20 USB
    Focusrite Scarlett Gen 2/3 Mixer Driver enabled pid=0x8215

**Use**

Run alsamixer -cUSB and you should see lots of controls. Use F3, F4, arrows keys, space bar, and "M" to display the controls, move around, and change values. To understand what the controls do, you will need to study the ASCII-art diagram at the top of the mixer_scarlett_gen2.c source code and the mixer driver feature list. You'll probably also need to study the Focusrite manual for your interface as well. Good luck!

Reference:  https://github.com/geoffreybennett/scarlett-gen2/releases/tag/v5.14