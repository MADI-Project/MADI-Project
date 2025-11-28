# MADI PROJECT: Local Education with Emotion Recognition
## A learning assistant device designed so that the student can ask questions with their voices and receive simple explanations in real time. 
Among its main features are:
* It works without an internet connection.
* It only listens when a physical button is pressed.
* It recognizes when a student is speaking normally or with signs of frustration, adapting its tone to explain more patiently.
* It does not record personal data.
* It does not store or transmit information outside the device.
* The prototype was specifically designed to support teaching and learning processes with complete safety for students.



# Emotion-Aware Local Educational Assistant  
TinyML (Edge Impulse) · Jetson Orin Nano Super · Gemma-2 LLM · Whisper STT · Piper TTS

This project showcases how **Edge Impulse TinyML models** can power real-time **emotion recognition** on microcontrollers and how this emotional signal can be used to adapt the behavior of a **local LLM** running on embedded hardware.  
Emotion detection is the core innovation of this project and the main driver of the assistant’s teaching style.

Everything runs fully offline on:
- Arduino Nano 33 BLE Sense (TinyML inference)
- Jetson Orin Nano Super (STT, LLM, TTS)

Enabling privacy-focused, low-latency deployment for classrooms and embedded environments.

---

# 1. Role of TinyML in the Project

A central component of this assistant is its ability to recognize the user’s emotional state directly on a low-power microcontroller.  
For this, a lightweight audio-based classifier was designed using a TinyML workflow and deployed on the Arduino Nano 33 BLE Sense.  
The model runs entirely on-device and distinguishes between two states:

- Neutral  
- Negative / Frustrated  

The Jetson receives these probabilities over serial and uses them to adjust the behavior of the language model, enabling responses that feel more supportive when signs of frustration appear.


### Benefits provided by TinyML Model:

- TinyML neural networks that run fully on-device  
- Real-time emotion recognition without cloud processing  
- MFCC audio processing optimized for the Nano 33 BLE Sense  
- Perfect integration with embedded workflows  
- Minimal RAM usage  
- Extremely low latency  
- Privacy-preserving inference  
- Reproducibility for hackathon evaluation  

**The emotional intelligence layer of this assistant depends entirely on Edge Impulse**, and it is the foundation of how the system behaves.

---

# 2. Emotion Recognition Pipeline (Core Component)

```
+---------------------------+
| Arduino Nano 33 BLE Sense |
+------------+--------------+
             |
     Built-in microphone
             |
             v
+-------------------------------+
| Edge Impulse TinyML Model    |
| - MFCC audio features         |
| - Lightweight classifier      |
+-------------------------------+
             |
             v
  Output probabilities:
       negative, neutral
             |
             v
+-------------------------------+
| JSON over USB Serial          |
| {"id":"audio",                |
|  "negative":0.20,             |
|  "neutral":0.80}              |
+-------------------------------+
             |
             v
      Jetson Orin Nano
```

The Jetson reads these probabilities, fuses data, and determines one of:

```
NEUTRAL
FRUSTRATED
```

This emotional state completely changes the LLM’s tone, pacing, and level of detail.

---

# 3. Emotion-Adaptive LLM Behavior

### Neutral learner:
- Clear and direct explanations  
- Secondary school–level reasoning  

### Frustrated learner:
- Slow, patient response style  
- Step-by-step reasoning  
- Encouraging tone  
- Simple examples and micro-activities  

Emotion is not decoration.  
Emotion *determines* how the assistant teaches.

---

# 4. High-Level System Architecture

```
+---------------------------------------------------------------+
|                       EMOTION FIRST                           |
+---------------------------------------------------------------+

+---------------------------+        +---------------------------+
| Arduino Nano BLE Sense   |        | Jetson Orin Nano Super    |
| (Edge Impulse TinyML)    |        | (Local AI Pipeline)       |
+------------+--------------+        +-------------+-------------+
             | JSON (serial)                        |
             v                                       v
     +---------------------+             +---------------------------+
     |  Emotion Manager    |             |  Whisper STT             |
     |  Fusion + State     |             +------------+-------------+
     +----------+----------+                          |
                |                                      v
                |                           +-----------------------+
                |                           | Adaptive System Prompt|
                v                           +-----------+-----------+
      Emotion State (NEUTRAL / FRUSTRATED)              |
                                                        v
                                            +------------------------+
                                            | Gemma-2 LLM (LLM server)|
                                            +-----------+------------+
                                                        |
                                                        v
                                            +------------------------+
                                            | Piper TTS             |
                                            +-----------+------------+
                                                        |
                                                        v
                                                   Speaker Output
```

---

# 5. Project Overview

This assistant performs:

- Speech-to-text using Whisper  
- Emotion recognition using Edge Impulse TinyML  
- Emotion fusion on Jetson  
- Emotion-adaptive prompting for LLM  
- Local educational reasoning using Gemma-2 (llama.cpp)  
- Local text-to-speech using Piper  
- Push-to-talk hardware control  

All inference is offline, private, and fast.

---

# 6. Repository Structure

```
/
├── assistant.py               Main assistant script
├── README.md                  Project documentation
├── requirements.txt           Python dependencies
├── assets/
│   ├── bip.wav
│   └── bip2.wav
├── docs/
│   ├── installation_guide_jetson.md
│   ├── installation_guide_arduino.md
│   └── assets/
└── models/                    Placeholder for Gemma-2 GGUF model
```

---

# 7. Serial Emotion JSON Format

The Arduino must output the following structure:

```json
{"id":"audio","negative":0.13,"neutral":0.87}
```

Jetson logic:

- Reads probabilities via `/dev/ttyACM0`
- Normalizes values
- Determines final emotion state
- Adapts LLM prompt accordingly

---

# 8. Quick Start for Judges

### 1. Start LLM server:
```bash
cd ~/llama.cpp/build
./bin/llama-server \
  -m ../models/gemma-2-2b-it-Q4_K_S.gguf \
  -p 8090 -t 4 -c 2048 -ngl 999
```

### 2. Activate Python environment:
```bash
cd ~/orin_nano_assistant
source venv/bin/activate
```

### 3. Run assistant:
```bash
python3 assistant.py
```

### 4. Usage:
- Press and hold button → speak  
- Release → Whisper transcribes  
- Edge Impulse model provides emotion  
- Jetson fuses emotion  
- LLM responds with adapted tone  
- Piper speaks the output  

---

# 9. Installation

Jetson setup:
```
docs/installation_guide_jetson.md
```

Arduino/Edge Impulse setup:
```
docs/installation_guide_arduino.md
```

---

# 10. Configuration (assistant.py)

```
USE_IMAGE_EMOTION = False
USE_GUI_MODE = True
LANGUAGE = "es"
BUTTON_PIN = 15
AUDIO_SERIAL_PORT = "/dev/ttyACM0"
LLM_URL = "http://127.0.0.1:8090/completion"
PIPER_MODEL_PATH = "/usr/local/share/piper/models/es_MX-ald-medium.onnx"
```

---

# 11. Optional Extensions

Not required for judging but available:

- Image-based emotion model  
- Additional LLM languages  
- RAG context from local documents  
- Larger GGUF models (9B)  
- Multi-turn conversation memory  

---

# 12. Author

Didier – 2025  
Embedded AI • TinyML • Edge LLM Engineering

---

# 13. License

This project is provided for educational and research use as part of the Edge Impulse Hackathon.
