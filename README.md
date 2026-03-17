# AI Writing Assistant 🖊️

A private, free, local AI writing assistant built for 
novelists and storytellers. Runs entirely on your machine 
— no cloud, no subscriptions, no data collection.

Built with Ollama + Mistral + Python.

## Features
- Learns your unique writing style
- Generates chapters with persistent story memory
- Edits and rewrites scenes on command
- Researches facts for your story world
- Works offline — your stories never leave your machine
- Supports horror, thriller, romance, mystery genres

## Why I built this
As a writer and CS student, I wanted an AI writing 
assistant that truly understood my voice — not a generic 
tool. This is fully private and customizable.

## Requirements
- Mac (M1/M2/M3/M4) or Linux
- Python 3.9+
- Ollama installed
- 8GB RAM minimum
- 10GB free disk space

## Quick Start

### 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

### 2. Pull Mistral
ollama pull mistral

### 3. Clone this repo
git clone https://github.com/yourusername/ai-writing-assistant
cd ai-writing-assistant

### 4. Install dependencies
pip3 install -r requirements.txt

### 5. Add your stories
Copy your .docx, .txt, or .pdf stories into:
my-stories/

### 6. Run style analyzer
python3 src/story_memory.py

### 7. Start writing
python3 src/writer.py

## How it works
1. Reads your existing stories
2. Builds a personal style profile
3. Uses that profile as memory in every generation
4. Generates new content that sounds like YOU

## Roadmap
- [x] Style analyzer
- [x] Chapter generator
- [ ] Web research integration
- [ ] Fine-tuning support
- [ ] Web UI

## License
MIT License — free to use, modify, and distribute.

## Contributing
Pull requests welcome. Please read CONTRIBUTING.md first.
```

---

**The `.gitignore` file — protects your private data:**
```
# Never upload these
my-stories/
story-bible/
output/
*.modelfile
*.bin
__pycache__/
.env
*.pyc
.DS_Store
```

---

**The `requirements.txt` file:**
```
python-docx==1.1.0
ollama==0.1.8
requests==2.31.0
beautifulsoup4==4.12.2
rich==13.7.0
