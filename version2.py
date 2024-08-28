from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import remove

def main():
    configFile = open("configV2.json", "r").read()
    config = loads(configFile)
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
        for year in range(config['yearStart'],config['yearEnd']+1):
            print(f"Downloading {config['examNumber']} 20{year} paper {config['paperNumber']} ms and qp")
            for varient in range(0,config['varients']+1):
                if varient == 0:
                    varient = ""
                paper = download(config['siteDirectory'],config['examNumber'],config['season'],year,"ms",config['paperNumber'],varient)
                filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{year}_ms_{config['paperNumber']}{varient}.pdf")
                filePath.write_bytes(paper.content)
                try:
                    PdfReader(filePath)
                except PdfReadError:
                    print(f"Invalid PDF file ({filePath})")
                    missingFile.write(f"\nMISSING: {config['examNumber']}_{config['season']}{year}_ms_{config['paperNumber']}{varient}.pdf")
                    remove(filePath)
                else:
                    pass
            for varient in range(0,config['varients']+1):
                if varient == 0:
                    varient = ""
                paper = download(config['siteDirectory'],config['examNumber'],config['season'],year,"qp",config['paperNumber'],varient)
                filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{year}_qp_{config['paperNumber']}{varient}.pdf")
                filePath.write_bytes(paper.content)
                try:
                    PdfReader(filePath)
                except PdfReadError:
                    print(f"Invalid PDF file ({filePath})")
                    missingFile.write(f"\nMISSING: {config['examNumber']}_{config['season']}{year}_qp_{config['paperNumber']}{varient}.pdf")
                    remove(filePath)
                else:
                    pass
        missingFile.write(f"\n\n If nothing was written above in MISSING, you are good! Redownloading may be required for other files or some papers might just not exist on the directory you are downloading from or maybe just not exist entirely.\n")
    else:
        print("ERROR")
    missingFile.close()

if __name__ == "__main__":
    main()