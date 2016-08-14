import os,json,string,re

class Push_Notification():

	def __init__(self,dirlocation="jsonqueries/"):
		self.titles={}
		for filename in os.listdir(dirlocation):
			#print("Opening file : "+filename)
			try:
				jobjects=json.loads(open(dirlocation+filename).read())
				for jo in jobjects:
					try:
						self.titles[jo['topid']]=jo['title']
					except	ValueError:
						print()	
			except	ValueError:
					print()
		#print(len(self.titles))	
	
	def similarity(self,standard,test):
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		S=set(regex.sub('',standard).split(" "))
		T=set(regex.sub('',test).split(" "))
		return float(len(S&T))/len(S)
		
	def relevanttopics(self,tweet):
		results=[]
		for q in self.titles:
			if self.similarity(self.titles[q],tweet)>0.5:
				results.append(q)
		return results
		
	def ifduplicate(self,topicid,tweet):
		try:
			topicfile=open("Submitted_tweet/"+topicid)
		except Exception as excp:
			return False
		data=topicfile.read().split("\n")		
		if len(data)<=1:
			return False
		for d in data:
			#print(str(self.similarity(d,tweet)))
			if self.similarity(d,tweet)>.5:
					return True
		return False
						
if __name__=='__main__':
	pn=Push_Notification()
	topics=pn.relevanttopics("I am not tired yet!")
	print(topics)
		
