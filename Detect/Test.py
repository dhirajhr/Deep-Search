import numpy
import cv2
import scenedetect
import scenedetect.detectors
import requests
import re, math
import json
from collections import Counter
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#API Call
def apiCall(url):
    subscription_key = "cfa2ac95fcf04101b79b839837876d16"
    assert subscription_key
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    vision_analyze_url = vision_base_url + "describe"
    image_url = url
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
    params   = {'visualFeatures': 'Categories,Description,Color'}
    data     = {'url': image_url}
    response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
    #response.raise_for_status()
    analysis = response.json()
    #print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    return image_caption

def addo(x):
    print(x)
    return 10


#API Call


#Upload

def uploadImg(myblob):
    from azure.storage.blob import BlockBlobService
    block_blob_service = BlockBlobService(account_name='eventdetect', account_key='VdqUAaFmd5K8bF5Pp+wt6cDfYUWiAtR2ib7+rKP76sqgJwSo0+friYmuVd+Y5oEWDh6/4oaRa423fXproar3aw==')
    block_blob_service.create_container('mycontainer')
    from azure.storage.blob import PublicAccess
    block_blob_service.create_container('mycontainer', public_access=PublicAccess.Container)
    block_blob_service.set_container_acl('mycontainer', public_access=PublicAccess.Container)
    from azure.storage.blob import ContentSettings
    block_blob_service.create_blob_from_path(
        'mycontainer',
        myblob,
        'Images\\'+myblob,
        content_settings=ContentSettings(content_type='image/jpg')
            )

#Upload


#Cosine Similarity Measure
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator
WORD = re.compile(r'\w+')
def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

#CSM
def finalFunc(textSearch):
    scene_list = []        # Scenes will be added to this list in detect_scenes().
    path = 'goldeneye.mp4'  # Path to video file.

    # Usually use one detector, but multiple can be used.

    detector_list = [
        scenedetect.detectors.ContentDetector(threshold=30)

    ]
    #scenedetect.save_preview_images('C:\\Users\\dramn\\PycharmProjects\\Scene\\Detect',4,True,True,1)


    '''video_framerate, frames_read = scenedetect.detect_scenes_file(
        path, scene_list, detector_list)
    # scene_list now contains the frame numbers of scene boundaries.
    #print(scene_list)
    #Write Scenes
    writeDict=dict()
    fhand=open('goldeneye.txt','w')
    for i in range(len(scene_list)):
        writeDict[i]=scene_list[i]
    c=json.loads("[{}]".format(json.dumps(writeDict)))
    fhand.write(json.dumps(c))'''
    #Write Scenes
    finalDict=dict()
    fhand=open('jamesbond.txt')
    bigDict=json.load(fhand)
    scene_list=[]
    for i in bigDict[0]:
        scene_list.append(bigDict[0][i])
    cap = cv2.VideoCapture('goldeneye.mp4')
    video_name='goldeneye.mp4'
    if video_name=='goldeneye.mp4':
        frame_name = "frame"
    elif video_name=='Hacktech.mp4':
        frame_name = "frame1"
    elif video_name=='Crime.mp4':
        frame_name = "frame2"
    for frame_no in scene_list:
        cap = cv2.VideoCapture(video_name) #video_name is the video being called
        cap.set(1,frame_no); # Where frame_no is the frame you want
        ret, frame = cap.read() # Read the frame
        #cv2.imshow('window_name', frame)
        cv2.imwrite("Images\\"+frame_name+"_" + str(frame_no) + ".jpg",frame)
        uploadImg(frame_name+"_" + str(frame_no) + ".jpg")

        '''while True:
            ch = 0xFF & cv2.waitKey(1) # Wait for a second
            if ch == 27:
                break'''

    for item in scene_list:
        url='https://eventdetect.blob.core.windows.net/mycontainer/'+frame_name+'_'+str(item)+'.jpg'
        finalDict[item]=apiCall(url)
    #finalDict[0] = apiCall('https://eventdetect.blob.core.windows.net/mycontainer/frame_1281.jpg')
    #print (finalDict)
    #textToSearch='Izabella scorupco'#Search
    textToSearch=textSearch
    # Calculate Cosine Similarity::
    WORD = re.compile(r'\w+')



    text1 = textToSearch
    vector1 = text_to_vector(text1)
    max=-1.0
    frameFound=-1.0
    for item in finalDict:
        text2 = finalDict[item]
        #print(text2)
        vector2 = text_to_vector(text2)
        cosine = get_cosine(vector1, vector2)
        if cosine>max:
            frameFound=item
            max=cosine
    timeAppeared=frameFound/23
    #print (timeAppeared)
    return str(int(timeAppeared))
    #Done
finalFunc('window')
