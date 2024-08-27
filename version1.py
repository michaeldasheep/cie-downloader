from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import remove

def main():
    configFile = open("configV1.json", "r").read()
    config = loads(configFile)
    cond = True
    while cond == True:
        for i in range(1,4):
            paper = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"ms",config['paperNumber'],i)
            filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_ms_{config['paperNumber']}{i}.pdf")
            filePath.write_bytes(paper.content)
            try:
                PdfReader(filePath)
            except PdfReadError:
                print(f"invalid PDF file ({filePath})")
                remove(filePath)
            else:
                pass
        for i in range(1,4):
            paper = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"qp",config['paperNumber'],i)
            filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_qp_{config['paperNumber']}{i}.pdf")
            filePath.write_bytes(paper.content)
            try:
                PdfReader(filePath)
            except PdfReadError:
                print(f"invalid PDF file ({filePath})")
                remove(filePath)
            else:
                pass
        cond = False

if __name__ == "__main__":
    main()
