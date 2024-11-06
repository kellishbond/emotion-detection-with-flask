let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            let responseElement = document.getElementById("system_response");
            if (this.status == 200) {
                // Parse the JSON response
                let responseData = JSON.parse(xhttp.responseText);
                
                // Create a formatted string to display
                let resultHtml = `
                    <h3>Emotion Detection Results:</h3>
                    <p><strong>Anger:</strong> ${responseData.anger}</p>
                    <p><strong>Disgust:</strong> ${responseData.disgust}</p>
                    <p><strong>Fear:</strong> ${responseData.fear}</p>
                    <p><strong>Joy:</strong> ${responseData.joy}</p>
                    <p><strong>Sadness:</strong> ${responseData.sadness}</p>
                    <p><strong>Dominant Emotion:</strong> ${responseData.dominant_emotion}</p>
                `;
                responseElement.innerHTML = resultHtml;
            } else {
                responseElement.innerHTML = "Error: Invalid text! Please try again!";
            }
        }
    };
    xhttp.open("POST", "/emotionDetector", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify({ text: textToAnalyze }));
}

