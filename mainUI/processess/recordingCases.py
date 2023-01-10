import re
import random
import jsonlines
from bs4 import BeautifulSoup
from random import randrange
from ..models import Annotations

def saveLastTwoRecordsPerman(obfuscInfo):
	"""
	Function for saving last two recording from source and suspicious
	to a permanent file.
	"""
	i = 0
	jsonDocinfo = {
	"suspDoc": {"suspDocName": None, "suspText": None,
					"suspMath": None, "suspImages": None,
					"suspDocHTML": None,
					"suspDocHTMLParent": None
					},
	"srcDoc": {"srcDocName": None, "srcText": None,
					"srcMath": None, "srcImages": None,
					"srcDocHTML": None,
					"srcDocHTMLParent": None
					},
	"casesReuse" : None,
	"colorHighlight": None	
	}
	recordings = {"suspDocstart": None, "suspDocend": None,
					"srcDocstart": None, "srcDocend": None,
					"obfuscation":None, "recordingType":None
					}
	sizeOfreader = 0  #To keep track of how many records are there in tempRecords
	sizeOfreaderAg = 0 #For assigning accurate record
	lastElement = 0 #We save last and secpnd last ele permanently so 
	secondlastElement = 0 #these two are to keep track of index
	with jsonlines.open('permanRecords.jsonl', mode='a') as writer:
		with jsonlines.open('tempRecords.jsonl') as reader:
			for ob1 in reader:
				sizeOfreader += 1
			lastElement = sizeOfreader - 1
			secondlastElement = sizeOfreader -2
		with jsonlines.open('tempRecords.jsonl') as reader:
			for obj in reader:
				sizeOfreaderAg += 1
				if i == 0:
					sizeOfreaderAg -= 1
					suspDocNametemp = obj["susp"]
					srcDocNametemp = obj["src"]
				if lastElement == sizeOfreaderAg or secondlastElement == sizeOfreaderAg:
					if i == 0:
						print("Skipped")
					else:
						if obj["count"][0] == "1":
							dictSusp = getdictCaseMisc("susp", obj)
							jsonDocinfo["suspDoc"]["suspDocName"] = suspDocNametemp
							if "Text" in obfuscInfo:
								jsonDocinfo["suspDoc"]["suspText"] = dictSusp["text"]   #obj["text"][0]
								recordings["suspDocstart"] = dictSusp["suspStart"]
								recordings["suspDocend"] = dictSusp["suspEnd"]
							if "Math" in obfuscInfo:
								jsonDocinfo["suspDoc"]["suspMath"] = dictSusp["math"]
							jsonDocinfo["suspDoc"]["suspImages"] = dictSusp["img"]
							jsonDocinfo["suspDoc"]["suspDocHTML"] = dictSusp["html"] #obj['htmlFraction'][0]
							jsonDocinfo["suspDoc"]["suspDocHTMLParent"] = dictSusp["htmlParent"] #obj['parentHTMLfraction'][0]
							jsonDocinfo["colorHighlight"] = dictSusp["color"] #obj['color'][0]
							if "InputObfusc" in obfuscInfo.keys() and len(obfuscInfo["InputObfusc"])>0:
								recordings["obfuscation"] = obfuscInfo["InputObfusc"] 
							else:
								recordings["obfuscation"] = obfuscInfo["obfuscType"]
							jsonDocinfo["casesReuse"] = recordings
							caseTyp = list()
							if "Text" in obfuscInfo:
								caseTyp.append("Text")
							if "Math" in obfuscInfo:
								caseTyp.append("Math")
							if "Image" in obfuscInfo:
								caseTyp.append("Image")
							recordings["recordingType"] = caseTyp
						if obj["count"][0] == "2":
							dictSrc = getdictCaseMisc("src", obj)
							jsonDocinfo["srcDoc"]["srcDocName"] = srcDocNametemp
							if "Math" in obfuscInfo:
								jsonDocinfo["srcDoc"]["srcMath"] = dictSrc["math"]
							jsonDocinfo["srcDoc"]["srcImages"] = dictSrc["img"]
							jsonDocinfo["srcDoc"]["srcDocHTML"] = dictSrc["html"] #obj['htmlFraction'][0]
							jsonDocinfo["srcDoc"]["srcDocHTMLParent"] = dictSrc["htmlParent"] #obj['parentHTMLfraction'][0]
							if "Text" in obfuscInfo:
								jsonDocinfo["srcDoc"]["srcText"] = dictSrc["text"]   #obj["text"][0]
								recordings["srcDocstart"] = dictSrc["srcStart"]
								recordings["srcDocend"] = dictSrc["srcEnd"]
							jsonDocinfo["casesReuse"] = recordings
				i += 1
		Annotations.objects.create(annotation=jsonDocinfo)
		writer.write(jsonDocinfo)


