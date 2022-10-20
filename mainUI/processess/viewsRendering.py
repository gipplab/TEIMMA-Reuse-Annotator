import os
import json
import jsonlines
from django.conf import settings
from django.shortcuts import render
from .latexTohtml import laTextoHTML
from django.core.files.storage import FileSystemStorage
from .recordingCases import saveLastTwoRecordsPerman

def renderViews(request, stringRecordings):
	doc_names = {}
	renderView = render(request, 'base_layout.html')
	if request.POST.get('uploadFiles') == 'uploadFiles':
		delete_All_record()
		if 'suspiciousDoc' in request.FILES.keys():
			susp_doc_tex = request.FILES['suspiciousDoc']
			src_doc_tex = request.FILES['sourceDoc']
			suspDocName = request.FILES['suspiciousDoc'].name 
			srcDocName = request.FILES['sourceDoc'].name
			filesys = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, "mainMedia"))
			if not filesys.exists(suspDocName):
				#clearDIRsSuspSrc()
				filesys.save(suspDocName, susp_doc_tex)
				laTextoHTML(suspDocName, "suspiciousDoc")
			if not filesys.exists(srcDocName):
				#clearDIRsSuspSrc(srcDocName, filesys)
				filesys.save(srcDocName, src_doc_tex)
				laTextoHTML(srcDocName, "sourceDoc")
			doc_names["src"] = srcDocName
			doc_names["susp"] = suspDocName
			saveResult(doc_names,0)
			renderView = render(request, 'sample_text/src_susp_doc_view.html', 
					{'susp':"mainMedia/suspiciousDoc.html", 
					'src':"mainMedia/sourceDoc.html", 
					'startRecording':False, 'countRef':0, 
					'prevRecordings':stringRecordings})
		else:
			renderView = render(request, 'error_File.html')
	if request.POST.get('startRecording') == 'startRecording':
		renderView = render(request, 'sample_text/src_susp_doc_view.html', 
				{'susp':"mainMedia/suspiciousDoc.html", 
				'src':"mainMedia/sourceDoc.html",
				'startRecording':True, 'countRef':0,
				'prevRecordings':stringRecordings})
	if request.POST.get('newRecording') == 'newRecording':
		delete_last_record()
		renderView = render(request, 'sample_text/src_susp_doc_view.html', 
				{'susp':"mainMedia/suspiciousDoc.html", 
				'src':"mainMedia/sourceDoc.html",
				'startRecording':True, 'countRef':0,
				'prevRecordings':geRecordings()})
	if request.POST.get('finishRecording') == 'finishRecording':
		print("Value from the box: ", request.POST)
		obfuscInformation = request.POST
		saveLastTwoRecordsPerman(obfuscInformation);
		renderView = render(request, 'sample_text/src_susp_doc_view.html', 
				{'susp':"mainMedia/suspiciousDoc.html", 
				'src':"mainMedia/sourceDoc.html", 
				'startRecording':True, 'countRef':2,
				'prevRecordings':stringRecordings})

	if request.POST.get('viewAll') == 'viewAll':
		print("Viewing all records")
		renderView = render(request, 'sample_text/view_all_recorded.html',
			{'allCases':getAllrecordings()})

	if request.POST.get('clearAllRecording') == 'clearAllRecording':
		delete_All_record()
		renderView = render(request, 'sample_text/src_susp_doc_view.html', 
				{'susp':"mainMedia/suspiciousDoc.html", 
				'src':"mainMedia/sourceDoc.html", 
				'startRecording':True, 'countRef':0,
				'prevRecordings':[]})
	return renderView


def getAllrecordings():
	"""
	Return all permanently recorded cases as JSON view.
	if the permanently recorded cases are 0 then returns null.
	"""
	listRecords = []
	with jsonlines.open('permanRecords.jsonl', mode='r') as reader:
		for obj in reader:
			#print(obj['SuspiciousDocName'])
			listRecords.append(obj)
	return json.dumps(listRecords,indent=4)

def saveResult(resultHere, intI):
	"""
	Takes Json result(resultHere) from ajax Query and save it to the JsonlinesFile.
	intI: is to keep track whether a new file recording is started or not.
	"""
	intJ = 0
	if intI == 0:
		with jsonlines.open('tempRecords.jsonl', mode='w') as writer:
			writer.write(resultHere)		
	elif intI == -2:
		with jsonlines.open('tempRecords.jsonl', mode='w') as writer:
			intJ += 1
	else:
		with jsonlines.open('tempRecords.jsonl', mode='a') as writer:
			writer.write(resultHere)


def delete_last_record():
	"""
	In case annotation is stopped in the middle, this fucntion will allow to
	clear falsely recorded annotation.
	Currently: Delete last record option, you should be able to see that record 
	that has been deleted has no background color. 
	"""
	newRcrds = list()
	with jsonlines.open('tempRecords.jsonl', mode='r') as readerOp:
		for obj in readerOp:
			newRcrds.append(obj)
	with jsonlines.open('tempRecords.jsonl', mode='w') as writerOp:
		for obji in newRcrds[:len(newRcrds)-1]:
			writerOp.write(obji)


def geRecordings():
	listRecordings = []
	i = 0
	with jsonlines.open('tempRecords.jsonl', mode='r') as reader:
		for obj in reader:
			if i != 0:
				listRecordings.append(obj)
			i+=1
	return str(listRecordings)


def delete_All_record():
	"""
	Deleting all the records. For the "tempRecords" it is eesential to save
	Firt line to keep track of names of src and susp docs
	"""
	with jsonlines.open('permanRecords.jsonl', mode='w') as writer:
		print("All permanent records deleted")
	with jsonlines.open('tempRecords.jsonl', mode='r') as reader:
		for obj in reader:
			with jsonlines.open('tempRecords.jsonl', mode='w') as writerOP:
				writerOP.write(obj)
			break
			print("All trmporary records deleted")