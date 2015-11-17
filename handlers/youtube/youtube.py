#!/usr/bin/python
# Searches YouTube for specified query
# Returns video url of most relevant video

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

API_KEY = "AIzaSyAmSMLzMQIdfDDDfw3Z33OToO_w9rSZxPo"
API_NAME = "youtube"
API_VERSION = "v3"

def query(options):
	youtube = build(API_NAME, API_VERSION, developerKey = API_KEY)
	
	response = youtube.search().list(
		q = options.q,
		part = "id, snippet",
		maxResults = options.max_results
	).execute()
	
	videos = []
	
	for result in response.get("items", []):
		if result["id"]["kind"] == "youtube#video":
			videos.append("%s (%s)" % (result["snippet"]["title"],
                                 result["id"]["videoId"]))
                                 
	print "Videos:\n", "\n".join(videos)
    
if __name__ == "__main__":
	argparser.add_argument("--q", help="query term", default="Google")
	argparser.add_argument("--max-results", help="max results to show", default=10)
	args = argparser.parse_args()

	try:
		query(args)
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)