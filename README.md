# 🎙️ PodCaster AI — Create Intelligent Podcasts from Text

**PodCaster AI** is a Django-based web app that turns your ideas into full podcast episodes. It lets you generate podcast scripts with Gemini or GPT and converts them to realistic speech using [Piper TTS](https://github.com/rhasspy/piper) — completely offline.

---

## Features

-  **AI-Generated Podcast Scripts**  
  Generate high-quality podcast content using Gemini or OpenAI.

-  **Chat-style Interface**  
  Interact with your AI assistant in real time to refine or expand your script.

-  **Text-to-Speech with Piper**  
  Convert your podcast to human-like audio locally using the fast, open-source Piper engine.

-✍ **Markdown Support**  
  Write and preview formatted content before narration.

-   **Full Local Processing**  
  No cloud TTS required — everything runs on your machine.

---

##  Tech Used:

| Layer             | Tech                    |
|------------------|-------------------------|
| Backend          | Django 5.x              |
| AI Integration   | Gemini 2.5 / OpenAI GPT |
| TTS Engine       | [Piper TTS](https://github.com/rhasspy/piper) |
| Frontend         | Bootstrap 5 + JS        |
| Script Parsing   | `markdown`, `BeautifulSoup` |
| Audio Output     | `.wav` files via Piper  |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/blackwolf2902/podcaster.git
cd podcaster
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Download Piper Binary and Voice Model

```bash
mkdir piper && cd piper
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-amy-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-amy-medium.onnx.json
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
chmod +x piper
cd ..
```

### 5. Set Your API Key

Create a `.env` file in your root directory:

```env
API_KEY=your_key
```

---

## 🧪 Running the App

```bash
python manage.py migrate
python manage.py runserver
```

Open in browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Outputs

- **Scripts** saved as `.md` in the root directory:  
  `podcast_script_YYYYMMDD_HHMMSS.md`

- **Audio** saved as `.wav` in `/piper/`:  
  `podcast_audio_YYYYMMDD_HHMMSS.wav`

Access audio at:  
`http://localhost:8000/media/podcast_audio_YYYYMMDD_HHMMSS.wav`

---

## 🛠 Developer Highlights

- Markdown-to-plain-text cleaning before TTS
- Fully offline voice generation
- Chat logic managed via DeepSeekR1 API backend session
- Uses Django’s session to track active podcast flow

---

##  Future Enhancements (Open for Contributions)

- 🔊 Add background music and transitions (via FFmpeg)
- 🎛️ Voice customization (pitch, speed, pauses)
- 📡 Export to RSS, Spotify, YouTube
- 🗣️ Multi-voice / speaker identification (via Dia TTS)

---

## 🤝 Credits

- [Piper TTS](https://github.com/rhasspy/piper)
- [OpenRouter.ai](https://openrouter.ai/) (For API)
- [Bootstrap 5](https://getbootstrap.com/)

---

## 📜 License

MIT License.  
Built with ❤️ by **Arumugam N**.
