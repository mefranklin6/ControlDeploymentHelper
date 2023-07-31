import requests
import re
import json
from os import listdir


#### Created by Matthew Franklin ###
#### Please see www.github.com/mefranklin6 for license, readme, updates ###

# Execute this code on your computer, don't put it on the processor


###############################################################################
# Begin User Variables
###############################################################################

# Root directory of the project on your computer
# ex: 'C:/Users/<YOURUSER>/Documents/<PROJECTFOLDERNAME>'
ProjectRootDirectory = 'C:/Users/mefranklin/Documents/Github/VSCodeTemplate'

# Directory of your GUI Files.
# Make sure the model number of the TLP is in the file name ex: 'ClientName_525M.gdl'
# Make sure there's only one file per TLP model in the directory
GUI_File_Directory = 'C:/Users/mefranklin/Documents/Github/VSCodeTemplate/layout'

# Names your project descriptor file, processors, and TLP's
RoomName = 'TestRoom1' 

# Default project descriptor JSON file location
# !!!! IMPORTANT Do not have this in the root of your project file !!!!
Default_JSON_File_Location = 'C:/Users/mefranklin/Documents/Github/VSCodeTemplate/rfile/DEFAULT.json'

MainProcessor_IP = '192.168.253.250'
MainProcessor_AVLAN_IP = '' #placholder

First_TLP_IP = '192.168.253.8'
Second_TLP_IP = '' #placeholder


"""
 instead of this manual dictionary of {Model : PartNumber},
 it could also be possible to script a login to the admin web interface
 and grab the part number there (or login ssh/telnet)
 
 I wanted to keep web scraping and passwords to a mimimum,
 hence the hardcoded dictionary below """


ProcessorModels = {
                    'IPCP Pro 355MQ xi' : '60-1919-01',
                    'some other model' : '11-1111-11',
}

TLP_Models = {
                    'TLP Pro 525M' : '60-1561-02',
                    'some other tlp' : '22-2222-22',
}


# Models with both LAN and AVLAN
AVLAN_Processors = [ 
                    'IPCP Pro 255',
                    'IPCP Pro 350',
                    'IPCP Pro 355',
                    'IPCP Pro 360',
                    'IPCP Pro 555',
                    'IPCP Pro 255Q xi',
                    'IPCP Pro 350 xi',
                    'IPCP Pro 355MQ xi', #built in 1808
                    'IPCP Pro 355DRQ xi',
                    'IPCP Pro 555Q xi'
                    #TODO: confirm this is all models.  (Built-in ones are tricky)
]




###############################################################################
# End User Variables
###############################################################################



# Parent classes
class Processor:
    address = ''
    AVLAN_address = ''
    model_name = ''
    part_number = ''
    Has_AVLAN = bool

class TLP:
    address = ''
    model_name = ''
    part_number = ''
    layout_file = ''


# Subclasses
class MainProcessor(Processor):
    address = MainProcessor_IP

class First_TLP(TLP):
    address = First_TLP_IP




def ScrapeWebInterface(ip):
    HTTP = requests.get(f'https://{ip}/www/index.html', verify=False)
    return HTTP.text


def ExtractModelName(ip):
    HTTP = ScrapeWebInterface(ip)
    HTTPSearch = re.search(r'var device_name =(.*?);', HTTP)
    DeviceModel = HTTPSearch.group(1).strip().replace('"', '')
    return DeviceModel


def GetPartNumber(model_name):

    if model_name in ProcessorModels.keys():
        model_number = ProcessorModels[model_name]
        return model_number
    
    if model_name in TLP_Models.keys():
        model_number = TLP_Models[model_name]
        return model_number
    

def GUI_Selector(tlp_model_name):
    TLP_ModelNumberOnly = re.search(r'(\d{3,4})', tlp_model_name)
    GUI_Files = listdir(GUI_File_Directory)
    
    for GUI_File in GUI_Files:
        if TLP_ModelNumberOnly[1] in GUI_File:
            return GUI_File
	
    if len(GUI_Files) == 1:
        return GUI_Files[0]
		

def DecideProcessorNetworks (processor_model_name):
    for AVLAN_Processor in AVLAN_Processors:
        if processor_model_name in AVLAN_Processor:
            return True


# Function calls, load attributes into classes
MainProcessor.model_name = ExtractModelName(MainProcessor.address)
MainProcessor.part_number = GetPartNumber(MainProcessor.model_name)
MainProcessor.Has_AVLAN = DecideProcessorNetworks(MainProcessor.model_name)
if MainProcessor.Has_AVLAN == True:
    print('Processor has AVLAN') # placeholder

First_TLP.model_name = ExtractModelName(First_TLP.address)
First_TLP.part_number = GetPartNumber(First_TLP.model_name)
First_TLP.layout_file = GUI_Selector(First_TLP.model_name)


with open(Default_JSON_File_Location, 'r') as DefaultJSON_File:
    JSON_Data = json.load(DefaultJSON_File)


# Read
MainProcessorDeviceFields = JSON_Data['devices'][0]

#Set
MainProcessorDeviceFields['name'] = f'{RoomName} - MainProcessor'
MainProcessorDeviceFields['part_number'] = MainProcessor.part_number
# TODO: format MainProcessorNetworkFields based on if processor has AVLAN or just LAN


# Read
First_TLP_DeviceFields = JSON_Data['devices'][1]
First_TLP_NetworkFields = First_TLP_DeviceFields['network']['interfaces']

#Set
First_TLP_DeviceFields['name'] = f'{RoomName} - MainTLP'
First_TLP_DeviceFields['part_number'] = First_TLP.part_number
First_TLP_NetworkFields[0]['address'] = First_TLP.address
First_TLP_DeviceFields['ui']['layout_file'] = First_TLP.layout_file

#TODO: Processor LAN inc AVLAN if applicable


with open(f'{ProjectRootDirectory}/{RoomName}.json', 'w') as New_JSON_File:
    json.dump(JSON_Data, New_JSON_File)
