import cv2
import numpy as np
import pyaudio
import wave
import time
import threading

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 500  # Audio level threshold to detect talking
TALKING_DURATION_THRESHOLD = 2  # Seconds to consider continuous talking

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Global variable to track talking status
is_talking = False

def detect_talking():
    global is_talking
    talking_start_time = None

    while True:
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        audio_level = np.abs(data).mean()

        if audio_level > THRESHOLD:
            if not talking_start_time:
                talking_start_time = time.time()
            elif time.time() - talking_start_time > TALKING_DURATION_THRESHOLD:
                is_talking = True
        else:
            talking_start_time = None
            is_talking = False

# Start audio processing thread
audio_thread = threading.Thread(target=detect_talking)
audio_thread.start()

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if is_talking:
        cv2.putText(frame, "Danger! Talking detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Safe", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Talking Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
p.terminate()
