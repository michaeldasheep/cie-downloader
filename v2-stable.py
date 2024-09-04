from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import path,remove

# CIE Past Paper Downloader V2
# Download Multiple Past Papers with this

def downloadLoop(siteDirectory,yearStart,yearEnd,examNumber,examSeason,season,paperNumber,paperNumberEnd,variants,missingFile):
    paperCodes = ['qp','ms']
    if paperNumberEnd == paperNumber or paperNumberEnd == 0:
        if paperFileWriteParam == True:
            paperNumberFile = open(f"./downloads/{paperNumber}.paperList.txt","a")
        for year in range(yearStart,yearEnd+1):
            print(f"Downloading {examNumber} 20{year} {season} paper {paperNumber} qp and ms")
            for paperCode in paperCodes:
                for variant in range(0,variants+1):
                    runDownload(missingFile,variant,siteDirectory,examNumber,examSeason,year,paperCode,paperNumber,paperNumberFile)
    elif paperNumber < paperNumberEnd:
        for paperNumberVar in range(paperNumber,paperNumberEnd+1):
            if paperFileWriteParam == True:
                paperNumberFile = open(f"./downloads/{paperNumberVar}.paperList.txt","w")
            for year in range(yearStart,yearEnd+1):
                print(f"Downloading {examNumber} 20{year} {season} paper {paperNumberVar} qp and ms")
                for paperCode in paperCodes:
                    for variant in range(0,variants+1):
                        runDownload(missingFile,variant,siteDirectory,examNumber,examSeason,year,paperCode,paperNumberVar,paperNumberFile)
    else:
        print("ERROR")
        exit()

def runDownload(missingFile,variant: int,siteDirectory,examNumber,examSeason,year: int,paperCode: str,paperNumberVar,paperNumberFile):
    if not path.exists(f"./downloads/{examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf"):
        if variant == 0:
            varient = ""
        else:
            varient = variant
        url = f"{siteDirectory}{examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf"
        successCode,paper = download(url)
        if successCode == True:
            filePath = Path(f"./downloads/{examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf")
            filePath.write_bytes(paper.content)
            try:
                PdfReader(filePath)
            except PdfReadError:
                print(f"Invalid PDF file ({filePath})")
                missingFile.write(f"\nMISSING: {examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf")
                remove(filePath)
            else:
                if paperFileWriteParam == True:
                    paperNumberFile.write(f"{examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf\n")
        elif successCode == False:
            missingFile.write(f"\nMISSING: {examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf")
    else:
        print(f"{examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf - Already Exists, skipping")

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

def main():
    config = configLoad("config.json")
    Path("./downloads").mkdir(parents=True, exist_ok=True)
    missingFile = open("./downloads/missing.txt","a")
    setWriteParam(config)
    if (config['yearStart'] < config['yearEnd'] or config['yearStart'] == config['yearEnd']) and (config['season'] == "w" or config['season'] == "s" or config['season'] == "m"):
        if config['season'] == "w":
            examSeason = "Winter"
        elif config['season'] == "s":
            examSeason = "Summer"
        elif config['season'] == "m":
            examSeason = "March"
        missingFile.write(f"\n\nDOWNLOADING from 20{config['yearStart']} to 20{config['yearEnd']} {config['examNumber']} {examSeason} papers {config['paperNumber']} - Missing Files if any:")
        downloadLoop(config['siteDirectory'],config['yearStart'],config['yearEnd'],config['examNumber'],config['season'],examSeason,config['paperNumber'],config['paperNumberEnd'],config['variants'],missingFile)
        missingFile.write(f"\n\n If nothing was written above in MISSING, you are good! Redownloading may be required for other files or some papers might just not exist on the directory you are downloading from or maybe just not exist entirely.\n")
    elif (config['yearStart'] < config['yearEnd'] or config['yearStart'] == config['yearEnd']) and (config['season'] == "all"):
        seasons = {"w":"Winter","s":"Summer","m":"March"}
        for season in seasons.keys():
            examSeason = seasons[season]
            missingFile.write(f"\n\nDOWNLOADING from 20{config['yearStart']} to 20{config['yearEnd']} {config['examNumber']} {examSeason} papers {config['paperNumber']} - Missing Files if any:")
            downloadLoop(config['siteDirectory'],config['yearStart'],config['yearEnd'],config['examNumber'],season,examSeason,config['paperNumber'],config['paperNumberEnd'],config['variants'],missingFile)
        missingFile.write(f"\n\n If nothing was written above in MISSING, you are good! Redownloading may be required for other files or some papers might just not exist on the directory you are downloading from or maybe just not exist entirely.\n")
    else:
        print("ERROR")
    missingFile.close()

if __name__ == "__main__":
    main()