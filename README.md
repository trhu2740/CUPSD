# CUPSD

Code for the Senior Design Team 4 partnering with CU Physics. Automated insulation wrapping machine.

# Raspberry Pi Setup

For your initial setup of your raspberry pi, plug it in and connect a USB keyboard/mouse. Connect the raspberry pi to your local WI-FI or ad-hoc network that you will use to control the Pi. Once connected, you will no longer need a monitor, keyboard, or mouse for the Pi.

Once the Pi is connected to your local network, you can SSH into your Pi to control it from your computer. The following terminal commands can be used on your Mac:

```
cd /Applications/Utilities/
ssh kwiat-test:@raspberrypi.local
(you will be prompted to enter your password here)
```

For windows, you can use any SSH client (such as PuTTy, or the command prompt).

# Usage

The entire goal of this code is to make the machine automated. Many files in CUPSD are used for testing or were used for aid in development.

The only files you will need to make modifications to are in /src.

The src directory holds the primary file for running the machine, called:

```
main.py
```

You can run this file by using:

```
python3 main.py
```

Main operates by using threads, to run control the drive motor, magentic brakes, and read data from the follower arms simultaneously. Most importantly, these are threads and NOT processes. This means that although these operations are never truly running concurrently, they context switch thousands of times per second. Due to time constraints, multiprocessing was never tested and I am unsure of the Pi's capability for multiprocessing.

Inside of main.py you can change any constants for the drive motor or tensioning operations.

I highly reccommend taking a look at Tensioning.py and MotorPID.py to understand how they work. I imagine these will be the primary two files you will want to modify when making modifications to this machine.

For grabbing/sending specific values to specific hardware, please see the test directory. This directory holds some files for moving the linear actuator, reading encoder position and RPM, sweeping hardwarePWM and softwarePWM values, getting fake tension values, etc.

For more understanding of threads and running software-only tests, see the threads directory.

# Installation

The CUPSD source code is designed to work only on a Raspberry Pi (model 3B+). This source code will not compile on Arduino.

Clone the directory to your designated folder using one of the following (Https, SSH, CLI). Please refer to git documentation for any troubles cloning the repository:

```
git clone https://github.com/trhu2740/CUPSD.git
git clone git@github.com:trhu2740/CUPSD.git
gh repo clone trhu2740/CUPSD
```

Trying to run any source code immediately after setting up your Pi may not work. To ensure your Pi is setup correctly, please use the following steps from your Pi terminal:

```
sudo apt update
sudo apt full-upgrade
sudo raspi-config
(When the menu opens, navigate to "Interfacing Options" and enable SPi)
```

The source code may use python libraries that don't come natively installed on your Raspberry Pi. Using the traditional "pip install [library]" may throw errors. The most common error I have seen is:

```
error: externally-managed-environment
```

To get around this, I reccommend using the following command to install any additional packages, where xyz is your desired package. Note the 'sudo' command at the beginning:

```
sudo apt install python3-xyz
```

The most important package to install is pigpio (pronounced Pi-GPIO). This library manages all of our hardware PWM channels to control the drivetrain motor and linear actuator. To install this package, use the above command but replace xyz with pigpio.

```
sudo apt install python3-pigpio
```

# Setup Tips

Prior to running any code, ensure you are able to actually output PWM signals from the raspberry pi. To start pigpio, you need to start a daemon. To start a daemon:

```
sudo pigpiod
```

After executing this command, a daemon should be started and PWM signals should work when you begin running code. Note, you will have to restart a daemon whenever the Pi is power cycled or shut off.

To see the status of the Pi's GPIO pins, execute the following command:

```
raspi-gpio get
```

Each GPIO can be configured to one of eight different modes. The modes are: Input, Output, ALT0, ALT1, ALT2, ALT3, ALT4, and ALT5. You may not ever have to set the mode of a GPIO pin - however, if you are experiencing unexpected behavior from a GPIO pin, check the mode as a last resort. Example to change the pin mode:

```
pigs m 4 r # Input (read)
pigs m 4 w # Output (write)
pigs m 4 0 # ALT 0
pigs m 4 5 # ALT 5
```

Editing files from the terminal can be done in primarily one of two ways, and it comes down to your preference. To edit a file, you can use nano or vim. Nano and vim keyboard shortcuts can be found online. Examples to edit a file:

```
nano yourfile.py
vi yourfile.py
```

To shutdown the Pi safely, halt the system:

```
sudo halt
```

Wait for the green LED on the Pi to stop blinking. After which, you can safely disconnect the power without any possible memory corruption.

To remotely copy files from the pi to your machine, use the scp command (note: IP address may change):

```
scp kwiat-test@10.201.5.94:/home/kwiat-test/Desktop/fisherman.jpg /Users/troyhusted/Desktop/
```

To get the IP address of the PI, ssh with local and use the following command:

```
hostname -I
```

Note, you can reserve an IP for the raspberry pi in your router or request the DHCP to reserve one. Otherwise, it is not gauranteed that the Pi will have the same IP address whenever it reboots.

change

change
