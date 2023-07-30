# ControlDeploymentHelper
FOSS 3rd Party tool to help Extron Authorized Programmers deploy systems using Control Script.
Not in any way affilated with Extron Corporation!

# Reason:
I want to reduce the amount of manual work it takes to deploy or upgrade systems to the new Control Script with VS Code.  This is especially relevant when upgrading existing rooms from GCP to Control Script using a project file that accounts for hardware variations (like the one Relensky made for my org!)

# v0.1 28 July 2023:
Initial proof-of-concept work.  Only sets the part numbers for a single processor and single TLP, but it will be easy to expand the scope to most fields in the JSON Project Descriptor file.  Some of that may be personal taste, so modify this as you see fit, check back for updates, and submit pull requests!

# v0.2 30 July 2023:
Script now sets:
- Main Processor Name
- Main Processor Part#
- First TLP Name
- First TLP Part#
- First TLP IP Address
- First TLP .gdl GUI File

# Roadmap:
- Add support for multiple processors per room
- Add support for multiple TLP's per room
- Remove user variables from .py script and add it to a config file (I like YAML), or maybe a simple GUI
- Add processor IP address(es) (need to handle processors with just LAN vs those with LAN and AVLAN)
- Error and Exception handling
- Log information to CSV?
- Let me know if you would like to see anything additional!  

# Instructions:
Assuming you are deploying new systems or upgrading existing rooms:
1. Get your Extron devices on the network and get their IP's (get your computer on the same network too)
2. Edit the 'user variables' in this .py file to fit your enviroment
3. Create a default or generic project descriptor JSON file AND MAKE SURE IT IS NOT IN YOUR PROJECT DIRECTORY ROOT (also make sure you set the path in the user variables)
4. Run this .py on your PC.  This is not a file meant to be ran by the control processor.

Pull requests welcome.  Integration into CSDU also welcome!