def getdictCaseMisc(docType, mainOPrcrd):
	"""
	Input:  docType= whether it is suspicious document or source
			mainOPrcrd = dict obtained from tempRecords.jsonl
	Output: "suspDict" = with all the elements required for suspicious document side
			"srcDict" = with all the elements required for source document side
	"""
	if docType == "susp":
		suspDict = dict()
		suspDict["text"] = mainOPrcrd["text"][0]
		suspDict["html"] = mainOPrcrd["htmlFraction"][0]
		suspDict["htmlParent"] = mainOPrcrd["parentHTMLfraction"][0]
		suspDict["color"] = mainOPrcrd["color"][0]
		subHTMLsoup = BeautifulSoup(mainOPrcrd["htmlFraction"][0],"html.parser")
		listOfmathIDs = list()
		for indtag in subHTMLsoup.find_all("math"):
			listOfmathIDs.append(indtag["id"])
			indtag.replaceWith("["+indtag["id"]+"]")	
		suspDict["math"] = listOfmathIDs
		listOfimgIDS = list()
		for indtag in subHTMLsoup.find_all("img"):
			listOfimgIDS.append(indtag["id"])
			indtag.replaceWith("["+indtag["id"]+"]")
		suspDict["img"] = listOfimgIDS
		texts = subHTMLsoup.findAll(text=True)
		standardText = u"".join(t for t in texts)
		standardText = standardText.replace("\n", ' ')
		standardText = re.sub('[^A-Za-z0-9 ]+', '', standardText)
		main_text = open("media/text/suspiciousDocText.txt", encoding="utf8").read()
		main_text = main_text.replace("\n", ' ')
		main_text = re.sub('[^A-Za-z0-9 ]+', '', main_text)
		matchesText = re.search(standardText, main_text)
		if matchesText:
			suspDict["suspStart"] = matchesText.span()[0]
			suspDict["suspEnd"] = matchesText.span()[1]
		else:
			suspDict["suspStart"] = "No accurate matches found"
			suspDict["suspEnd"] = "No accurate matches found"
		suspDict["obfuscation"] = "No obfuscation"
		return suspDict
	if docType == "src":
		srcDict = dict()
		srcDict["text"] = mainOPrcrd["text"][0]
		srcDict["html"] = mainOPrcrd["htmlFraction"][0]
		srcDict["htmlParent"] = mainOPrcrd["parentHTMLfraction"][0]
		subHTMLsoup = BeautifulSoup(mainOPrcrd["htmlFraction"][0],"html.parser")
		listOfmathIDs = list()
		for indtag in subHTMLsoup.find_all("math"):
			listOfmathIDs.append(indtag["id"])
			indtag.replaceWith("["+indtag["id"]+"]")
		srcDict["math"] = listOfmathIDs
		listOfimgIDS = list()
		for indtag in subHTMLsoup.find_all("img"):
			listOfimgIDS.append(indtag["id"])
			indtag.replaceWith("["+indtag["id"]+"]")
		srcDict["img"] = listOfimgIDS
		texts = subHTMLsoup.findAll(text=True)
		standardText = u"".join(t for t in texts)
		standardText = standardText.replace("\n", ' ')
		standardText = re.sub('[^A-Za-z0-9 ]+', '', standardText)
		main_text = open("media/text/sourceDocText.txt", encoding="utf8").read()
		main_text = main_text.replace("\n", ' ')
		main_text = re.sub('[^A-Za-z0-9 ]+', '', main_text)
		matchesText = re.search(standardText, main_text)
		if matchesText:
			srcDict["srcStart"] = matchesText.span()[0]
			srcDict["srcEnd"] = matchesText.span()[1]
		else:
			srcDict["srcStart"] = "No accurate matches found"
			srcDict["srcEnd"] = "No accurate matches found"
		return srcDict
