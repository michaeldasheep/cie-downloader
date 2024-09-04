from pathlib import Path
from json import loads
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import remove
from requests import get

# CIE Past Paper Downloader V1.1
# Download a single past paper with this

def main():
    configFileLocation = open("config.standalone.json", "r")
    configFile = configFileLocation.read()
    config = loads(configFile)
    configFileLocation.close() # Addressed bug opened by bohrium2b
    Path("./downloads").mkdir(parents=True, exist_ok=True)
    successCode,paper = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"ms",config['paperNumber'],config['varient'])
    filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_ms_{config['paperNumber']}{config['varient']}.pdf")
    filePath.write_bytes(paper.content)
    try:
        PdfReader(filePath)
    except PdfReadError:
        print(f"Invalid PDF file ({filePath})")
        remove(filePath)
    else:
        pass
    successCode2,paper2 = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"qp",config['paperNumber'],config['varient'])
    filePath2 = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_qp_{config['paperNumber']}{config['varient']}.pdf")
    filePath2.write_bytes(paper2.content)
    try:
        PdfReader(filePath2)
    except PdfReadError:
        print(f"Invalid PDF file ({filePath2})")
        remove(filePath2)
    else:
        pass

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

if __name__ == "__main__":
    main()