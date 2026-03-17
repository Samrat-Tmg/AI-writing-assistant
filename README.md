# AI Writing Assistant 🖊️

A private, free, local AI writing assistant for novelists 
and storytellers. Runs entirely on your Mac — no cloud, 
no subscriptions, no data collection.

Built by a writer and CS student from Kathmandu, Nepal.
Built with Ollama + Mistral + Python.

## What it does
- Reads your existing stories and learns your writing style
- Takes your plot skeletons, scene ideas, and rough notes
- Turns them into full polished prose in YOUR voice
- Saves everything locally — your stories never leave your machine

## Works great for
- Horror
- Thriller / Mystery  
- Romance / Drama

## Requirements

### Mac (M1/M2/M3/M4) — Recommended
- Python 3.9+
- Ollama installed
- 8GB RAM minimum
- 15GB free disk space

### Linux (Ubuntu/Debian)
- Python 3.9+
- Ollama installed
- 8GB RAM minimum
- 15GB free disk space

### Windows 10/11
- Python 3.9+ (from python.org)
- Ollama for Windows (from ollama.com)
- 8GB RAM minimum
- 15GB free disk space
- Git Bash or PowerShell recommended

## Installation by OS

### Mac/Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
git clone https://github.com/Samrat-Tmg/AI-writing-assistant
cd AI-writing-assistant
pip3 install python-docx ollama rich requests beautifulsoup4
```

### Windows
```bash
# 1. Download and install Ollama from ollama.com
# 2. Open PowerShell and run:
winget install ollama
ollama pull mistral
git clone https://github.com/Samrat-Tmg/AI-writing-assistant
cd AI-writing-assistant
pip install python-docx ollama rich requests beautifulsoup4
```

## Quick Start

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull Mistral
```bash
ollama pull mistral
```

### 3. Clone this repo
```bash
git clone https://github.com/Samrat-Tmg/AI-writing-assistant
cd AI-writing-assistant
```

### 4. Install dependencies
```bash
pip3 install python-docx ollama
```

### 5. Add your stories
Copy your .docx story files into:
```
~/Documents/stories/
```

### 6. Analyze your style
```bash
python3 story_memory.py
```

### 7. Start writing
```bash
python3 writer.py
```

## How it works
1. Reads your existing stories from ~/Documents/stories/
2. Builds a personal style profile using Mistral AI
3. Uses that profile as memory in every generation
4. You give it plot skeletons, scene ideas, character notes
5. It writes full prose that sounds like YOU

## Privacy
Your stories and style profile never leave your machine.
The .gitignore ensures they can never be accidentally uploaded.

## License
MIT License — free to use, modify, and distribute.

## Author
Made with ☕ in Kathmandu, Nepal
```

Click **Commit changes** when done.

---

**2 — Add a `requirements.txt` file**

In your repo click **Add file** → **Create new file** → name it `requirements.txt` → paste:
```
python-docx==1.1.0
ollama==0.1.8
