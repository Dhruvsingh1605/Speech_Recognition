import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI

eleven_labs = "sk_ad51e555f963c37e20ef7c0ef0ca4a5aa2c547a62210ddd5"
openai = "sk-proj—oZocKgxJJkxd4ZRla148k2D6zT1bFTanlEqx5OadeQkBQ-Eqw821DKI1egaHqB-plVEi7iTTwT3BlbkFJ_rA0pJDJTc5Mhic7xIaxIQCVCwvPVTONhmmg0s10FQmLbLqjzx4HPMp4ftMak1Z1Pzdng3axYA"


class AI_Assistant:
    def __init__self(self):
        aai.settings.api_key = "2cfbb383d6c84b13be20b858b059254c"
        self.openai_client = OpenAI(api_key=openai)
        self.elevenlabs_api_key = eleven_labs

        self.transcribe = None

        self.full_transcript = [
            {"role":"system", "content":"You are a Nurse at hospital, and you have to ask similar and related questions to the patient for better diagnosis of the patient"},
        ]
    def start_transcription(self):
        self.transcribe = aai.RealtimeTranscriber(
            sample_rate= 16000,
            on_data = self.on_data,
            on_error = self.on_error,
            on_open = self.on_open,
            on_close= self.on_clise,
            end_utterance_silence_threshold = 1000

        )

        self.transcribe.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcribe.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcribe:
            self.transcribe.close()
            self.transcribe = None
    
    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)
        return


    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")


    def on_error(self, error: aai.RealtimeError):
        print("An error occured:", error)
        return


    def on_close(self):
        return
    
    def generate_ai_response(self, transcript):

        self.stop_transcription()

        self.full_transcript.append({"role":"user", "content": transcript.text})
        print(f"\nPatient: {transcript.text}", end="\r\n")

        response = self.openai_client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = self.full_transcript
        )

        ai_response = response.choices[0].message.content

        self.generate_audio(ai_response)

        self.start_transcription()
        print(f"\nReal-time transcription: ", end="\r\n")

        
    def generate_audio(self, text):

        self.full_transcript.append({"role":"assistant", "content": text})
        print(f"\nAI Receptionist: {text}")

        audio_stream = generate(
            api_key = self.elevenlabs_api_key,
            text = text,
            voice = "Rachel",
            stream = True
        )

        stream(audio_stream)

greeting = "Thank you for calling Parth devariya's clinic. My name is Sandy, how may I assist you?"
ai_assistant = AI_Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()


