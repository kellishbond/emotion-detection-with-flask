from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# API endpoint and headers for Watson Emotion API
API_URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def get_emotion_analysis(text_to_analyse):
    """
    Sends a request to the Watson Emotion API to analyze the given text.

    Args:
        text_to_analyse (str): The text to analyze for emotions.

    Returns:
        response (requests.Response): The response object from the API call.
    """
    data = {
        "raw_document": {
            "text": text_to_analyse
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    return response

def emotion_detector(text):
    """
    Analyzes the emotions in the provided text using Watson Emotion API.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary with emotion scores and the dominant emotion,
              or an error message if the API call fails.
    """
    response = get_emotion_analysis(text)
    if response.status_code == 200:
        data = response.json()
        emotions = data['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotions, key=emotions.get)


        formatted_result = {
            'anger': emotions.get('anger', 0),
            'disgust': emotions.get('disgust', 0),
            'fear': emotions.get('fear', 0),
            'joy': emotions.get('joy', 0),
            'sadness': emotions.get('sadness', 0),
            'dominant_emotion': dominant_emotion
        }
        return formatted_result
    elif response.status_code == 400:
        return {key: None for key in ['anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion']}
    else:
        return {"error": "Failed to connect to the API"}

@app.route('/')
def index():
    """
    Renders the main HTML form for input.

    Returns:
        str: The rendered HTML template.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    """
    Handles emotion detection requests via GET or POST.

    Returns:
        Response: JSON response containing emotion analysis results,
                  or an error message for invalid input.
    """
    text = request.json.get("text") if request.method == 'POST' else request.args.get("textToAnalyze")
    
    if not text:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    result = emotion_detector(text)
    if result.get("dominant_emotion") is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
