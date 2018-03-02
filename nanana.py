from __future__ import print_function
import time
import requests
import cv2
import operator
import numpy as np
from PIL import Image
from io import BytesIO
import http.client, urllib.parse, json
from xml.etree import ElementTree
from IPython.display import Audio, display
import matplotlib.pyplot as plt
subscription_key = "4d87050e410c4251952eedcd102b129b"
#assert subscription_key
import os
#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"
import requests
cap = cv2.VideoCapture(1)
parentCount = 0
while(cap.isOpened()):
    _,frame = cap.read()
    #cv2.imwrite("pic%d.jpg" % count, frame)
    cv2.imwrite("picPP.jpg", frame)
    cv2.waitKey(0)
    time.sleep(0.5)
    pathToFileInDisk = r'picPP.jpg'
    image_data = open(pathToFileInDisk, "rb").read()
    vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v1.0/"
    vision_analyze_url = vision_base_url + "analyze"
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key ,
               "Content-Type": "application/octet-stream" }
    params   = {'visualFeatures': 'Categories,Description,Color'}
    apiKey = "dbeb3e64bd764f79927488d937c9a277"
    params1 = ""
    headers1 = {"Ocp-Apim-Subscription-Key": apiKey}
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"
    from gtts import gTTS
    response = requests.post(vision_analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    print(image_caption)
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params1, headers1)
    response1 = conn.getresponse()
    data = response1.read()
    conn.close()
    accesstoken = data.decode("UTF-8")
    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)')
    voice.text = image_caption

    headers = {"Content-type": "application/ssml+xml",
			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
			"Authorization": "Bearer " + accesstoken,
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
			"User-Agent": "TTSForPython"}

    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
    response1 = conn.getresponse()
    print(type(response1))
    print(response1.status, response1.reason)

    data2 = response1.read()
    conn.close()
    tts = gTTS(image_caption, lang='en')
    tts.save("pcvoice.mp3")
    os.system("start pcvoice.mp3")

    #display(audio_bytes)
