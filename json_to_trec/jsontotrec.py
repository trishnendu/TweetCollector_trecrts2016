import json
infile=open("TREC2015-MB-eval-topics.json")
outfile=open("TREC2015-MB-eval-topics.trec",'w')
jsonobjects=json.loads(infile.read())
for jobject in jsonobjects:
	outfile.write("<top>\n<num>"+jobject['topid']+"</num>\n<title>"+
		jobject['title']+"</title>\n<desc>"+
		jobject['description']+"</desc>\n<narr>"+
		jobject['narrative']+"</narr>\n</top>\n\n")
outfile.close()
infile.close()