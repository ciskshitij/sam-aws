
import json
from flask_lambda import FlaskLambda
from flask import request,jsonify
from datetime import date

import mysql.connector
from mysql.connector import Error

app = FlaskLambda(__name__)

try:
    connection_config_dict = {
        'user': 'admin',
        'password': 'asdqwe123',
        'host': 'database-1.ckytshswooyn.ap-south-1.rds.amazonaws.com',
        'database': 'db1',
        'raise_on_warnings': True,
        'use_pure': False,
        'autocommit': True,
    }
    connection = mysql.connector.connect(**connection_config_dict)

    if connection.is_connected():
        # cursor = connection.cursor()
        # cursor.execute("CREATE TABLE Video(videoId INT NOT NULL AUTO_INCREMENT,youtubeVideoId VARCHAR (200),title varchar(101),channelId varchar(100),totalViews int default 0,totalCountOfComments int default 0,totalThumbsUp int default 0,totalThumbsDown int default 0,createDate date,PRIMARY KEY (videoId))")
        print("You are connected to database")

except Error as e:
    print("Error while connecting to MySQL", e)

@app.route('/', methods=['GET'])
def index():
    return jsonify(create_response_format(msg= "Welcome to YouTube data storage and retrieval API using Python and the AWS SAM framework"))


@app.route('/videos', methods=['GET','POST'])
def videos_api():
    if request.method == 'GET':
        try:
            cursor = connection.cursor()
            cursor.execute("select * from Video;")
            videos = cursor.fetchall()
            print(videos,'------')
            if len(videos)==0:
                return jsonify(create_response_format(status=404, msg="Videos not available"))
            columns = ['videoId','youtubeVideoId','title','channelId','totalViews','totalCountOfComments','totalThumbsUp','totalThumbsDown','createDate']
            data = [{k:v for k,v in zip(columns, video)} for video in videos]
            return jsonify(create_response_format(status=200, msg="Videos get", result=data))
        except Error as e:
            return jsonify(create_response_format(status=400, msg="Error",error=e))

    elif request.method == 'POST':     
        data = json.loads(request.data)

        youtubeVideoId = data['id']
        title = data['snippet']['title']
        channelId = data['snippet']['channelId']
        totalViews = data['statistics']['viewCount']
        totalCountOfComments = data['statistics']['commentCount']
        totalThumbsUp = data['statistics']['likeCount']
        totalThumbsDown = data['statistics']['dislikeCount']
        createDate = date.today()
        try:
            sql ="INSERT INTO Video (youtubeVideoId, title, channelId, totalViews, totalCountOfComments, totalThumbsUp, totalThumbsDown,createDate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (youtubeVideoId, title, channelId, totalViews, totalCountOfComments, totalThumbsUp, totalThumbsDown,createDate)
            cursor = connection.cursor()
            cursor.execute(sql,val)
            connection.commit()
            videoId = cursor.lastrowid
            cursor.close()
            return jsonify(create_response_format(msg="Video '{0}' created".format(videoId),status=201))
        except Error as e:
            print("Error while connecting to MySQL", e)
            return jsonify(create_response_format(status=400, msg="Error", error=e))

        return jsonify(create_response_format(status=404, msg="Unexpected error"))
    


@app.route('/video/<videoId>', methods = ['GET','PUT','DELETE'])
def video_api(videoId):
    if request.method == 'GET':
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Video WHERE videoId='{0}'".format(videoId))
            video = cursor.fetchone()
            if not video:
                return jsonify(create_response_format(status=404, msg="Video id '{0}' not available".format(videoId)))

            columns = ['videoId','youtubeVideoId','title','channelId','totalViews','totalCountOfComments','totalThumbsUp','totalThumbsDown','createDate']
            data = {k:v for k, v in zip(columns, video)}
            return jsonify(create_response_format(status=200, msg="Video '{0}' get".format(videoId), result=data))
        except Error as e:
            return jsonify(create_response_format(status=400, msg="Error",error=e))

    elif request.method == 'PUT':
        data = json.loads(request.data)

        youtubeVideoId = data['id']
        title = data['snippet']['title']
        channelId = data['snippet']['channelId']
        totalViews = data['statistics']['viewCount']
        totalCountOfComments = data['statistics']['commentCount']
        totalThumbsUp = data['statistics']['likeCount']
        totalThumbsDown = data['statistics']['dislikeCount']
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE Video SET youtubeVideoId=%s, title=%s, channelId=%s, totalViews=%s, totalCountOfComments=%s, totalThumbsUp=%s, totalThumbsDown=%s WHERE videoId=%s""", (youtubeVideoId, title, channelId, totalViews, totalCountOfComments, totalThumbsUp, totalThumbsDown,videoId))
            connection.commit()
            cursor.close()
            return jsonify(create_response_format(msg="Successfully video '{0}' updated".format(videoId),status=200))
        except Error as e:
            return jsonify(create_response_format(status=400, msg="Error", error=e))

    elif request.method == 'DELETE':
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Video WHERE videoId='{0}'".format(videoId))
            return jsonify(create_response_format(msg="Video '{0}' deleted".format(videoId),status=200))
        except Error as e:
            return jsonify(create_response_format(status=400, msg="Error", error=e))

    return jsonify(create_response_format(status=404, msg="Unexpected error"))


def create_response_format(msg=None,status=None,error=None,result=None,extra_data={}):
    context = {}
    
    if status:        
        context['status'] = status
    if msg:
        context['message'] = msg
    if error:        
        context['error'] = error
    if result:        
        context['result'] = result
    return context


