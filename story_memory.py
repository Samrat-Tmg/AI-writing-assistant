import os
from docx import Document
import ollama

STORIES_DIR = os.path.expanduser("~/Documents/stories")
BIBLE_DIR = os.path.expanduser("~/writing-assistant/story-bible")

def read_docx(filepath):
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def load_all_stories():
    stories = {}
    for filename in os.listdir(STORIES_DIR):
        if filename.endswith(".docx"):
            path = os.path.join(STORIES_DIR, filename)
            stories[filename] = read_docx(path)
            print(f"✅ Loaded: {filename}")
    return stories

def analyze_style(stories):
    combined = "\n\n---\n\n".join(stories.values())
    sample = " ".join(combined.split()[:3000])

    prompt = f"""You are a literary analyst. Analyze these story excerpts written by the same author and extract:

1. WRITING STYLE - sentence structure, pacing, vocabulary level
2. TONE - dark, atmospheric, suspenseful, emotional?
3. RECURRING THEMES - what themes appear across stories?
4. NARRATIVE VOICE - first person, third person, how does narrator feel?
5. SIGNATURE TECHNIQUES - what makes this writer unique?

Stories:
{sample}

Give a detailed analysis in each category."""

    print("\n🔍 Analyzing your writing style...\n")
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]

def save_style_profile(analysis):
    path = os.path.join(BIBLE_DIR, "style_profile.txt")
    with open(path, "w") as f:
        f.write(analysis)
    print(f"\n✅ Style profile saved to: {path}")

def main():
    print("📚 Loading your stories...\n")
    stories = load_all_stories()

    if not stories:
        print("❌ No .docx files found in ~/Documents/stories/")
        return

    print(f"\n📖 Found {len(stories)} stories. Analyzing...\n")
    analysis = analyze_style(stories)

    print("\n═══════════════════════════════")
    print("YOUR WRITING STYLE PROFILE")
    print("═══════════════════════════════")
    print(analysis)

    save_style_profile(analysis)

if __name__ == "__main__":
    main()
