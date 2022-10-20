import json
import jsonlines
from django.shortcuts import render
from django.http import JsonResponse
from .processess.viewsRendering import renderViews, saveResult
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# This is request handler which takes request and returns response 

@csrf_exempt
def say_hello(request):
	result = request.POST.get('htmlFraction', None)
	print("request post: ",dict(request.POST))
	stringRecordings = geRecordings()
	renderView = render(request, 'base_layout.html')
	if result != None:
		saveResult(dict(request.POST), request.POST.get('count'))
	if request.method == 'POST':
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
	return render(request, 'implemJS.html', {'susp':'sample_data/1309.2020_HTML.html'})

def sample_document_2(request):
	return render(request, 'base_layout.html')

def viewPag(request):
	return render(request, 'main_page.html', {'src':'mainMedia/sourceDoc.html',
		'susp':'mainMedia/suspiciousDoc.html'})
# Function for the views ends
