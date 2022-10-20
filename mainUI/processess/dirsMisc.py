import os

#function to clear directories of existing files
def clearDIRsSuspSrc():
	#ToDo: Delete previous files both in case of suspicious and source doc
	#One immediate solution comes to the mind is add src abd susp dir in main media and adjust the settings
	os.remove(os.path.join(settings.MEDIA_ROOT))
	# if fSys.exists(docName):
	# 	os.remove(os.path.join(settings.MEDIA_ROOT, docName))
	# if fSys.exists(docName+".xml"):
	# 	os.remove(os.path.join(settings.MEDIA_ROOT, docName+".xml"))	
	# if fSys.exists(docName+".html"):
	# 	os.remove(os.path.join(settings.MEDIA_ROOT, docName+".html"))	