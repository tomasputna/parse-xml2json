from __future__ import print_function
import os.path
import json 
import xmltodict 
import time
import glob

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1vreBYUh_WrCR7VY6ZPxZU1Y4hciDI7AkKeqBz9nKs0g'
SAMPLE_RANGE_NAME = 'M!A2:C'

def loadXMLFile():
    XMLlist = glob.glob("./xml_file/*.XML")
    return XMLlist

def parseXML():
    # listing all file in dir
    sortedTrnMessages = []
    sortCompTrnMessage = {}
    dictXmlMsg = []

    for file in loadXMLFile():
        print(file)
        with open(file) as xml_file: 
            data_dict = xmltodict.parse(xml_file.read()) 
            xml_file.close() 
            
            # generate the object using json.dumps()  
            # corresponding to json data 
            json_data = json.dumps(data_dict) 
            person_dict = json.loads(json_data)

            trnMessage = {}
            completeTrnMessage = {}          
            
            # parse json
            for key in person_dict['statement']['transactions']['transaction']:
                if (type(key['trn-messages']) is dict):
                    trnMessage[key['trn-messages']['trn-message']['#text']] = key['@amount']
                else:
                    if (type(key['trn-messages'][1]['trn-message']) is dict):
                        trnMessage[key['trn-messages'][1]['trn-message']['#text']] = key['@amount']
                    else:
                        trnMessage[key['trn-messages'][1]['trn-message'][-1]['#text']] = key['@amount']
                
                completeTrnMessage[person_dict['statement']['header']['stmt']['@date']] = trnMessage

            new_stack = dict(completeTrnMessage)
            dictXmlMsg.append(new_stack)

    return dictXmlMsg
   
    # sorted dictionary        
    #for keys in dictXmlMsg:
    #    for k, v in keys.items():
    #        sortedDict = {k: v for k, v in sorted(v.items(), key=lambda item: item[1])}
    #        sortCompTrnMessage[k] = sortedDict
    #        sortedTrnMessages.append(sortCompTrnMessage)

    #return sortedTrnMessages

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    
    # Prepare Data
    data = []
    finalData=[]
    dataFromXml = parseXML()
    
    for values in dataFromXml:
        print(values)
        for k, v in values.items():
            for kk, vv in v.items():
                data.append(k)
                data.append(kk)
                data.append(vv)
                new_stack = list(data)
                finalData.append(new_stack)
                data.clear()
 
    res = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":finalData}).execute()
    print(res)

if __name__ == '__main__':
    main()
    