import pickle

with open("transcription_data.pkl", "rb") as f:
    data = pickle.load(f)

print("Transcribed Text:", data["transcribed_text"])
print("Generated Questions:", data["generated_questions"])
