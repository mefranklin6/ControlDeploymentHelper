import requests
import re
import json
from os import listdir
from random import randrange


#### Created by Matthew Franklin ###
#### Please see www.github.com/mefranklin6 for license, readme, updates ###

# Execute this code on your computer, don't put it on the processor


###############################################################################
# Begin User Variables
###############################################################################


#### Commonly Changed Variables ####

# Names your project descriptor file, processors, and TLP's
SystemName = 'TestRoom' 

MainProcessor_IP = '192.168.253.250'
MainProcessor_AVLAN_IP = '192.168.254.250'

First_TLP_IP = '192.168.253.8'
Second_TLP_IP = '' # Leave empty string if none

####################################


#### Setup Variables ####
# Root directory of the project on your computer
# ex: 'C:/Users/<YOURUSER>/Documents/<PROJECTFOLDERNAME>'
ProjectRootDirectory = 'C:/Users/mefranklin/Documents/Github/VSCodeTemplate'

# Directory of your GUI Files.
# Make sure the model number of the TLP is in the file name ex: 'ClientName_525M.gdl'
# Make sure there's only one file per TLP model in the directory
GUI_File_Directory = 'C:/Users/mefranklin/Documents/Github/VSCodeTemplate/layout'

# Default project descriptor JSON file location
# !!!! IMPORTANT Do not have this in the root of your project file !!!!
Default_JSON_File_Location = 'C:/Users/mefranklin/Documents/Github/VSCodeTemplate/rfile/DEFAULT.json'

#### Backend Variables ####

"""
 instead of this manual dictionary of {Model : PartNumber},
 it could also be possible to script a login to the admin web interface
 and grab the part number there (or login ssh/telnet)
 
 I wanted to keep web scraping and passwords to a mimimum,
 hence the hardcoded dictionary below """

ProcessorModels = {
                    'IPCP Pro 355MQ xi' : '60-1919-01',
                    'IPCP Pro 550' : '60-1418-01',
                    'IPCP Pro 550 xi' : '60-1913-01A',
                    'IPCP Pro 555Q xi' : '60-1917-01A',
                    'IPCP Pro 555' : '60-1434-01',
                    'IPL Pro S6' : '60-1414-01',
                    'IPCP Pro 250' : '60-1429-01',
                    'IPCP Pro 350' : '60-1417-01',
}

TLP_Models = {
                    'TLP Pro 525M' : '60-1561-02',
                    'TLP Pro 525T' : '60-1559-02',
                    'TLP Pro 725M' : '60-1563-02',
                    'TLP Pro 725T' : '60-1562-02',
                    'TLP Pro 1025T' : '60-1565-02',
                    'TLP Pro 1025M' : '60-1566-02',
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
]




###############################################################################
# End User Variables
###############################################################################




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
    else:
        print(f'Can not find TLP Part Number for {model_name}')
    



class Processor:
    
    def __init__(self, address, avlan_address):
        self.address = address
        self.avlan_address = avlan_address
        self.model_name = ExtractModelName(self.address)
        self.part_number = GetPartNumber(self.model_name)
        self.Has_AVLAN = self.DecideProcessorNetworks(self.model_name)


    def DecideProcessorNetworks(self, model_name):
        for AVLAN_Processor in AVLAN_Processors:
            if model_name in AVLAN_Processor:
                return True
            return False


class TLP:

    def __init__(self, address):
        self.address = address
        self.model_name = ExtractModelName(self.address)
        self.part_number = GetPartNumber(self.model_name)
        self.layout_file = self.GUI_Selector(self.model_name)
    

    def GUI_Selector(self, tlp_model_name):
        TLP_ModelNumberOnly = re.search(r'(\d{3,4})', tlp_model_name)
        GUI_Files = listdir(GUI_File_Directory)
    
        for GUI_File in GUI_Files:
            if TLP_ModelNumberOnly[1] in GUI_File:
                return GUI_File
        if len(GUI_Files) == 1:
            return GUI_Files[0]


MainProcessor = Processor(MainProcessor_IP, MainProcessor_AVLAN_IP) 
First_TLP = TLP(First_TLP_IP)

Second_TLP_Exist = False
if Second_TLP_IP is not None and Second_TLP_IP != '':
    Second_TLP_Exist = True
    Second_TLP = TLP(Second_TLP_IP)




with open(Default_JSON_File_Location, 'r') as DefaultJSON_File:
    JSON_Data = json.load(DefaultJSON_File)

JSON_Data['system']['name'] = SystemName
JSON_Data['system']['system_id'] = str(randrange(1000, 9999))

# Set Main Processor
JSON_Data['devices'][0]['name'] = f'{SystemName} - MainProcessor'
JSON_Data['devices'][0]['part_number'] = MainProcessor.part_number
JSON_Data['devices'][0]['network']['interfaces'][0]['address'] = MainProcessor.address

if MainProcessor.Has_AVLAN == True:
    JSON_Data['devices'][0]['network']['interfaces'][1]['address'] = MainProcessor.avlan_address
else:
    del(JSON_Data['devices'][0]['network']['interfaces'][1]) # if no AVLAN


# Set TLP('s)
JSON_Data['devices'][1]['name'] = f'{SystemName} - MainTLP'
JSON_Data['devices'][1]['part_number'] = First_TLP.part_number
JSON_Data['devices'][1]['network']['interfaces'][0]['address'] = First_TLP.address
JSON_Data['devices'][1]['ui']['layout_file'] = First_TLP.layout_file

if Second_TLP_Exist:
    JSON_Data['devices'][2]['name'] = f'{SystemName} - SecondTLP'
    JSON_Data['devices'][2]['part_number'] = Second_TLP.part_number
    JSON_Data['devices'][2]['network']['interfaces'][0]['address'] = Second_TLP.address
    JSON_Data['devices'][2]['ui']['layout_file'] = Second_TLP.layout_file

else:
    del(JSON_Data['devices'][2]) # if no second TLP


with open(f'{ProjectRootDirectory}/{SystemName}.json', 'w') as New_JSON_File:
    json.dump(JSON_Data, New_JSON_File)
