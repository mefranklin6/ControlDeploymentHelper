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

Processor_IP = '192.168.253.250'
TLP_IP = '192.168.253.8'


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


def PairModelNameNumber(ip):
    ModelName = ExtractModelName(ip)

    if ModelName in ProcessorModels.keys():
        ModelNumber = ProcessorModels[ModelName]
        return (ModelName, ModelNumber)
    
    if ModelName in TLP_Models.keys():
        ModelNumber = TLP_Models[ModelName]
        return (ModelName, ModelNumber)
    



MainProcessorModenNameNumber = PairModelNameNumber(Processor_IP)
First_TLP_NameNumber = PairModelNameNumber(TLP_IP)




# TODO: add support for multiple TLP's
def GUI_Selector():
    TLP_ModelNumberOnly = re.search(r'(\d{3})', First_TLP_NameNumber[0])
    GUI_Files = listdir(GUI_File_Directory)
    
    for GUI_File in GUI_Files:
        if TLP_ModelNumberOnly[1] in GUI_File:
            return GUI_File




with open(Default_JSON_File_Location, 'r') as DefaultJSON_File:
    JSON_Data = json.load(DefaultJSON_File)


# Read
MainProcessorDeviceFields = JSON_Data['devices'][0]

#Set
MainProcessorDeviceFields['name'] = f'{RoomName} - MainProcessor'
MainProcessorDeviceFields['part_number'] = str(MainProcessorModenNameNumber[1])
# TODO: format MainProcessorNetworkFields based on if processor has AVLAN or just LAN


# Read
First_TLP_DeviceFields = JSON_Data['devices'][1]
First_TLP_NetworkFields = First_TLP_DeviceFields['network']['interfaces']

#Set
First_TLP_DeviceFields['name'] = f'{RoomName} - MainTLP'
First_TLP_DeviceFields['part_number'] = str(First_TLP_NameNumber[1])
First_TLP_NetworkFields[0]['address'] = TLP_IP
First_TLP_DeviceFields['ui']['layout_file'] = GUI_Selector()




#TODO: add the rest of the fields as they make sense, such as IP addresses and whatnot


with open(f'{ProjectRootDirectory}/{RoomName}.json', 'w') as New_JSON_File:
    json.dump(JSON_Data, New_JSON_File)
