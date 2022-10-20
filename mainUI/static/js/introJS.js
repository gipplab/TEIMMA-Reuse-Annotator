var countN = 0;
var colorSave = null;

function textSelection(selectionCount) {
  if (selectionCount >= 2) {
  	countN = 0;
  	return
  }
  if (countN === 0) {
	colorSave = getRandomColor();
  }
  countN = countN + 1;  

  // var text = "";
  // var textOuter= "";
  // var sel = window.getSelection();

  // console.log('rangeCount:',sel.anchorNode);

  // var range = sel.getRangeAt(0).cloneRange();

  var range = window.getSelection().getRangeAt(0);
  var selectionContents = range.extractContents();
  var div = document.createElement("div");
  div.style.backgroundColor = colorSave;
  div.appendChild(selectionContents);
  range.insertNode(div);

  //console.log('div :',div);

  // //const cloneDeep = require(['lodash.clonedeep'])
  // //const rangeSave = JSON.parse(JSON.stringify(range))
  // //rangeSave = String(range);

  // var markerTextChar = range.extractContents();

  // var markerEl, markerId = "sel_" + new Date().getTime() + "_" + Math.random().toString().substr(2);
  // markerEl = document.createElement("span");

  // markerEl.id = markerId;

  // markerEl.appendChild(markerTextChar);

  // range.insertNode(markerEl);

  // markerEl.style.backgroundColor = colorSave;
  // markerEl.style.cursor = 'pointer';

  // //text = window.getSelection().toString();
  // //Filhal we stick to innerHTML (tip: outerHTML also works)
  // // but we are not sure if this is sufficient to highlight the text again 
  // // COME BACK LATER HERE IF RE-HIGHLIGHTING SPAN IS NOT ACEIVABLE
  // text = markerEl.outerHTML;

  // textOuter = markerEl.parentElement.outerHTML;

  // //console.log('selected text outerHTML: ',markerEl.parentElement.outerHTML);   
  // //console.log('main Html of selected text?: ',textOuter);   
  // console.log('markerTextChar: ',markerTextChar);

  $.ajax({
        type: "POST",
        url: '/mainUI/',
        data: {
        	"parentHTMLfraction":div.parentElement.outerHTML,
            "htmlFraction": div.innerHTML,
            "text": div.innerText,
            "count": countN,
            "color":colorSave,
            "csrfmiddlewaretoken": "{{ csrf_token }}"
        },
        dataType: "json",
        success: function (data) {
            // any process in data
            alert("successfull")
        },
        failure: function () {
            alert("failure");
        }
    });
  return
}


function renderCases(getRcrd) {
	console.log('records: ',getRcrd);
	/* 
	Lets pass the markings as a variable which is obtaibned through rendering requests.
	No get json file directly to javascript
	*/

	//require(['./jsonlViewsample.json'], function (jsonK) {});
	//var json = require('/tempRecords.jsonl');

	console.log('Ready to render recorded offsets ');
	//console.log('Document ID: ',document.getElementsByClassName("ltx_contact ltx_role_address"));	
 
	for (var j=0; j < getRcrd.length; j++) {
		var docCreate = new DOMParser().parseFromString(getRcrd[j].parentHTMLfraction[0],'text/html');
		//console.log("createddoc",docCreate);
		//console.log("createddoc",docCreate.all[3].className);
		//break;
		//var className = docCreate.activeElement.className;
		//for (var k=0; k < docCreate.all.length; k++) {
			var classNamelocal = docCreate.all[3].className
			if (classNamelocal) {
				let listEle = document.getElementsByClassName(classNamelocal);
				//console.log("classNamelocal",classNamelocal)
				for (var i=0; i < listEle.length; i++) {
					//console.log();
					if (listEle[i].textContent == docCreate.activeElement.textContent) {
						// console.log("From current view",docCreate.all[k].textContent);
						// console.log("From saved view",listEle[i].textContent);
  				// 		console.log("Matched found oky ");
  						// console.log("outer HTML old: ",docCreate.lastChild.outerHTML);
  						listEle[i].outerHTML = docCreate.activeElement.outerHTML;
  					}
				}
			}
		//}
		//break;
		//Following three are working correctly
		// console.log("From saved view",docCreate.all);
		// console.log("From saved view",docCreate.all[0].className);
		// console.log("Got these class names",docCreate.activeElement.className);
		//console.log("From current view",getRcrd[j].result[0])
		//break;
		//console.log("docCreate: ",docCreate.activeElement.className);
	}	
	return
}

function getRandomColor() {
    var letters = 'BCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * letters.length)];
    }
    return color;
}

function renderCasesPro() {

	// let urlResponse = new URL("http://localhost:8000/api/getJson");
	// console.log("Returned cases", urlResponse.searchParams.get("src"));

	//console.log("data here:", data);

	  $.ajax({
        type: "POST",
        url: 'api/getJson',
        dataType: "json",
        success: function () {
            // any process in data
            alert("successfull")
        },
        failure: function () {
            alert("failure");
        }
    });
}