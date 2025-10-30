let total;
let inputJSON;
let txt;
const hasMultiplierLabels = false;

//

//This variable is the multiplier for parts of the game that increase based on difficulty
let difficultyMultiplier = 1;
const difficultyMultiplierLevels = [1,1.5,2];
let scoreMultipliers = [];





function init(){
    document.getElementById("codeDisplay").innerHTML = "Field Code: " + localStorage.getItem("code");
    
    document.getElementById("matchNum").value = localStorage.getItem("match#");
    
    //Update the multiplier arrays  and elements
    //updateScoreMultipliers();
    //updateMultiplierLabels();
    fetchJSONData();
    fetchTeams()
    
    
    
    //Set a timer to calculate the score every 500ms
    setInterval(calculateScores, 500);
    
    //Add event listener to update the team when the match is changed
    //document.getElementById('matchNumber').addEventListener('change', updateTeam);
    
}

function fetchJSONData() {
    
    fetch("./inputs.json")
    .then(response => {
        if (!response.ok){
            throw new Error("Failed to read JSON file")
        }
        return response.json();
    })
    .then(data => {
        addInputs(data);

    })
    .catch((error) => {
        console.log(error);
    })

}

function fetchTeams() {
    url = "./teams.txt";
    fetch(url)
    .then(response => {
        if (!response.ok){
            throw new Error("Failed to read text file")
        }
        return response.text();
    })
    .then(data => {
        processTxt(data);
    })
    .catch((error) => {
        console.log('Error fetching Txt file:', error);
    })
}

function processTxt(theTxt)
{
    txt = theTxt.split("\n");
    for(let team of txt){
        console.log(team);
    }
    
    teams = document.getElementById("teamDisplay");
    for (team of txt){
        let option = document.createElement("option");
        option.innerText = team;
        teams.appendChild(option);
    }
}

//Defunct function
/*
function updateTeam()
{
    let output = document.getElementById('teamDisplay');
    let match = document.getElementById('matchNum');
    match = parseInt(match.value);
    field = localStorage.getItem("fieldColor");
    console.log(field + " match " + match);
    try {
        team = txt[match-1][field];
    }
    catch (error){
        team = "Out of bounds"
        console.log(error);
    }

    output.innerHTML = team;
    
    
}*/

function addInputs(jsonObj){
    //Get the keys from the json object
    const keys = Object.keys(jsonObj);
    
    //Loop through every key
    for (key of keys){
        //Get the input object
        let input = jsonObj[key];
        let name = key;
        //Read all the data from the obj and store in variables
        //let name = input["name"];
        let type = input["type"];
        let options = input["options"];
        let maxInput = input["maxInput"];
        let pointValue = input["pointValue"];
        let isMultiplied = input["multiplied"];
        let lineBreak = input["lineBreak"];
        let column = input["column"];
        let div;
        if(column == "left"){
            div = "left"
        }else if(column == "right"){
            div = "right";
        }else{
            console.log("Invalid column name");
        }
        
        if(type == "number"){
            addInput("number", name, pointValue, lineBreak,isMultiplied,div,maxInput, "");
        }else if(type == "dropdown"){
            addInput("dropdown", name, pointValue, lineBreak, isMultiplied,div, 10000, options);
        }else if(type == "checkbox"){
            addInput("checkbox", name, pointValue, lineBreak, isMultiplied, div, 1000, "");
        }else{
            console.log("Invalid input type: " + input);
        }
    }
}

