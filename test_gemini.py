import urllib.request, json
key = open("/Users/ts-1148/Desktop/Pulu-workspace/.env").read().split('GEMINI_API_KEY="')[1].split('"')[0]
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
req = urllib.request.Request(url)
try:
    data = json.loads(urllib.request.urlopen(req).read().decode())
    for m in data.get("models", []):
        print(m["name"])
except Exception as e:
    import urllib.error
    if isinstance(e, urllib.error.HTTPError):
        print(e.read().decode())
    else:
        print(e)
