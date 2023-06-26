window.onload = function() {

let button = document.getElementById("compText");
const myCheckbox = document.getElementById("LCS");
const myCheckboxAda = document.getElementById("Adaptivesize");
const myCheckboxLCIS = document.getElementById("LCIS");
const myCheckboxGIT = document.getElementById("GIT");


myCheckboxGIT.addEventListener("change", function() {
   if (myCheckboxGIT.checked) {

    let inputValueGIT = document.getElementById("GITthre").value;
    let intValueGIT = parseInt(inputValueGIT)   ;

    if (intValueGIT > 29){

    // console.log('No range:',findSimilarAlphabets());
    changeMathTagColorL(intValueGIT, document.getElementById("left"), "red", findSimilarAlphabets());
    changeMathTagColorL(intValueGIT, document.getElementById("right"), "yellow", findSimilarAlphabets());
    }
  } else {
    console.log('No range:');
    location.reload();
  }
});


myCheckboxLCIS.addEventListener("change", function() {
   if (myCheckboxLCIS.checked) {

    let inputValueLCIS = document.getElementById("LCISthre").value;
    let intValueLCIS = parseInt(inputValueLCIS);

    if (intValueLCIS > 0){

    // console.log('No range:',findSimilarAlphabets());
    changeMathTagColorL(intValueLCIS, document.getElementById("left"), "red",findSimilarAlphabets());
    changeMathTagColorL(intValueLCIS, document.getElementById("right"), "yellow",findSimilarAlphabets());
    }
  } else {
    console.log('No range:');
    location.reload();
  }
});


myCheckboxAda.addEventListener("change", function() {
   if (myCheckboxAda.checked) {

    let inputValuea = document.getElementById("Adaptivesizethre").value;
    let intValuea = parseInt(inputValuea);

    // Requirement of Adaplag algo due to parameter settings
    if (intValuea > 20){
    let text1 = document.getElementById("left").textContent;
    let text2 = document.getElementById("right").textContent;

    let similarTokens = getSimilarTextTokens(text1,text2,intValuea);

    // console.log("tokens: ",similarTokens);

    highlightMatchedSubstrings(similarTokens, "left");
    highlightMatchedSubstrings(similarTokens, "right");

    }

  } else {
    console.log('No range:');
    location.reload();
  }
});


myCheckbox.addEventListener("change", function() {
   if (myCheckbox.checked) {

    let inputValue = document.getElementById("LCSthreashold").value;
    let intValue = parseInt(inputValue);

    if (intValue > 2){

    let text1 = document.getElementById("left").textContent;
    let text2 = document.getElementById("right").textContent;

    let similarTokens = getSimilarTextTokens(text1,text2,intValue);

    console.log("similar tokens from LCIS: ",similarTokens);

    highlightMatchedSubstrings(similarTokens, "left");
    highlightMatchedSubstrings(similarTokens, "right");
    }
  } else {
    console.log('No range:');
    location.reload();
  }
});
}


function searcH(ele) {
    if(event.key === 'Enter') {
        const myCheckbox = document.getElementById("LCS");
        const myCheckboxAda = document.getElementById("Adaptivesize");
        const myCheckboxLCIS = document.getElementById("LCIS");
        const myCheckboxGIT = document.getElementById("GIT");
        if (myCheckbox.checked || myCheckboxAda.checked || myCheckboxLCIS.checked || myCheckboxGIT.checked) {
            alert('Please re-run the algorithm by re-selecting the checkbox after entering new parameters.');
        } else {            
        alert('Please select an algorithm checkbox');     
        }
    }
}


function getSimilarTextTokens(text1, text2, n) {
  let tokens1 = text1.split(" ");
  let tokens2 = text2.split(" ");
  let similarTokens = [];

  for (let i = 0; i < tokens1.length; i++) {
    for (let j = 0; j < tokens2.length; j++) {
      if (tokens1[i].match(/^[a-z]+$/i) && tokens2[j].match(/^[a-z]+$/i)) {
        if (tokens1[i] === tokens2[j]) {
          let count = 1;
          let k = i + 1;
          let l = j + 1;
          while (k < tokens1.length && l < tokens2.length &&
                 tokens1[k].match(/^[a-z]+$/i) && tokens2[l].match(/^[a-z]+$/i) &&
                 tokens1[k] === tokens2[l]) {
            count++;
            k++;
            l++;
          }
          if (count >= n) {
            similarTokens.push(tokens1.slice(i, i + count).join(" "));
            i = k - 1;
            j = l - 1;
          }
        }
      }
    }
  }
  return similarTokens;
}


