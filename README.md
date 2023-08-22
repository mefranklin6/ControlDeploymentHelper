# ControlDeploymentHelper
FOSS 3rd Party tool to help Extron Authorized Programmers deploy systems using Control Script.
Not in any way affilated with Extron Corporation!

The tool simply takes the IP addresses of your already deployed Extron equipment and creates the Project Descriptor JSON for you.
If you only have one processor and one or two TLP's, this script will likely fill in all fields for you.
If your system is more complex than the above, this will at least get your started and keep manual entry to a minimum.

# Reason:
I want to reduce the amount of manual work it takes to deploy or upgrade systems to the new Control Script with VS Code.  This is especially relevant when upgrading existing rooms from GCP to Control Script using a project file that accounts for hardware variations (like the one Relensky made for my org!)

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

Pull requests welcome.  Integration into CSDU also welcome!
