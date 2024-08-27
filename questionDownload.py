from requests import get

def download(siteDirectory, examNumber, season, year, type, paperNumber, paperVarient):
    url = f"{siteDirectory}{examNumber}_{season}{year}_{type}_{paperNumber}{paperVarient}.pdf"
    print(url)
    response = get(url)
    return response