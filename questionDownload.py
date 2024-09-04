from requests import get

def download(siteDirectory:str, examNumber, season:str, year:int, type:str, paperNumber, paperVarient):
    userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edge/123.0.2420.81'}
    url = f"{siteDirectory}{examNumber}_{season}{year}_{type}_{paperNumber}{paperVarient}.pdf"
    try:
        response = get(url, headers=userAgent, timeout=60)
    except ConnectionError:
        successCode = False
        print(f"CONNECTION ERROR: {url}")
    else:
        if response.status_code == 404:
            successCode = False
            print(f"CONNECTION ERROR (404 NOT FOUND): {url}")
        elif response.status_code != 200:
            successCode = False
            print(f"CONNECTION ERROR (NON HTTP RESPONSE 200 CODE): {url}")
        elif "<!DOCTYPE html>" in response.text:
            successCode = False
            print(f"FILE NOT PDF: {url}")
        else:
            print(f"GET: {url}")
            successCode = True
    return successCode,response
