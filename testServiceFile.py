import requests

filePath = 'C:\\DataSets\\SCUTFBP5500\\images\\AF1.jpg'
url = 'http://127.0.0.1:5000/facerate/1.0/imageresultforimagefile'
files = {'imageFile': open(filePath, 'rb')}
response = requests.post(url, files=files)
print(response.text)
