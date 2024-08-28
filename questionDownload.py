from requests import get

def download(siteDirectory, examNumber, season, year, type, paperNumber, paperVarient):
    userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81'}
    url = f"{siteDirectory}{examNumber}_{season}{year}_{type}_{paperNumber}{paperVarient}.pdf"
    print(f"GET: {url}")
    response = get(url, headers=userAgent)
    return response