function addInput(objectType, name, pointValue, newLine, isMultiplied, column, theMaxInput, theOptions){
    let inputDiv = document.getElementById(column);
    let container = document.createElement("div");
    container.setAttribute("class","container");

    //Label
    let label = document.createElement("label");
    label.innerText = name + ": ";
    //container.appendChild(label);
    addFlexDivAroundElement(container, label);

    //Create the input
    if(objectType == "number"){
        //Deincrement button
        let minus = document.createElement("button");
        minus.setAttribute("class","incrementbutton");
        minus.onclick = function(){deincrement(name);};
        minus.innerText = "-";
        //container.appendChild(minus);
        addFlexDivAroundElement(container, minus);

        //Number input
        let input = document.createElement("input");
        input.setAttribute("class","sum");
        input.setAttribute("id",name);

        //Store variables in the element
        input.setAttribute("data-max", theMaxInput);
        input.setAttribute("data-pointvalue", pointValue);
        input.setAttribute("data-ismultiplied", isMultiplied);

        input.value = 0;
        input.type = "number";
        //container.appendChild(input);
        addFlexDivAroundElement(container, input);

        //Increment button
        let add = document.createElement("button");
        add.setAttribute("class","incrementbutton");
        //minus.addEventListener("click", deincrement);
        add.onclick = function(){increment(name);};
        add.innerText = "+"
        //container.appendChild(add);
        addFlexDivAroundElement(container, add);
    }else if(objectType == "dropdown"){
        //Dropdown input
        let input = document.createElement("select");
        input.setAttribute("class","Dropdown sum");

        //Store variables in the element
        input.setAttribute("data-pointvalue", pointValue);
        input.setAttribute("data-ismultiplied", isMultiplied);

        input.setAttribute("id",name);

        //Add options
        options = theOptions.split(",");
        for (value of options){
            let option = document.createElement("option");
            option.innerText = value;
            input.appendChild(option);
        }
        input.setAttribute("id",name);
        //container.appendChild(input);
        addFlexDivAroundElement(container, input);
    }else if(objectType == "checkbox"){
        //Checkbox input
        let input = document.createElement("input");
        input.setAttribute("class","CheckBox sum");
        input.setAttribute("id",name);
        
        //Store variables in the element
        input.setAttribute("data-pointvalue", pointValue);
        input.setAttribute("data-ismultiplied", isMultiplied);
        
        input.type = "checkbox";
        //container.appendChild(input);
        addFlexDivAroundElement(container, input);
    }else{
        console.log("Invalid input type")
    }

    //Multiplier label
    let span = document.createElement("span");
    span.setAttribute("class", "multiplierLabel");
    span.innerText = "x" + pointValue;
    if(hasMultiplierLabels){
        //container.appendChild(span);
        addFlexDivAroundElement(container, span);
    }

    //Whether to include <br> or not
    if(newLine){
        container.appendChild(document.createElement("br"));
    }
    
    //Add the container to to the <div>
    inputDiv.appendChild(container);

    
    
}

/*This function creates a flex div around a 
 *@param parentDiv The parent element that the flex div will be added to 
 *@param childElement The element that will be put inside the flex div
 *@return
 */
function addFlexDivAroundElement(parentDiv, childElement){
    let container = document.createElement("div");
    container.appendChild(childElement);
    container.setAttribute("class","flex");
    parentDiv.appendChild(container);
}


//This function advances to the next match
function nextMatch(){
    let read = parseInt(localStorage.getItem("match#"));
    //console.log(read);
    if(read == "NaN"){
       localStorage.setItem("match#", 1);
    }else{
        localStorage.setItem("match#", read+1);
    }
    
    
    document.getElementById("matchNum").value = localStorage.getItem("match#");
    
}

function updateMatch(){
    localStorage.setItem("match#", document.getElementById("matchNum").value);
    
}

//This function updates the multiplier lables to make them reflect the array
function updateMultiplierLabels(){
    let labels = document.getElementsByClassName("multiplierLabel");
    
    for(let i = 0; i < labels.length; i++){
        labels[i].innerHTML = scoreMultipliers[i];
    }
    
}

