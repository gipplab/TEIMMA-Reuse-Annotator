import os
import sys
import jsonlines
from bs4 import BeautifulSoup
from ..models import PlainText
from ..models import Math
from ..models import HTMLFiles
from django.conf import settings

def laTextoHTML(filename, docType):
	"""
	function to convert LaTex to HTML and also HTML to plain_text, math_equations.
	It uses parallelXML highlighting implementation jar to produce
	1. Plain text (with math IDs replacing MathML elements) 
	2. Math Elements: Separate file with mathID and their MathML content
	3. Output mappings (to keep track of from wehre the text is taken from)
	4. Output XML tags (saved XML tags)
	ToDo: We do not need 3 and 4, get rid of them from main implementation
	"""
	nameWithoutext = filename[:len(filename)-4]
	cmdLtxtoXML = "latexml --dest="+os.path.join(settings.MEDIA_ROOT, 
		"mainMedia",nameWithoutext)+".xml "+os.path.join(settings.MEDIA_ROOT, "mainMedia" ,filename)
	os.system(cmdLtxtoXML)
	cmdXMLtoHTML = "latexmlpost --format=xhtml --dest="+os.path.join(settings.MEDIA_ROOT, 
	"mainMedia", docType)+".html "+os.path.join(settings.MEDIA_ROOT, "mainMedia" ,nameWithoutext+".xml")
	os.system(cmdXMLtoHTML)
	# @Ankit Not running java jar from parallel XML as it does not gives correct output
	# cmdtoJarrun = "java -cp "+os.path.join(settings.MEDIA_ROOT,
	# 	"pds-xmlph-parent-0.0.1-SNAPSHOT.jar")+" org.sciplore.pds.TextFeatureProcess_extract "+os.path.join(settings.MEDIA_ROOT, 
	# 	"mainMedia" ,docType+".html")+" "+os.path.join(settings.MEDIA_ROOT, "text" 
	# 	,docType+"output_plain.txt")+" "+os.path.join(settings.MEDIA_ROOT, 
	# 	"math" ,docType+"output_math.txt")+" "+os.path.join(settings.MEDIA_ROOT, 
	# 	"text" ,docType+"output_mapping.txt")+" "+os.path.join(settings.MEDIA_ROOT, 
	# 	"text" ,docType+"output_xml_tags.txt")
	# print(cmdtoJarrun)
	# os.system(cmdtoJarrun)
	htmltoMathandTextFileWrite(docType, filename);


def htmltoMathandTextFileWrite(filename, fileStringName):
	"""
	To get all the math equations in a file
	"""
	file = os.path.join(settings.MEDIA_ROOT, "mainMedia", filename)+".html"
	soupHTML = BeautifulSoup(open(file, encoding="utf8").read(),"html.parser")
	#saving HTML data in PostgreSQL
	HTMLFiles.objects.create(filename=fileStringName,
		htmlfile=open(file, encoding="utf8").read())
	listOfmathjsons = list()
	#Creating list of dict (maID:content)
	for indtag in soupHTML.find_all("math"):
		dictMath = dict()
		dictMath[indtag["id"]] = str(indtag)
		listOfmathjsons.append(dictMath)
	#Writing mathequations to a JsonFile
	with jsonlines.open(os.path.join(settings.MEDIA_ROOT,"math",
		filename+"Math.jsonl"), mode='w') as writer:
		for item in listOfmathjsons:
			writer.write(item)
	Math.objects.create(filename=fileStringName,
		math=listOfmathjsons)
	#Replacing all math tags from main HTML with their IDS
	for indtag in soupHTML.find_all("math"):
		indtag.replaceWith("["+indtag["id"]+"]")
	#Saving all the text with IDS to a text file
	textFilePath = os.path.join(settings.MEDIA_ROOT,"text",filename+"Text.txt")
	#changed saving with the matches
	with open(textFilePath, "w", encoding="utf8") as textFile:
		textTags = soupHTML.findAll(text=True)
		#saving data of plaintext file to PostgreSQLDB
		PlainText.objects.create(filename=fileStringName,
			plaintext=u"".join(t for t in textTags))
		textFile.write(u"".join(t for t in textTags))