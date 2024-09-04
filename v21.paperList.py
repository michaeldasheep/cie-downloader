from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import path,remove
from requests import get

# CIE Past Paper Downloader v2.1
# PAPER LIST DOWNLOADER
# Download Multiple Past Papers with this

def setWriteParam(config):
    global paperFileWriteParam
    if config['writePaperList'] == 1:
        paperFileWriteParam = True
    else:
        paperFileWriteParam = False

def configLoad(file:str):
    configFileLocation = open(file, "r")
    configFile = configFileLocation.read()
    config = loads(configFile)
    configFileLocation.close() # Addressed bug opened by bohrium2b
    return config

def downloadPaperList(siteDirectory:str,paperListNumber:int):
    userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edge/123.0.2420.81'}
    url = f"{siteDirectory}{paperListNumber}.paperList.txt"
    try:
        response = get(url, headers=userAgent, timeout=60)
    except ConnectionError:
        print("CONNECTION ERROR WHEN GETTING PAPERLIST, ABORTING")
        exit()
    else:
        if response.status_code == 404:
            print("404 NOT FOUND WHEN GETTING PAPERLIST, ABORTING")
            exit()
        elif response.status_code != 200:
            print("NON 200 CODE WHEN GETTING PAPERLIST, ABORTING")
            exit()
        else:
            content = response.text.splitlines()
            return content

def main():
    config = configLoad("config.paperList.json")
    Path("./downloads").mkdir(parents=True, exist_ok=True)
    missingFile = open("./downloads/missing.txt","a")
    setWriteParam(config)
    missingFile.write(f"\n\nDOWNLOADING from {config['siteDirectory']}{config['paperListNumber']}.paperList.txt - Missing Files if any:")
    paperList = downloadPaperList(config['siteDirectory'],config['paperListNumber'])
    print(f"Downloading papers of {config['siteDirectory']}{config['paperListNumber']}.paperList.txt:")
    if paperFileWriteParam == True:
        paperNumberFile = open(f"./downloads/{config['paperListNumber']}.paperList.txt","a")
    for paper in paperList:
        if not path.exists(f"./downloads/{paper}"):
            url = f"{config['siteDirectory']}{paper}"
            successCode,paperDownloaded = download(url)
            if successCode == True:
                filePath = Path(f"./downloads/{paper}")
                filePath.write_bytes(paperDownloaded.content)
                try:
                    PdfReader(filePath)
                except PdfReadError:
                    print(f"Invalid PDF file ({filePath})")
                    missingFile.write(f"\nMISSING: {paper}")
                    remove(filePath)
                else:
                    if paperFileWriteParam == True:
                        paperNumberFile.write(f"{paper}\n")
            elif successCode == False:
                missingFile.write(f"\nMISSING: {paper}")
        else:
            print(f"{paper} - Already Exists, skipping")
    missingFile.write(f"\n\n If nothing was written above in MISSING, you are good! Redownloading may be required for other files or some papers might just not exist on the directory you are downloading from or maybe just not exist entirely.\n")
    missingFile.close()

if __name__ == "__main__":
    main()