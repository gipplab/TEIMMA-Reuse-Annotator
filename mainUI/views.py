import os
import json
import jsonlines
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .processess.viewsRendering import renderViews, saveResult
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from .models import Pair

def save_pair(request):
	if request.method == 'POST':
		filename1 = request.POST.get('filename1')
		filename2 = request.POST.get('filename2')
		print("Here are the post parameters: ", filename2, filename1)
		case_type = request.POST.get('case_type')
		case_function = request.POST.get('case_function')
		comments = request.POST.get('comments')
		feedback = request.POST.get('feedback')

		pair = Pair(
			filename1=filename1,
			filename2=filename2,
			case_type=case_type,
			case_function=case_function,
			comments=comments,
			feedback=feedback
		)
		pair.save()

		redirect_path = reverse('pair_detail', args=[filename1, filename2])

		return redirect_path  # Redirect to the desired page after saving

	return redirect_path  # Redirect to the desired page if the request method is not POST


def download_file(request):
    file_path = settings.MEDIA_ROOT + '/mainMedia/permanRecords.jsonl'
    file_storage = FileSystemStorage()
    file = file_storage.open(file_path)
    response = FileResponse(file, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file_path}'
    return response

def pair_detail_view(request, file_name1, file_name2):
	selected_pairs = []

	file_pairs = request.session.get('file_pairs', [])
	# Iterate over the file_pairs to find the matching pair
	for pair in file_pairs:
		if pair['fileName1'] == file_name1 and pair['fileName2'] == file_name2:
			selected_pairs = pair['html_pairs']
			break
	return render(request, 'annotFeedback/pair_detail.html', {'selected_pairs': selected_pairs})

def feednackanno(request):
	file_pairs = []
	jsonLines_filPath = 'annotations_withIDs.jsonl'

	unique_pairs = set()
	file_data = {} 

	with jsonlines.open(jsonLines_filPath) as reader:
		for line in reader:
			pair_key = (line["suspDoc"]["suspDocName"], line["srcDoc"]["srcDocName"])
			unique_pairs.add(pair_key)

			if pair_key not in file_data:
				file_data[pair_key] = []

			if "casesReuse" in line.keys():
				file_data[pair_key].append((line["suspDoc"]['suspDocHTML'], line["srcDoc"]['srcDocHTML'], 
					str(line["casesReuse"]["recordingType"]),
					line["casesReuse"]["obfuscation"],
					line["ID_nr"]))
				# caseType[str(line["casesReuse"]["recordingType"])] += 1
				# obfuscation[line["casesReuse"]["obfuscation"]] += 1
			elif "casesPlag" in line.keys():
				file_data[pair_key].append((line["suspDoc"]['suspDocHTML'], line["srcDoc"]['srcDocHTML'], 
					str(str(line["casesPlag"]["recordingType"])),
					line["casesPlag"]["obfuscation"],
					line["ID_nr"]))
				# caseType[str(line["casesPlag"]["recordingType"])] += 1
				# obfuscation[line["casesPlag"]["obfuscation"]] += 1

			# file_data[pair_key].append((line["suspDoc"]['suspDocHTML'], line["srcDoc"]['srcDocHTML']))

	for pair_key in unique_pairs:
		file_pairs.append({
			'fileName1': pair_key[0],
			'fileName2': pair_key[1],
			'html_pairs': file_data[pair_key]
        })

	# Store the file_pairs list in the session
	request.session['file_pairs'] = file_pairs

    # return render(request, 'file_pairs.html', {'file_pairs': file_pairs})
	return render(request, 'reviewAnnotations.html', {'file_pairs': file_pairs})

@csrf_exempt
def say_hello(request):
	result = request.POST.get('htmlFraction', None)
	print("request post: ",dict(request.POST))
	stringRecordings = geRecordings()
	# renderView = render(request, 'base_layout.html')
	if result != None:
		saveResult(dict(request.POST), request.POST.get('count'))
	# if request.method == 'POST':
	renderView = renderViews(request, stringRecordings)
	return renderView

def getJson(request):
	listRecords = []
	with jsonlines.open('tempRecords.jsonl', mode='r') as reader:
		for obj in reader:
			#print(obj['SuspiciousDocName'])
			listRecords.append(obj)
			#break
		#json.dumps(listRecords,indent=4)
	return JsonResponse(obj)


def geRecordings():
	listRecordings = []
	i = 0
	with jsonlines.open('tempRecords.jsonl', mode='r') as reader:
		for obj in reader:
			if i != 0:
				listRecordings.append(obj)
			i+=1
	return str(listRecordings)

def drawing(request):
    user = request.user

    url = request.POST.get('url') # url from ajax will be saved here.
    first_value = next(iter(((request.POST).dict()).values())) # cleaning output
    
    with open("media/{}/dict.json".format(user), 'w') as draw:
        draw.write(first_value) # save to file

    return JsonResponse(url, safe=False)


def getCharacterOffsets(request):
    result = request.GET.get('htmlFraction', None)
    # Any process that you want
    #print(request.GET)
    data = {}
    return JsonResponse(data)


def getInitialData(request):
	result = request.GET.get('title')
	print(request.GET)
	data = {}
	#return JsonResponse({'text': 'I am here with JsonRespons now'})
	return JsonResponse(data)


# Function for the views starts
def sample_document(request):
	return render(request, 'aboutSite.html')

def sample_document_2(request):
	return render(request, 'base_layout.html')

def viewPag(request):
	return render(request, 'main_page.html', {'src':'mainMedia/sourceDoc.html',
		'susp':'mainMedia/suspiciousDoc.html'})
# Function for the views ends
