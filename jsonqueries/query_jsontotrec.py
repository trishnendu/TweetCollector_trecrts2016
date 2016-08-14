import os,sys,json

meditoutputfile="query_trec2106.txt"
outf=open(outputfile,'w')
	
cwd=os.getcwd()
for filename in os.listdir(cwd):
	if ".json" in filename:
		inputf=open(filename)
		data=inputf.read()
		jobjs=json.loads(data)
		for jo in jobjs:
			outf.write("<top>\n<num>"+jo['topid']+"</num>\n<title>"+jo['title']+
				"</title>\n<desc>"+jo['description']+"</desc>\n<narr>"+jo['narrative']+"</narr>\n</top>\n")
		inputf.close()
outf.close()			