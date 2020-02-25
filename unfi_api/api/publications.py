import requests



def get_publication_types(session, digest_context):
    headers = {
        'authority': 'customers.unfi.com',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'x-requestdigest': digest_context,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'dnt': '1',
        'content-type': 'text/xml',
        'accept': '*/*',
        'origin': 'https://customers.unfi.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://customers.unfi.com/Pages/Publications.aspx',
        'accept-language': 'en-US,en;q=0.9',
    }

    data = '<Request xmlns="http://schemas.microsoft.com/sharepoint/clientquery/2009"' \
           ' SchemaVersion="15.0.0.0" ' \
           'LibraryVersion="15.0.0.0" ' \
           'ApplicationName="Javascript Library">' \
           '<Actions>' \
           '<ObjectPath Id="1" ObjectPathId="0" />' \
           '<ObjectPath Id="3" ObjectPathId="2" />' \
           '<ObjectPath Id="5" ObjectPathId="4" />' \
           '<ObjectPath Id="7" ObjectPathId="6" />' \
           '<ObjectIdentityQuery Id="8" ObjectPathId="6" />' \
           '<ObjectPath Id="10" ObjectPathId="9" />' \
           '<Query Id="11" ObjectPathId="9">' \
           '<Query SelectAllProperties="false">' \
           '<Properties />' \
           '</Query>' \
           '<ChildItemQuery SelectAllProperties="false">' \
           '<Properties>' \
           '<Property Name="Title" SelectAll="true" />' \
           '<Property Name="Library_x0020_Name" SelectAll="true" />' \
           '<Property Name="View_x0020_Mode" SelectAll="true" />' \
           '</Properties></ChildItemQuery>' \
           '</Query>' \
           '</Actions>' \
           '<ObjectPaths>' \
           '<StaticProperty Id="0" TypeId="{3747adcd-a3c3-41b9-bfab-4a64dd2f1e0a}" Name="Current" />' \
           '<Property Id="2" ParentId="0" Name="Web" />' \
           '<Property Id="4" ParentId="2" Name="Lists" />' \
           '<Method Id="6" ParentId="4" Name="GetByTitle">' \
           '<Parameters>' \
           '<Parameter Type="String">Publications</Parameter>' \
           '</Parameters>' \
           '</Method>' \
           '<Method Id="9" ParentId="6" Name="GetItems">' \
           '<Parameters>' \
           '<Parameter TypeId="{3d248d7b-fc86-40a3-aa97-02a75d69fb8a}">' \
           '<Property Name="DatesInUtc" Type="Boolean">true</Property>' \
           '<Property Name="FolderServerRelativeUrl" Type="Null" />' \
           '<Property Name="ListItemCollectionPosition" Type="Null" />' \
           '<Property Name="ViewXml" Type="String">' \
           '&lt;View&gt;&lt;RowLimit&gt;200&lt;/RowLimit&gt;&lt;/View&gt;' \
           '</Property>' \
           '</Parameter>' \
           '</Parameters>' \
           '</Method>' \
           '</ObjectPaths>' \
           '</Request>'

    response = requests.post('https://customers.unfi.com/_vti_bin/client.svc/ProcessQuery', headers=headers, data=data)

