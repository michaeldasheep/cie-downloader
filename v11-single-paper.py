from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import remove

# CIE Past Paper Downloader V1.1
# Download a single past paper with this

def main():
    configFileLocation = open("config.standalone.json", "r")
    configFile = configFileLocation.read()
    config = loads(configFile)
    configFileLocation.close() # Addressed bug opened by bohrium2b
    cond = True
    Path("./downloads").mkdir(parents=True, exist_ok=True)
    paper = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"ms",config['paperNumber'],config['varient'])
    filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_ms_{config['paperNumber']}{config['varient']}.pdf")
    filePath.write_bytes(paper.content)
    try:
        PdfReader(filePath)
    except PdfReadError:
        print(f"Invalid PDF file ({filePath})")
        remove(filePath)
    else:
        pass
    paper2 = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"qp",config['paperNumber'],config['varient'])
    filePath2 = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_qp_{config['paperNumber']}{config['varient']}.pdf")
    filePath2.write_bytes(paper2.content)
    try:
        PdfReader(filePath2)
    except PdfReadError:
        print(f"Invalid PDF file ({filePath2})")
        remove(filePath2)
    else:
        pass

if __name__ == "__main__":
    main()