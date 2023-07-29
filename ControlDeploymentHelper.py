import requests
import re
import json


#### Created by Matthew Franklin ###
#### Please see https://github.com/mefranklin6/ControlDeploymentHelper/ ####

# Execute this code on your computer, don't put it on the processor


###############################################################################
# Begin User Variables
###############################################################################

# Root directory of the project on your computer
# ex: 'C:/Users/<YOURUSER>/Documents/<PROJECTFOLDERNAME>'
ProjectRootDirectory = 'C:/Users/mefranklin/Documents/Github/VSCodeTemplate'

# becomes your project descriptor JSON file name
RoomName = 'TestRoom1' 

# Default project descriptor JSON file location
# !!!! IMPORTANT Do not have this in the root of your project file !!!!
Default_JSON_File_Location = 'rfile/DEFAULT.json'

Processor_IP = '192.168.253.250'
TLP_IP = '192.168.253.8'


"""
 instead of this manual dictionary of {Model : PartNumber},
 it could also be possible to script a login to the admin web interface
 and grab the part number there.
 
 I wanted to keep web scraping to a mimimum, 
 and it also keeps passwords out of scripts,
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




with open(Default_JSON_File_Location, 'r') as DefaultJSON_File:
    JSON_Data = json.load(DefaultJSON_File)


# field for main processor part number
JSON_Data['devices'][0]['part_number'] = str(PairModelNameNumber(Processor_IP)[1])


# field for first TLP part number
JSON_Data['devices'][1]['part_number'] = str(PairModelNameNumber(TLP_IP)[1])

#TODO: add the rest of the fields as they make sense, such as IP addresses and whatnot


with open(f'{ProjectRootDirectory}/{RoomName}.json', 'w') as New_JSON_File:
    json.dump(JSON_Data, New_JSON_File)
