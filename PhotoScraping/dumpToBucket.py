#////////////////////////////////////////////////
#Gets images from Flickr and dumps to S3 bucket//
#Author: thanika							   //
#////////////////////////////////////////////////

import csv
import json
import boto3
import datetime
import flickrapi
import urllib.request
from collections import defaultdict

#Create S3 Bucket
s3_resource = boto3.resource('s3')
our_bucket = s3_resource.Bucket(name='flickrbigdatacu')

#Create Flickr object
key='72867a4388924cd9840ae813f23a70cf'
secret='49021d0404efb5c3'
flickr = flickrapi.FlickrAPI(key,secret, format='parsed-json')

#Dictionary to store image path in S3 and its tags
#{"id1": {"filename", "tag1", "tag2", "tag3"}, "id2": {"filename", "tag1", "tag2", "tag3"}, "id3": {"filename", "tag1", "tag2", "tag3"}}
image_dictionary = defaultdict(dict)

#Specify start and end dates. 
#For each date, 100 images are obtained by default. To change, vary "per_page".
#Around 200 days for 100k photos if 500 photos per day
#From date
date1 = '2019-03-20' 
#To date
date2 = '2019-03-29' 
start = datetime.datetime.strptime(date1, '%Y-%m-%d')
end = datetime.datetime.strptime(date2, '%Y-%m-%d')
step = datetime.timedelta(days=1)

#For each date
while start <= end:

	print(start.date())
	
	#Get 2 most interesting photos for the this date
	apiResult = flickr.interestingness.getList(date = str(start.date()), per_page = '2') 
	photos = apiResult["photos"]["photo"]

	#Dump one by one in S3 bucket
	for photo in photos:

		imageURL = 'https://farm'+str(photo["farm"])+'.staticflickr.com/'+photo["server"]+'/'+photo["id"]+'_'+photo["secret"]+'.jpg'
		
		try:
			urllib.request.urlretrieve(imageURL, 'temporary.jpg')

			#ML object detection here - gives three tags for the image
			#/////////////////////////////////////////////////////////

			#If tags are obtained, then store in dictionary and upload

			#Store in dictionary
			image_dictionary[photo["id"]]["filename"] = photo["id"]+'.jpg'
			image_dictionary[photo["id"]]["tag1"] = 'TAG 1'
			image_dictionary[photo["id"]]["tag2"] = 'TAG 2'
			image_dictionary[photo["id"]]["tag3"] = 'TAG 3'

			#Upload image to S3 Bucket
			our_bucket.upload_file(Filename='temporary.jpg', Key=photo["id"]+'.jpg')
			print("SUCCESSfully dumped photo with ID: "+photo["id"])

		except:
			print("FAILED to dump photo with ID: "+photo["id"])

	start += step

#Dump into json file
json.dump(image_dictionary, open("image_dictionary.json","w"))

#our_bucket.download_file('testing.jpg','testing_download.jpg')