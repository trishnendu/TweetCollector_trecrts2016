import json

class Topics:
	
	def __init__(self, filename="TREC2015-MB-eval-topics.json"):
		self.infile=open(filename)
		self.jobject=json.loads(self.infile.read())
		self.topics={}
		for jo in self.jobject:
			self.topics[jo['topid']]=jo['title']
		
	def printtopics(self):
		for key in self.topics:
			print(key+" : "+self.topics[key])
			
			
if __name__ == '__main__':
	T=Topics()
	T.printtopics()  