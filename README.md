# TEIMMA-Reuse-Annotator
TE (Text) - IM(Image) - MA (Math) reuse annotator

```
Features.
1. Annotates text, math, images.
2. Documents extension: Currently = LaTex, (Internally: HTML, XML so ot can eventually take input in these formats)
3. Future extension: Allow direct PDFs, highlighting already similar text (to help user in finding plagiarism)
```

## Installation Instructions

1. `python3 -m venv mathPlagAnno` (More on creating [virtual environment](https://docs.python.org/3/library/venv.html))
2. `source mathPlagAnno/bin/activate` ([activate](https://docs.python.org/3/tutorial/venv.html#:~:text=Once%20you%E2%80%99ve%20created%20a%20virtual%20environment%2C%20you%20may%20activate%20it.) virtual environment)
3. `pip install -r requirements.txt` 
4. `Setup PostgressDatabase` 
5. `python manage.py runserver`
6. Open: http://localhost:8000/hellow/ in any browser.


## Annotation Procedure

1. Choose Suspicious document (left side upload) and Source document (right side upload) file with LateX source content. 
	1. File(s) with any other extension will throw an unknown error.
	2. Also, make sure you choose your source and suspicious files in the correct columns; otherwise, this will significantly record wrong cases.
2. After choosing both files from a local directory, click on the upload button.
	1. This might take a while as latex conversion to HTML5 is in the process using [LaTeXML](https://math.nist.gov/~BMiller/LaTeXML/).
	2. You can observe the progress on the terminal.
	3. Upon successful conversion, both documents will be shown on the main UI page. You can verify if the content is converted correctly and the source and suspicious documents are correct.
	4. The generated HTML5 files will be cached till the next upload overwrites. If you would like to upload the same suspicious and source files again, the UI select the same files, and cached HTML5 files will be used to display.
	4. You can also scroll into the individual documents to see further content
3. To start recording a plagiarism case, click on the `Start Recording` button and select a part of text from the Suspicious document first and then the source document.
	1. You will see that both the selected texts will be highlighted with the same background colour.
	2. If the colour is not assigned, please redo the selection by clicking on `Start Recording` again.
4. Select an option from `Type of case.`
	1. If not chosen, then `Text` will be selected as the default option.
	2. You can choose more than one box to indicate that you annotate with multi-type.
5. Select the appropriate `Obfuscation type` from the drop-down menu. If you think that the obfuscation present in the text does not match the available choice, then enter an appropriate option of yours in the block `Enter custom name`.
6. Finally, click on `Finish Recording` to save the recorded case. After this, the page will refresh, and your saved case will be shown again with the same asigned background colour.

## Additional Buttons

1. `View all recorded cases`: All documented cases will be viewed in a JSON format.
```
jsonDocinfo = {
	"suspDoc": {"suspDocName": None, "suspText": None,
					"suspMath": None, "suspDocHTML": None,
					"suspDocHTMLParent": None
					},
	"srcDoc": {"srcDocName": None, "srcText": None,
					"srcMath": None, "srcDocHTML": None,
					"srcDocHTMLParent": None
					},
	"casesPlag" : None,
	"colorHighlight": None	
	}
	recordings = {"suspDocstart": None, "suspDocend": None,
					"srcDocstart": None, "srcDocend": None,
					"obfuscation":None, "recordingType":None
					}
```
2. `Clear all recorded cases`: This will delete all recorded cases permanently; make sure you have taken a backup of previously recorded cases; otherwise, previously recorded cases will not be able to restore.
3. `Home`: clears the uploaded document and takes the user to the main UI.
4. `About`: About the development of the tool.  


