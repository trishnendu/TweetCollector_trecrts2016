import os,json,string,re,math

class Push_Notification():
	def __init__(self,dirlocation="jsonqueries/"):
		self.titles={}
		self.titlebag={}
		self.desc={}
		self.idf={}
		self.numberofquery=0
		self.keywords={}
		self.stopwords=set()
		self.keywords={}
		
		stopwordfile=open("smart-stopwords",'r')
		for d in stopwordfile.read().split("\n"):
			self.stopwords.add(d)
			
		for filename in os.listdir(dirlocation):
			try:
				jobjects=json.loads(open(dirlocation+filename).read())
				for jo in jobjects:
					self.numberofquery+=1
					try:
						self.titles[jo['topid']]=jo['title']
						regex = re.compile('[%s]' % re.escape(string.punctuation))
						terms=set(regex.sub('',jo['title']).lower().split(" "))-self.stopwords
						self.titlebag[jo['topid']]={}
						for term in terms:
							term=str(term).lower();
							occurence=str(regex.sub('',jo['title'])).lower().count(term)
							if term in self.titlebag:	self.titlebag[term]+=occurence
							else:	self.titlebag[jo['topid']][term]=occurence
							
						self.desc[jo['topid']]=jo['description']
						regex = re.compile('[%s]' % re.escape(string.punctuation))
						terms=set(regex.sub('',jo['description']).lower().split(" "))-self.stopwords
						for term in terms:
							term=str(term).lower();
							occurence=str(regex.sub('',jo['description'])).lower().count(term)
							if term in self.titlebag:	self.titlebag[term]+=occurence
							else:	self.titlebag[jo['topid']][term]=occurence
							
						for term in self.titlebag[jo['topid']]:
							if term in self.idf:	self.idf[term]+=1
							else:	self.idf[term]=1
							
					except	ValueError:
						print()
						
			except	ValueError:
				print()
		
		outfile=open("query_model2016tfidf",'w')
		for key in self.titlebag:
			self.keywords[key]=set()
			l={}
			termlist=[]
			#print("Topic: "+key)
				
			for term in self.titlebag[key]:
				tfidf=round(float(1+math.log(self.titlebag[key][term]))*float(math.log(1+self.numberofquery/self.idf[term])),2)
				if tfidf>1:
					if tfidf in l:
						l[tfidf].append(term)
						termlist.append(term)
					else:
						l[tfidf]=[term]
						termlist.append(term)
			
			outfile.write("<top>\n<num>"+key+"</num>\n<title>"+self.titles[key]+"</title>\n<priorterms>"+str(termlist)+"</priorterms>\n<qmodel>")
			for terms in termlist:
				outfile.write("TEXT:"+terms+" ")
			outfile.write("</qmodel>\n</top>\n")
			#print("Topic: "+key)
			for k in sorted(l):
				print((l[k],k))
			print("\n ")
		outfile.close()
					#if tfidf>1:
					#	self.keywords[key].add(term)

	'''	total={}
		for key in self.titlebag:
			for term in self.titlebag[key]:
				if term in total:
					total[term]+=self.titlebag[key][term]
				else:
					total[term]=self.titlebag[key][term]
		total=sorted(total.items(),key=lambda x:x[1],reverse=True)
		for k in total:
			print(k)'''
				
	def similarity(self,standardset,test):
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		T=set(regex.sub('',test.lower()).split(" "))-self.stopwords
		if len(standardset)!=0:	return float(len(standardset&T))/len(standardset)
		else:	return 1
			
	def relevanttopics(self,tweet):
		results=[]
		for q in self.titles:
			if self.similarity(self.keywords[q],tweet)>0.6:
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
			if self.similarity(d,tweet)>0.6:
					return True
		return False
						
if __name__=='__main__':
	pn=Push_Notification()
	#topics=pn.relevanttopics("current united world war sentiment states atomic")
	#print(topics)
