from tweepy import StreamListener
import json, time, sys, os
from push_notification import Push_Notification
import requests as req


class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'tweet'):
    	#print("Slistener __init__ started")
    	self.api = api or API()
    	self.counter = 0
    	self.fprefix = fprefix
    	self.jsonfilename="jsondata/"+time.strftime('%d-%m')+"/"+fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + ".json"
    	self.logfilename="logfile.txt"
    	self.jsondir=os.path.dirname(self.jsonfilename)
    	if not os.path.exists(self.jsondir):	os.makedirs(self.jsondir)
    	logger=open(self.logfilename,'a')
    	self.jsonoutput=open(self.jsonfilename,"w")
    	logger.write(time.strftime('%Y%m%d-%H%M%S')+" : file "+self.jsonfilename+" created\n")
    	logger.close()
    	self.delout=open("delete.txt",'w')
    	self.resultfilename="results_for_scenario_A"
    	self.pn=Push_Notification()
        
    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            logger=open(self.logfilename,'a')
            logger.write(time.strftime('%Y%m%d-%H%M%S').encode('utf-8')+" : "+warning['message']+"\n")
            logger.close()
        	#print (warning['message'])
            return false

    def on_status(self, status):
        try:
        	jo=json.loads(status)
        	if jo['lang']=='en':
        		#print(jo['text'])
        		topics=self.pn.relevanttopics(jo['text'])
        		#print(topics)
        		if len(topics)>0:
        			out=open(self.resultfilename,'a')
        			for topic in topics:
        				record_name="Submitted_tweet/"+topic
        				recorddir=os.path.dirname(record_name)
        				if not os.path.exists(recorddir):	os.makedirs(recorddir)   	
        				record=open(record_name,'a')
        				record.close();
        				if not self.pn.ifduplicate(topic,jo['text']):
        					out.write(str(time.strftime('%Y%m%d-%H%M%S'))+str(topic)+" "+str(jo['id'])+"\n")
        					record=open(record_name,'a')
        					record.write(str(jo['text'])+"\n")
        					record.close()
        					#print(str(jo['id'])+" : "+str(jo['text']))
        					headers={}
        					headers['Content-type']='application/json'
        					#submit="http://54.164.151.19:80/tweet/"+topic+"/"+str(jo['id'])+"<Your Client-id>"
        					try:
        						#r=req.post(submit,headers)
        						logger=open("Submission_info",'a')
        						logger.write(time.strftime('%Y%m%d-%H%M%S')+" : "+topic+" - "+str(jo['id']))
        						#logger.write(r)
        						logger.write("\n")
        						logger.close()
        					except Exception as excp:
        						logger=open(self.logfilename,'a')
        						logger.write(time.strftime('%Y%m%d-%H%M%S')+" : ")
        						logger.write(type(excp))
        						logger.write(" : "+str(excp)+"\n")
        						logger.close()
        	
        					record.close();	
        				#print(str(str(topic)+"  "+jo['text']))
        			out.close()			 
        except Exception as inst:
        	logger=open(self.logfilename,'a')
        	logger.write(time.strftime('%Y%m%d-%H%M%S')+" : "+str(type(inst))+ " : "+inst+"\n")
        	logger.close()
        	#print(str(type(inst)))
        	#print(inst)
        
        try:
        	self.jsonoutput.write(status+"\n")
        except UnicodeEncodeError:
        	#print(time.strftime('%Y%m%d-%H%M%S')+" DONT KNOW : UnicodeEncodeError\n")
        	logger=open(self.logfilename,'a')
        	logger.write(time.strftime('%Y%m%d-%H%M%S')+" DONT KNOW : UnicodeEncodeError\n")
        	logger.close()
       # print(self.counter)
        self.counter += 1

        if self.counter >= 6000:
        	logger=open(self.logfilename,'a')
        	self.jsonoutput.close()
        	logger.write(time.strftime('%Y%m%d-%H%M%S')+" : file "+self.jsonfilename+" closed\n")
        	self.jsonfilename="jsondata/"+time.strftime('%d-%m')+"/"+self.fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + ".json"
        	self.jsondir=os.path.dirname(self.jsonfilename)
        	if not os.path.exists(self.jsondir):	os.makedirs(self.jsondir)
        	self.jsonoutput=open(self.jsonfilename,"w")
        	logger.write(time.strftime('%Y%m%d-%H%M%S')+" : file "+self.jsonfilename+" created\n")
        	logger.close()
        	self.counter = 0
        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        #sys.stderr.write('Error: ' + str(status_code) + "\n")
        logger=open("logfile.txt",'a')
        logger.write('Error: ' + str(status_code) + "\n")
        logger.close()
        return False

    def on_timeout(self):
        logger=open("logfile.txt",'a')
        logger.write("Timeout, sleeping for 60 seconds...\n")
        logger.close()
        #sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 
