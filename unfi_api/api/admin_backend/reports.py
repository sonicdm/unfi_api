import requests


def get_reports(token):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://customers.unfi.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://customers.unfi.com/Pages/Reports.aspx',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('AccountID', '759226'),
        ('AccountTypeID', '1'),
        ('ApplicationId', '1'),
        ('CustomerNumber', '001014    '),
        ('Region', 'West'),
        ('UserID', '155329'),
    )

    response = requests.get('https://adminbackend.unfi.com/api/Reports/GetReports', headers=headers, params=params)


def invoice_search(token):
    """
    search for invoice and get result as a link to download a pdf/xlsx/csv file
    :param token:
    :return:
    """
    headers = {
        'authority': 'customers.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'dnt': '1',
        'x-requested-with': 'XMLHttpRequest',
        'authorization': '155329~86164419-77c9-479b-b19f-83e8eb80147f:77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+MDUudHx1bmZpc3RzfGJ1bGtAY2FwZWxsYW1hcmtldC5jb20sMDUudHx1bmZpc3RzfGJ1bGtAY2FwZWxsYW1hcmtldC5jb20sMTMyMjc0MzE3Mjg3OTU0MzAxLEZhbHNlLGxaRGw3WWZBb1FmenNvUTZaT0VIdlRGZUxWRmNzc0RuTHBJZ2J6cXZhaERXZDlPbW9jOFg4RlhRa0d3S3VFczY3c1gvNjV0UDc1d3ZlYVkwV1ZuWUh1SXFYeHcyTmtaRm80dlZVZ0NNYVozOGxwZWtHVjErbEczTEtOMUpIbU04ak9qc0ZuLzdGeW0rWGZsd1haWExXVmNSQzQwT25wVTlSZGNCQzN6NUFkdjJMS1pnSFoycDR6S3Y2dk5SQTUwZ0dVZzBXbGlmbE9FKzVLbkVMdUNidk11VXVaVy9XL1RpaGdlalV2eUlJWGlMRzNHeUVVTlZHUU5Sb0NFaG5FSTBWWDhTR21aSVd1V0hXbEdWVk9KUEwxK2p0Z21pRUIvR1FiWmJRSUFYcURac0RvR1Rsd2pGaTRscXBuOWVObGdZdndDdDlzelZVSmdwdDJmM0tsY3FMdz09LGh0dHBzOi8vY3VzdG9tZXJzLnVuZmkuY29tLzwvU1A+:1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://customers.unfi.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://customers.unfi.com/Pages/ReportDetail.aspx?ReportID=26&ReportName=Invoice%20Search',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'visid_incap_536781=QRzIRFM6TC2qvoPgKWYeav+YUF4AAAAAQUIPAAAAAADn26qujEl9ESHhCxmN8LG4; visid_incap_544876=QuVHDFBpRt22lsPgKwjaCQKZUF4AAAAAQUIPAAAAAAC3WxN8v7615w58HkuGKolA; visid_incap_545234=OTE6OEpcTCisxRUNc3lStASZUF4AAAAAQUIPAAAAAADHjfUZfUm3oij1jDmU8yMM; nlbi_536781=4LF2cwUDnDk+9j5UKsD0NQAAAAAKrE3lu/ZidsonNM+TpqAv; incap_ses_207_536781=FcezLC5VGWvFvrOmB87fAqluU14AAAAApUkbnZ8p+0aAyPgi0nCnrA==; BIGipServerSharePoint_2013.app~SharePoint_2013_pool=2019229962.20480.0000; incap_ses_207_544876=bh05ALSn0mbRwrOmB87fAq1uU14AAAAAWq1qyoEL/d45r8TOX7wbEg==; incap_ses_207_545234=aAMMfOxPR3bmxLOmB87fAq9uU14AAAAAP24os+4D4q3g5ayJEINQ1Q==; FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+MDUudHx1bmZpc3RzfGJ1bGtAY2FwZWxsYW1hcmtldC5jb20sMDUudHx1bmZpc3RzfGJ1bGtAY2FwZWxsYW1hcmtldC5jb20sMTMyMjc0MzE3Mjg3OTU0MzAxLEZhbHNlLGxaRGw3WWZBb1FmenNvUTZaT0VIdlRGZUxWRmNzc0RuTHBJZ2J6cXZhaERXZDlPbW9jOFg4RlhRa0d3S3VFczY3c1gvNjV0UDc1d3ZlYVkwV1ZuWUh1SXFYeHcyTmtaRm80dlZVZ0NNYVozOGxwZWtHVjErbEczTEtOMUpIbU04ak9qc0ZuLzdGeW0rWGZsd1haWExXVmNSQzQwT25wVTlSZGNCQzN6NUFkdjJMS1pnSFoycDR6S3Y2dk5SQTUwZ0dVZzBXbGlmbE9FKzVLbkVMdUNidk11VXVaVy9XL1RpaGdlalV2eUlJWGlMRzNHeUVVTlZHUU5Sb0NFaG5FSTBWWDhTR21aSVd1V0hXbEdWVk9KUEwxK2p0Z21pRUIvR1FiWmJRSUFYcURac0RvR1Rsd2pGaTRscXBuOWVObGdZdndDdDlzelZVSmdwdDJmM0tsY3FMdz09LGh0dHBzOi8vY3VzdG9tZXJzLnVuZmkuY29tLzwvU1A+; ASP.NET_SessionId=yqd4nrbkay5jo0zrhtlbvatc; WSS_FullScreenMode=false; menuAlertFlag=visible',
    }

    data = {
        "ControlsAndValues": "CustomerNumber->>001014    ||"
                             "InvoiceNumber->>||"
                             "OrderNumber->>||"
                             "ProductNumber->>||"
                             "UPCCode->>||"
                             "StartDate->>8/23/2019||"
                             "EndDate->>2/23/2020||"
                             "Region->>west"
                             "||ReportPath->>/WebRewrite/Reports/OrderManagement/Invoice List",
        "ReportOptions": "CSV",
        "userID": "155329",
        "reportID": "26",
        "customerNumber": "001014    ",
        "emailAddress": "bulk@capellamarket.com",
        "chainAccounts": "",
        "actionType": "Save"
    }

    response = requests.post(
        'https://customers.unfi.com/_layouts/15/UNFI.UPO.WP.DynamicReportParams/AjaxBridge.aspx/SaveReportParams',
        headers=headers, json=data)
