import requests

# Replace `url` and `headers` with your actual values
url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
headers = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}

def emotion_detector(text_to_analyse):
    # Check if the input is empty
    if not text_to_analyse.strip():
        # Return None for all emotion keys
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    payload = {
        "raw_document": {
            "text": text_to_analyse
        }
    }
    
    print("Sending request to API...")  # Debugging statement before the request

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Response status code:", response.status_code)  # Check if response is received

        if response.status_code == 200:
            response_data = response.json()
            print("Full API response:", response_data)  # Print the JSON response for verification

            emotions = response_data.get('emotionPredictions', [{}])[0].get('emotion', {})
            anger_score = emotions.get('anger', 0)
            disgust_score = emotions.get('disgust', 0)
            fear_score = emotions.get('fear', 0)
            joy_score = emotions.get('joy', 0)
            sadness_score = emotions.get('sadness', 0)

            emotion_scores = {
                "anger": anger_score,
                "disgust": disgust_score,
                "fear": fear_score,
                "joy": joy_score,
                "sadness": sadness_score
            }
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

            result = {
                "anger": anger_score,
                "disgust": disgust_score,
                "fear": fear_score,
                "joy": joy_score,
                "sadness": sadness_score,
                "dominant_emotion": dominant_emotion
            }

            print("Formatted result:", result)  # Print final output
            return result

        else:
            print("Failed to connect. Status code:", response.status_code)
            print("Response text:", response.text)  # Print any error details from the API
            return {"error": "Failed to retrieve emotions"}

    except requests.exceptions.RequestException as e:
        print("Error connecting to Watson API:", e)
        return {"error": "Connection failed", "details": str(e)}