function findSimilarAlphabets() {
  const mathTags = document.getElementsByTagName("math");
  const similarAlphabets = [];

  for (let i = 0; i < mathTags.length; i++) {
    const textContent = mathTags[i].textContent;
    const filteredTextContent = textContent.replace(/[^a-zA-Z]/g, '');
    // const filteredTextContent = textContent;

    for (let j = 0; j < filteredTextContent.length; j++) {
      const alphabet = filteredTextContent.charAt(j);
      if (filteredTextContent.indexOf(alphabet, j + 1) !== -1) {
        if (!similarAlphabets.includes(alphabet)) {
          similarAlphabets.push(alphabet);
        }
      }
    }
  }
  return similarAlphabets;
}


function changeMathTagColorL(lenThre, elementHere, color, similarEls) {
  const mathTags =   elementHere.getElementsByTagName("math");

  let i1 = 0;
  let colorH = ["red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink"]


  for (let i = 0; i < mathTags.length; i++) {   
    if (mathTags[i].textContent.length >= lenThre) {
      var tagTr = false;
      indivSplitted = mathTags[i].textContent.split("");
      for (let n = 0; n < indivSplitted.length; n++) {
        for (let o = 0; o < similarEls.length; o++) {
                    if (similarEls[o] != indivSplitted[n]) {
                    tagTr = true;
              }
        }
      }
      if (tagTr){
        i1 = i1 + 1;
        if (i1 > 35){
        i1 = 0;
        }
        mathTags[i].style.color = colorH[i1];
      }
    }
  }
}

function getTextNodesIn(node) {
  var textNodes = [];
  if (node.nodeType == 3) {
    textNodes.push(node);
  } else {
    for (var i = 0; i < node.childNodes.length; i++) {
      textNodes = textNodes.concat(getTextNodesIn(node.childNodes[i]));
    }
  }
  return textNodes;
}


function changeMathTagColor(alphabetList, color) {
  const mathTags = document.getElementsByTagName("math");
  for (let i = 0; i < mathTags.length; i++) {
    const textContent = mathTags[i].textContent;
    const filteredTextContent = textContent;
    console.log('filteredTextContent ',textContent);
    for (let j = 0; j < filteredTextContent.length; j++) {
      const alphabet = filteredTextContent.charAt(j);
      console.log('alphabet ',alphabet);
    }
  }
}

function highlightMatchedSubstrings(substrings, htmlElementId) {
  const element = document.getElementById(htmlElementId);
  let html = element.innerHTML;
  let i1 = 0;
  let colorH = ["red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink",
    "red","blue","green","orange","purple","yellow","white","pink"]

  for (const substring of substrings) {
    let index = html.indexOf(substring);
    while (index !== -1) {
      let before = html.slice(0, index);
      i1 = i1 + 1;
      if (i1 > 35){
        i1 = 0;
      }
      let after = html.slice(index + substring.length);
      html = before + "<span style='color: "+colorH[i1]+"'>" + substring + "</span>" + after;
      index = html.indexOf(substring, index + substring.length + 37);
    }
  }
  element.innerHTML = html;
}


var countN = 0;
var colorSave = null;
var clickCount = 0;

function textSelection(selectionCount) {
  if (clickCount < 2) {
  if (selectionCount >= 2) {
    countN = 0;
    return
  }
  if (countN === 0) {
    colorSave = getRandomColor();
  }
  countN = countN + 1;  
  var range = window.getSelection().getRangeAt(0);
  console.log('Okay selection executaed...');
  var selectionContents = range.extractContents();
  var div = document.createElement("div");
  div.style.backgroundColor = colorSave;
  div.appendChild(selectionContents);
  range.insertNode(div);
  clickCount++;

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
        },
        failure: function () {
        }
    });
  return
}
}


function renderCases(getRcrd) {
    console.log('records: ',getRcrd);
    /* 
    Lets pass the markings as a variable which is obtaibned through rendering requests.
    No get json file directly to javascript
    */
    console.log('Ready to render recorded offsets '); 
    for (var j=0; j < getRcrd.length; j++) {
        var docCreate = new DOMParser().parseFromString(getRcrd[j].parentHTMLfraction[0],'text/html');
            var classNamelocal = docCreate.all[3].className
            if (classNamelocal) {
                let listEle = document.getElementsByClassName(classNamelocal);
                for (var i=0; i < listEle.length; i++) {
                    if (listEle[i].textContent == docCreate.activeElement.textContent) {
                        listEle[i].outerHTML = docCreate.activeElement.outerHTML;
                    }
                }
            }
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