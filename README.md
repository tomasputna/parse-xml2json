# parse-xml2json
Convert XML to JSON with Python 3 and defusedxml and push Sheets API

# Install
1. Enable [Step by Step Init Sheets API](https://developers.google.com/sheets/api/quickstart/python) 
2. Change API KEY: `SAMPLE_SPREADSHEET_ID = 'id'`
3. Change dir with XML file `loadXMLFile()`

# Usage
```sh
pip3 install defusedxml
$ python3 xml2json.py
```
# Conversion logic
Each element gets converted into an object of the form: `{'date': {'Subject': 'value', 'Subject': 'value', 'Subject': 'value', 'Subject': 'value'}}`


## Input
Load in `loadXMLFile()` dir with XML file

```xml
<statement>
 <transactions>
  <transaction date-post="2022-01-01">
   <trn-messages>
    <trn-message>some text</trn-message>
   </trn-messages>
  </transaction>
 </transactions>
</statement>
```

## Output
```json
{
    "statement": {
        "transactions": {
            "trn-messages": {
                "@number": "1",
                "@type": "0"
            }
        }
    }
}
```