def get_catalog_listing():
    headers = {
        'authority': 'customers.unfi.com',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'x-requestdigest': '0xF5EF7D81C1F5EE9D8C169B7DAAD8802ED58797663E345CB955CC687870EBD287F441F4B437E110D29690D0292BF6511697F76E936908DF9F9A55109CBA81A0D0,22 Feb 2020 18:38:51 -0000',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'dnt': '1',
        'content-type': 'text/xml',
        'accept': '*/*',
        'origin': 'https://customers.unfi.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://customers.unfi.com/Pages/Publications.aspx',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'visid_incap_544876=3XGsunKOSgmCtucsPHIWZ1WvP1wAAAAAQUIPAAAAAAAipeDJ7cI/2rx0bnYc7V2E; __utmz=166635820.1547677604.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); visid_incap_536781=KNoZ4lWmQoOzbjrbj1d7EmjtQFwAAAAAQUIPAAAAAAC147AFVLsrS1x3I+arcoC6; _ga=GA1.2.1970117247.1547758954; visid_incap_546185=+h1cSv77S7qS2nNQtOy2F3+iVV0AAAAAQUIPAAAAAACrURbmTlbTJJaUVhytVwaf; visid_incap_545234=mWiDpgZVQ42RL/4DDWsGsWrXNV4AAAAAQUIPAAAAAACn7QQran0tC9bO7lQnW1eH; visid_incap_546189=sjyznFXhQ06IVF9vNHpJA4rXNV4AAAAAQUIPAAAAAABepAz6aG+mOou29f7S5ph1; __utma=166635820.212628298.1547677604.1580586855.1582044654.28; BIGipServerSharePoint_2013.app~SharePoint_2013_pool=2019229962.20480.0000; ASP.NET_SessionId=hocpavzdwlhjwuwwiovxdobe; WSS_FullScreenMode=false; menuAlertFlag=visible; incap_ses_1163_544876=WNiVIIoZJRPwd7RSzc4jEEphUV4AAAAAY9pwBiqSrZo5W+ftkmmq0g==; incap_ses_1163_545234=r7seCmsKHHvU/r5Szc4jEHxzUV4AAAAAsAW060DHQjX7rMzrFnLlVg==; FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+MDUudHx1bmZpc3RzfHNjYW5uaW5nQGNhcGVsbGFtYXJrZXQuY29tLDA1LnR8dW5maXN0c3xzY2FubmluZ0BjYXBlbGxhbWFya2V0LmNvbSwxMzIyNzMwMTg5MTkyMDQ1NzgsRmFsc2UsR0ZJZGpYTUF1RS83bTRvVFljdENYWUx3ckxZcnhKV0FEMFZDbU5CZUs2M1BJa2lUUHhOeC9jU0ZQSEFMYW1pZG5lZFIvK2lmU3BiSG4rM2VPUmM3VXhVYjBCWkcrMEpDMW1Idk9hYnlnS01FYU8yTnc4WFZJTnlZTVNHalRhMVBoWGZWQ1I3Wmdpd0lHbExJVnJtcTJlcWk0MG5zK0ZyRmJCVXhNbFlSZEM0TVZremtiM3NmQUpiWTBJbEJILzBrcXlYSTd0L2p5Qy96UkcxcHRtYnZORGtGMkZXT0ZaNGs3RTdkME4zY1dicEZIYVFOYmQySllGM0p4NVBaOU13Kzh2dE9HZ1RXNHNOeWxlaU9XWjBDK0plMlYyQlNLZWNBTDF4SFBJZ2YvTnp6cXpSRWRiTXg1UGgyVlYwYVB0WjBSRHhJYmRVbGFsa2hodXAwWG5qeWZ3PT0saHR0cHM6Ly9jdXN0b21lcnMudW5maS5jb20vPC9TUD4=',
    }


    data = r'$<Request xmlns="http://schemas.microsoft.com/sharepoint/clientquery/2009"' \
           ' SchemaVersion="15.0.0.0" ' \
           'LibraryVersion="15.0.0.0" ' \
           'ApplicationName="Javascript Library">' \
           '<Actions>' \
           '<ObjectPath Id="80" ObjectPathId="79" />' \
           '<Query Id="81" ObjectPathId="79">' \
           '<Query SelectAllProperties="true">' \
           '<Properties />' \
           '</Query>' \
           '<ChildItemQuery SelectAllProperties="true">' \
           '<Properties />' \
           '</ChildItemQuery>' \
           '</Query>' \
           '</Actions>' \
           '<ObjectPaths>' \
           '<Method Id="79" ParentId="23" Name="GetItems">' \
           '<Parameters>' \
           '<Parameter TypeId="{3d248d7b-fc86-40a3-aa97-02a75d69fb8a}">' \
           '<Property Name="DatesInUtc" Type="Boolean">true</Property>' \
           '<Property Name="FolderServerRelativeUrl" Type="Null" />' \
           '<Property Name="ListItemCollectionPosition" Type="Null" />' \
           '<Property Name="ViewXml" Type="String">' \
           '<View>' \
           '<Query>' \
           '<Where><And><And><And><And><And><And><And><Or><Or><Or><And><Geq>' \
           '<FieldRef Name=\'To\' />' \
           '<Value  IncludeTimeValue=\'TRUE\' Type=\'DateTime\'><Today /></ Value>' \
           '</Geq><Leq>' \
           '<FieldRef Name=\'From\' />' \
           '<Value IncludeTimeValue=\'TRUE\' Type=\'DateTime\'>' \
           '<Today />' \
           '</Value>' \
           '</Leq></And><And><Geq><' \
           'FieldRef Name=\'To\' /><Value  ' \
           'IncludeTimeValue=\'TRUE\' Type=\'DateTime\'><Today /></Value></Geq><IsNull><' \
           'FieldRef Name=\'From\' /></IsNull></And></Or><And><IsNull><' \
           'FieldRef Name=\'To\' /></IsNull><Leq><FieldRef ' \
           'Name=\'From\' /><Value  ' \
           'IncludeTimeValue=\'TRUE\' ' \
           'Type=\'DateTime\'><' \
           'Today /></Value></Leq></And></Or><And><IsNull><' \
           'FieldRef Name=\'To\' /></IsNull><IsNull><' \
           'FieldRef Name=\'From\' /></IsNull></And></Or><Or><Eq><' \
           'FieldRef Name=\'Personas\' /><' \
           'Value Type=\'Lookup\'>1</Value></Eq><IsNull><' \
           'FieldRef Name=\'Personas\' /></IsNull></Or></And><Or><Eq><' \
           'FieldRef Name=\'WestChannels\' /><Value ' \
           'Type=\'Lookup\'>3</Value></Eq><IsNull><' \
           'FieldRef Name=\'WestChannels\' /></IsNull></Or></And><Or><Eq><' \
           'FieldRef Name=\'WestWarehouses\' /><Value Type=\'Lookup\'>6</Value></Eq><IsNull>' \
           '<FieldRef Name=\'WestWarehouses\' /></IsNull></Or></And><Or><Eq><' \
           'FieldRef Name=\'IsHonestGreen\' /><Value ' \
           'Type=\'Integer\'>0</Value></Eq><IsNull><' \
           'FieldRef Name=\'IsHonestGreen\' /></IsNull></Or></And><Or><Eq><' \
           'FieldRef Name=\'IsAlberts\' /><Value Type=\'Integer\'>0</Value></Eq><IsNull><' \
           'FieldRef Name=\'IsAlberts\' /></IsNull></Or></And><Or><Eq><' \
           'FieldRef Name=\'IsNorCal\' /><Value Type=\'Integer\'>0</Value></Eq><IsNull>' \
           '<FieldRef Name=\'IsNorCal\'/></IsNull></Or></And><Or><Eq><FieldRef Name=\'IsTonys\'/><Value '\
           'Type=\'Integer\'>0</Value></Eq><IsNull><' \
           'FieldRef Name=\'IsTonys\' /></IsNull></Or></And><OrderBy><' \
           'FieldRef Name =\'SortOrder\' Type=\'Number\' Ascending = \'TRUE\' /></OrderBy></Where></Query><' \
           'RowLimit Paged=\'TRUE\'>30</RowLimit></View>' \
           '</Property>' \
           '</Parameter>' \
           '</Parameters>' \
           '</Method>' \
           '<Identity Id="23" Name="740c6a0b-85e2-48a0-a494-e0f1759d4aa7:site:8cf33302-461e-45c3-b914-2b969d565564:web:33b3c9f7-83c7-47e6-9540-f18bbac77aff:list:86f4bf57-e9d5-49cc-9974-01802d219d8d" />' \
           '</ObjectPaths>' \
           '</Request>'
    response = requests.post('https://customers.unfi.com/_vti_bin/client.svc/ProcessQuery', headers=headers, data=data)