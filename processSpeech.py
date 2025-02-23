import speech_recognition as sr
import pyttsx3
import keyboard  # pip install keyboard
import threading
import processRequest

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Global variables to manage recording state and audio data
recording = False
audio_frames = []
recording_thread = None
sample_rate = None
sample_width = None

def SpeakText(command):
    """Speak the given text using pyttsx3."""
    engine.say(command)
    engine.runAndWait()

def record_audio():
    """
    Record audio continuously until the global 'recording' flag is set to False.
    The raw audio frames are stored in the global list 'audio_frames'.
    """
    global recording, audio_frames, sample_rate, sample_width
    audio_frames = []  # Reset the frames
    with sr.Microphone() as source:
        # Capture microphone parameters for later use
        sample_rate = source.SAMPLE_RATE
        sample_width = source.SAMPLE_WIDTH
        # Adjust for ambient noise for a short duration
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        while recording:
            try:
                # Removed exception_on_overflow argument to fix the error
                data = source.stream.read(source.CHUNK)
                audio_frames.append(data)
            except Exception as e:
                print("Error reading audio:", e)

def process_audio():
    """
    Process the accumulated audio frames by converting them into an AudioData object,
    sending it to Google's Speech Recognition service, printing and speaking the recognized text.
    """
    global audio_frames, sample_rate, sample_width
    # Combine all audio frames into a single bytes object
    raw_data = b''.join(audio_frames)
    audio_data = sr.AudioData(raw_data, sample_rate, sample_width)
    try:
        text = r.recognize_google(audio_data)
        print("Recognized text:", text)
        processRequest.process_request(text)
        # SpeakText(text)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Could not understand audio")

def toggle_recording():
    """
    Toggle the recording state when the shortcut key is pressed.
    If starting, spawn a new thread to record audio.
    If stopping, stop recording and process the audio.
    """
    global recording, recording_thread
    if not recording:
        print("Recording started. Press the shortcut key again to stop.")
        recording = True
        recording_thread = threading.Thread(target=record_audio)
        recording_thread.start()
    else:
        print("Recording stopped. Processing audio...")
        recording = False
        recording_thread.join()  # Wait for the recording thread to finish
        process_audio()

def base():
    # Set your chosen keyboard shortcut key (for example, F8)
    shortcut_key = "F8"
    print(f"Press '{shortcut_key}' to toggle recording on/off.")

    # Bind the toggle function to the shortcut key
    keyboard.add_hotkey(shortcut_key, toggle_recording)

    # Keep the program running indefinitely until you manually stop it
    keyboard.wait()