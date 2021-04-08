
# easy_mira_js
## Easy to create a MIRA Payload JS
This python script will be easy to covert the binary payload file to a simple payload javascript for PS4


* mira-project is here: https://github.com/OpenOrbis/mira-project/tree/port/755

>> Here I specify MIRA_PLATFORM as MIRA_PLATFORM_ORBIS_BSD_755, and run 'make' command to compile the kernel and loader projects

>> /kernel/build will generate a payload file which name is "Mira_Orbis_MIRA_PLATFORM_ORBIS_BSD_755.elf"

>> /loader/build will generate a payload file which name is "MiraLoader_Orbis_MIRA_PLATFORM_ORBIS_BSD_755.bin"



## Usage:
* 1.Put the two compiled payload files in the same directory as the python code
* 2.Make sure the python variable PLATFORM_VERSION which matched the MIRA_PLATFORM version number you compiled.
* 3.Run the Code
