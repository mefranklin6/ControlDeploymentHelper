# ControlDeploymentHelper
FOSS 3rd Party tool to help Extron Authorized Programmers deploy systems using Control Script.
Not in any way affilated with Extron Corporation!

The tool simply takes the IP addresses of your already deployed Extron equipment and creates the Project Descriptor JSON for you.
If you only have one processor and one or two TLP's, this script will likely fill in all fields for you.
If your system is more complex than the above, this will at least get your started and keep manual entry to a minimum.


# Reason:
Reduction in manual work when deploying new ECS systems or upgrading systems from GCP.

# v1.0b 31 July 2023: Beta
- Base functionalitly is feature complete

# v1.1b 21 August 2023: Refactor
- OOP refactor to make it easier to support more devices.  I'll keep this version at 1 Processor and 2 TLP's for simplicity.

# Instructions:
Assuming you are deploying new systems or upgrading existing rooms:
1. Get your Extron devices on the network and get their IP's (get your computer on the same network too)
2. Edit the 'user variables' in this .py file to fit your enviroment
3. Create a default or generic project descriptor JSON file AND MAKE SURE IT IS NOT IN YOUR PROJECT DIRECTORY ROOT (also make sure you set the path in the user variables).  One is provided in the repo if you need it.
5. Run this .py on your PC.  This is not a file meant to be ran by the control processor.

# Common Errors
No part number found?  Make sure your device and part number are present in the dictionary in User Variables.

# End Goal / Big Picture
This can be combined with additional tools for an almost one-click automated deployment as long as you have good documentation of what devices and IP's are in your systems.  My workflow includes internal tools that I wrote that are extremely specific to my org's enviroment and likely little use here, but the overview is:

- Internal tool to parse a device database that includes device IP, location and loosely what model and type the devices are
- Internal tool that matches devices per location to their IP's and matches devices in the database to supported devices in the ECS main.py
- Internal tool that writes a config.json file with device information that the main processor program looks at
- This tool to bootstrap the main processor and TLP(s) config, with the IP's filled in by the previous tool
- CSDU where you have to manually enter device credentials, certify, and deploy 
- Internal tool that loads the config.json onto the processor and re-initializes so it has the (usually mostly) correct config
- Manual confirmation of the system operation and fine-tuning in the room.  Overall, about 80% of the work is automated!


Pull requests welcome.  Integration into CSDU also welcome!
