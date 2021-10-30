from unfi_api import UnfiApiClient



if __name__ == '__main__':
    api = UnfiApiClient("CapellaAPI", "CapellaAPI2489")
    result = api.search("field day")
    pass