const codes =["01GR", "01RD", "01YL", "01BL"];
function getValue() {
  const inputValue = document.getElementById("gcode").value;
  console.log(inputValue);
  if (codes.includes(inputValue)){
      console.log("working");
      const matchNum = 1;
      //Store the code you entered in local storage under the variable code
      localStorage.setItem("code", inputValue);
      localStorage.setItem("match#", matchNum);
      
      // Call server to create session before redirecting
      fetch('/api/validate-session', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ code: inputValue, matchNum: matchNum })
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Session validation failed');
          }
          return response.json();
      })
      .then(data => {
          // Session created successfully, now redirect
          window.location.href = 'scoreboard.html';
      })
      .catch(error => {
          console.error('Error:', error);
          document.getElementById('errortext').style.visibility='visible';
      });
  } else{
      document.getElementById('errortext').style.visibility='visible'
  }
}

function logIn() {
    const field = document.getElementById("field").value;
    const color = document.getElementById("color").value;
    
    if(color == "NA" || field == "NA"){
        //document.getElementById('errortext').style.visibility='visible';
        document.getElementById('errortext').style.display='block';
        return;
    }
    
    const code = "" + field + color;
    const matchNum = 1;
    
    localStorage.setItem("code", code);
    localStorage.setItem("match#", matchNum);
    localStorage.setItem("fieldColor", color);
    
    // Call server to create session before redirecting
    fetch('/api/validate-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code, matchNum: matchNum })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Session validation failed');
        }
        return response.json();
    })
    .then(data => {
        // Session created successfully, now redirect
        window.location.href = 'scoreboard.html';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('errortext').textContent = 'Login failed. Please try again.';
        document.getElementById('errortext').style.display='block';
    });
}