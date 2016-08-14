from slistener import SListener
import time, tweepy, sys

#consumer_token="<Your consumer_token>"
#consumer_secret="<Your consumer_secret_token>"

#key="Your_access_token"	
#secret="Your_access_Token_Secret"

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(key, secret)
api      = tweepy.API(auth)
logger=open("logfile.txt",'a')
logger.write("\nStarting run at "+time.strftime('%Y%m%d-%H%M%S')+"\n")
    	
try:
		listen = SListener(api)
		stream = tweepy.Stream(auth, listen)
except Exception as inst:
			logger.write(time.strftime('%Y%m%d-%H%M%S')+" : "+str(type(inst)))
			logger.write(" "+str(inst)+"\n")
			
session=0
		
def streamming():
	global session
	session+=1
	try:
		stream.sample()
	except Exception as inst:
		logger.write(time.strftime('%Y%m%d-%H%M%S')+" : "+str(type(inst)))
		logger.write(" "+str(inst)+"\n")
			#stream.disconnect()
			
	except KeyboardInterrupt:
		stream.disconnect()
		exit()
	streamming()

if __name__ == '__main__':
	streamming()
	
