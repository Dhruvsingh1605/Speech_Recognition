import speech_recognition as sr
import openai
import pickle

openai.api_key = "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"

r = sr.Recognizer()

def record_text():
    """Record audio and transcribe to text."""
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening...")
            audio2 = r.listen(source2)
            Mytext = r.recognize_google(audio2)
            print(f"Recognized text: {Mytext}")
            return Mytext
    except sr.RequestError as e:
        print(f"Could not request results: {e}")
        return None
    except sr.UnknownValueError:
        print("Unknown speech detected. Please try again.")
        return None

def generate_questions(text):
    """Generate technical questions using OpenAI."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate five technical interview questions based on the following text:\n\n{text}",
            max_tokens=150,
            temperature=0.7,
        )
        questions = response.choices[0].text.strip()
        return questions
    except Exception as e:
        print(f"Error generating questions: {e}")
        return None

while True:
    text = record_text()
    if text is None:
        continue

    questions = generate_questions(text)
    if questions is None:
        continue

    data = {
        "transcribed_text": text,
        "generated_questions": questions
    }

    with open("transcription_data.pkl", "wb") as f:
        pickle.dump(data, f)

    print(f"Data saved to transcription_data.pkl")
    print(f"Transcribed Text: {text}")
    print(f"Generated Questions:\n{questions}")
