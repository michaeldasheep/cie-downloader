from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import remove

# CIE Past Paper Downloader V2
# Download Multiple Past Papers with this

def downloadLoop(siteDirectory,yearStart,yearEnd,examNumber,examSeason,season,paperNumber,paperNumberEnd,variants,missingFile):
    if paperNumberEnd == paperNumber:
        for year in range(yearStart,yearEnd+1):
            print(f"Downloading {examNumber} 20{year} {season} paper {paperNumber} ms and qp")
            paperCodes = ['ms','qp']
            for paperCode in paperCodes:
                for variant in range(0,variants):
                    if variant == 0 or variant == "0":
                        variant = ""
                    paper = download(siteDirectory,examNumber,examSeason,year,paperCode,paperNumber,variant)
                    filePath = Path(f"./downloads/{examNumber}_{examSeason}{year}_{paperCode}_{paperNumber}{variant}.pdf")
                    filePath.write_bytes(paper.content)
                    try:
                        PdfReader(filePath)
                    except PdfReadError:
                        print(f"Invalid PDF file ({filePath})")
                        missingFile.write(f"\nMISSING: {examNumber}_{examSeason}{year}_{paperCode}_{paperNumber}{variant}.pdf")
                        remove(filePath)
                    else:
                        pass
    elif paperNumber < paperNumberEnd:
        for paperNumberVar in range(paperNumber,paperNumberEnd+1):
            for year in range(yearStart,yearEnd+1):
                print(f"Downloading {examNumber} 20{year} {season} paper {paperNumberVar} ms and qp")
                paperCodes = ['ms','qp']
                for paperCode in paperCodes:
                    for variant in range(0,variants):
                        if variant == 0 or variant == "0":
                            variant = ""
                        paper = download(siteDirectory,examNumber,examSeason,year,paperCode,paperNumberVar,variant)
                        filePath = Path(f"./downloads/{examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf")
                        filePath.write_bytes(paper.content)
                        try:
                            PdfReader(filePath)
                        except PdfReadError:
                            print(f"Invalid PDF file ({filePath})")
                            missingFile.write(f"\nMISSING: {examNumber}_{examSeason}{year}_{paperCode}_{paperNumberVar}{variant}.pdf")
                            remove(filePath)
                        else:
                            pass
    else:
        print("ERROR")
        exit()

def main():
    configFileLocation = open("config.json", "r")
    configFile = configFileLocation.read()
    config = loads(configFile)
    configFileLocation.close() # Addressed bug opened by bohrium2b
    Path("./downloads").mkdir(parents=True, exist_ok=True)
    missingFile = open("./downloads/missing.txt","a")
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