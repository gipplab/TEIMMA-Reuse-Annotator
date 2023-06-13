# TEIMMA-Reuse-Annotator
TEIMMA: The First Content Reuse Annotator for Text, Images, and Math

```
Features.
1. Annotates text, math, and images.
2. Visualization of existing similairity: Users can use any of the four algorithms to assist them in annotating the present similarity in a scientific document pair.
3. Input documents extension: Currently = LaTex, PDF, Plain text (.txt) (Internally: HTML). It also provides converting PDF to LaTeX for accurate access to math.
4. Annotations can be exported from the database (It uses: PostgreSQL)
5. It remembers if an already annotated document pair is uploaded again for annotations. Hence, allowing multiple, multiple suspicious-source or source-suspicious recordings.
```


## Installation Instructions

### virtual environment
`python3 -m venv mathReuseAnno` (More on creating [virtual environment](https://docs.python.org/3/library/venv.html))
`source mathReuseAnno/bin/activate` ([activate](https://docs.python.org/3/tutorial/venv.html#:~:text=Once%20you%E2%80%99ve%20created%20a%20virtual%20environment%2C%20you%20may%20activate%20it.) virtual environment)

### install dependencies
`pip install -r requirements.txt` 

### install LaTeXML
`sudo apt-get install latexml` (Additional [installation instructions](https://math.nist.gov/~BMiller/LaTeXML/get.html) if needed or for differrent operating systems)

### setup PostgreSQL database 
`python manage.py migrate` (can also be used without a database but recommended to have a database). If you want to use the app without a database refer to Dcoker Installation Section.

### start server
`python manage.py runserver`

### open following URL in a browser to start recording reuse cases
`http://localhost:8000/mainUI/`


## Docker

### pull image
`docker pull ankitsatpute/reuseanno:latest` (configuration with PostgreSQL)
`docker pull ankitsatpute/reuseanno:wthtdb` (configuration without PostgreSQL)

### build image from repo
`docker build -t reuseanno .`

### run web server
`docker run --publish 8000:8000 reuseanno` (remember to put /mainUI/ after 8000 if using with PostgreSQL else only 8000 suffices for viewing main UI)


## Annotation Procedure

1. Choose the suspicious document (left side upload) and Source document (right side upload) file with LateX source content. 
	1. File(s) with any other extension will throw an unknown error.
	2. Also, choose your source and suspicious files in the correct columns; otherwise, this will significantly record wrong cases.
2. Click the upload button after choosing both files from a local directory.
	1. This might take a while as latex conversion to HTML5 is in the process using [LaTeXML](https://math.nist.gov/~BMiller/LaTeXML/).
	2. You can observe the progress on the terminal.
	3. Upon successful conversion, both documents will be shown on the main UI page. You can verify if the content is converted correctly and if the source and suspicious documents are correct.
	4. The generated HTML5 files will be cached till the next upload overwrites. If you would like to upload the same suspicious and source files again, the UI selects the same files, and cached HTML5 files will be used to display.
	4. You can also scroll into the individual documents to see further content
3. To start recording a plagiarism case, click on the `Start Recording` button and select a part of the text from the suspicious document first and then the source document.
	1. You will see that both the selected texts will be highlighted with the same background colour.
	2. If the colour is not assigned, please redo the selection by clicking on `Start Recording` again.
4. Select an option from `Type of case.`
	1. If not chosen, `Text` will be selected as the default option.
	2. You can choose more than one box to indicate that you annotate with multi-type.
5. Select the appropriate `Obfuscation type` from the drop-down menu. If you think that the obfuscation in the text does not match the available choice, enter an appropriate option of yours in the block `Enter the custom name`.
6. Click `Finish Recording` to save the recorded case. After this, the page will refresh, and your saved case will be shown again with the same assigned background colour.

## Additional Buttons

1. `View all recorded cases`: All documented cases will be viewed in a JSON format.
```
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
	recordings = {"suspDocstart": None, "suspDocend": None,
					"srcDocstart": None, "srcDocend": None,
					"obfuscation":None, "recordingType":None
					}
	}
```
2. `Clear all recorded cases`: This will delete all recorded cases permanently; make sure you have taken a backup of previously recorded cases; otherwise, previously recorded cases will not be able to restore.
3. `Home`: clears the uploaded document and takes the user to the main UI.
4. `About`: About the development of the tool.  

## License

MIT