//This function takes an HTML element and uses its attributes to calculate its value
function calculatePointValue(element){
    //Get the type of input the element is
    let type = element.type;
    //Read the point value or values of 
    let pointValue = element.dataset.pointvalue;
    //Turn into array
    pointValue = pointValue.split(",");
    let isMultiplied = element.dataset.ismultiplied;
    
    
    let value = 0;
    //Read the correct value depending on the type
    if (type == "number"){ 
        value = element.value;
    }else if (type == "checkbox"){ 
        if(element.checked){
            value = "1";
        }else{
            value = "0";
        }
    }else if (type == "select-one"){
        //Get the index of the currently selected dropdown item
        value = element.selectedIndex;
        
        
        
    }else {let value = 1000; console.log(type);}
    
    /*
    //Check to make sure the input isn't empty
    if(value.length > 0){
        //Turn the strings from the JSON into integers
        value = parseInt(value);
    }else{
        value = 0;
    }*/
    
    
    //console.log("Element:" + element.dataset.pointvalue);
    //console.log(pointValue);
    //console.log(isMultiplied + "2");
    //console.log(value);
    //console.log(hasLinearPointScaling);
    
    //Use the multiplier table to scale the input
    if(pointValue.length == 1){
        value *= parseInt(pointValue);
    }else{
        value = pointValue[value];
    }
    
    //console.log(value);
    
    //Global level multiplier
    //if(isMultiplied){
    //    value *= difficultyMultiplier;
    //}
    //console.log(pointValue.length);
    //console.log(value + type);
    return parseInt(value);
}

//This function calculates the total score
function calculateScores(){
    let parts = document.getElementsByClassName("sum");
    //console.log(parts.length);
    total = 0;
    for(element of parts){
        total += calculatePointValue(element);
        
        //console.log(value)
        
    }
    //console.log(total);
    document.getElementById("totalScore").innerHTML = total;
    
    //Set difficulty multiplier
    //REMOVED CODE
    //let multiplierValue = difficultyMultiplierLevels[0];
    //console.log(multiplierValue);
    //difficultyMultiplier = multiplierValue;
    
    //Update the multiplier arrays  and elements
    //updateScoreMultipliers();
    //updateMultiplierLabels();
    
     
}

//This function increases the value in the element "display"
function increment(display){
    
    const counterDisplay = document.getElementById(display);
    let currentVal = parseInt(counterDisplay.value);
    let maximum = counterDisplay.dataset.max;
    
    
    
    if(currentVal < maximum || maximum == undefined){
        currentVal ++;
    }
    counterDisplay.value = currentVal;
    
    
}

//This function decreases the value in the element "display"
function deincrement(display){
   const counterDisplay = document.getElementById(display);
    let currentVal = parseInt(counterDisplay.value);
    if(currentVal > 0){
        currentVal --;
    }
    counterDisplay.value = currentVal;
}


//This function saves all the data as a JSON item
function send(){
    let legal = document.getElementById("legal");
    let jsonOut = document.getElementById("jsonOut");
    if(! legal.checked){
        //Error Message
        jsonOut.innerHTML = "Please agree to the terms and conditions";
        return;
    }
    try{
        let data = {"field":null,
                    "matchNum":null,
                    "team":"null",
                    "totalScore":null,
                    "signiture":"null"};
                   
        data["field"] = localStorage.getItem("code");
        data["matchNum"] = document.getElementById("matchNum").value;
        data["team"] = document.getElementById("teamDisplay").value;
        
        //include all the sums
        let inputs = document.getElementsByClassName("sum");
        
        
        //Need to read value and save as dict instead. Loop through and read correct property********************************************
        //Create empty dictionary
        let inputValues = {};
        
        //Loop through the html elements in the input list
        for (key of inputs){
            //Save the element id and element value as a key-value pair
            inputValues[key.id] = key.value;
            
        }
        
        data = {...data, ...inputValues};
        
        
        data["totalScore"] = total.toString();
        //document.getElementById("jsonOut").innerHTML = JSON.stringify(data);
        
        
        updateMatch();
        nextMatch();
        console.log(inputs);
        
        sendToServer(data);
        
        //Reset the form by forcing the page to reload
        //window.location.reload()
        
    }
    catch(err){
        
        //Error catching
        document.getElementById("jsonOut").innerHTML = err;
    }
}


function sendToServer(dataToSend){
    let jsonString = JSON.stringify(dataToSend);
    //const url = 'https://api.example.com/data';
    const url = "/api/data";
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Important: tells the server the body is JSON
        },
        body: jsonString // The JSON string as the request body
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }else{
            window.location.reload();
        }
        return response.json(); // If expecting a JSON response
    })
    .then(data => {
        console.log('Success:', data);
        
    })
    .catch(error => {
        console.error('Error Special:', error);
    });
}
