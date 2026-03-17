import os
import ollama

BIBLE_DIR = os.path.expanduser("~/writing-assistant/story-bible")
OUTPUT_DIR = os.path.expanduser("~/writing-assistant/output")

def load_style_profile():
    path = os.path.join(BIBLE_DIR, "style_profile.txt")
    with open(path, "r") as f:
        return f.read()

def save_output(content, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"\n✅ Saved to: {path}")

def generate(system_prompt, user_prompt):
    print("\n✍️  Writing...\n")
    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    return response["message"]["content"]

def get_system_prompt():
    style = load_style_profile()
    return f"""You are a creative writing assistant for this specific author.

AUTHOR'S STYLE PROFILE:
{style}

Your job is to take the author's raw ideas — plot skeletons, 
rough paragraphs, twist ideas, character notes — and turn them 
into fully written prose that matches this author's voice exactly.

Rules:
- Always match the author's first person present tense style
- Keep their psychological horror atmosphere
- Expand their skeleton into rich full prose
- Never add ideas they didn't give you
- Never sound generic or AI-like
- Their vision, your execution"""

def menu():
    print("\n╔═══════════════════════════════════╗")
    print("║     AI WRITING ASSISTANT  🖊️       ║")
    print("╠═══════════════════════════════════╣")
    print("║  1. Expand plot into chapter      ║")
    print("║  2. Expand scene skeleton         ║")
    print("║  3. Polish rough paragraph        ║")
    print("║  4. Build out a twist             ║")
    print("║  5. Flesh out a character         ║")
    print("║  6. Continue from last scene      ║")
    print("║  7. Exit                          ║")
    print("╚═══════════════════════════════════╝")
    return input("\nChoose (1-7): ").strip()

def get_multiline_input(prompt):
    print(f"\n{prompt}")
    print("(Type your idea, press Enter twice when done)\n")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()

def main():
    print("\n📚 Loading your style profile...")
    system_prompt = get_system_prompt()
    print("✅ Your writing style loaded!\n")

    while True:
        choice = menu()

        if choice == "1":
            idea = get_multiline_input("Give me your plot outline or skeleton:")
            genre = input("Genre (horror/thriller/romance): ").strip()
            prompt = f"Expand this plot outline into a full opening chapter.\nGenre: {genre}\n\nPlot:\n{idea}"
            result = generate(system_prompt, prompt)

        elif choice == "2":
            idea = get_multiline_input("Give me your scene skeleton:")
            prompt = f"Expand this scene skeleton into full vivid prose:\n\n{idea}"
            result = generate(system_prompt, prompt)

        elif choice == "3":
            idea = get_multiline_input("Paste your rough paragraph:")
            prompt = f"Polish this rough paragraph into my writing style:\n\n{idea}"
            result = generate(system_prompt, prompt)

        elif choice == "4":
            idea = get_multiline_input("Describe your twist idea:")
            prompt = f"Build out this twist with full tension and atmosphere:\n\n{idea}"
            result = generate(system_prompt, prompt)

        elif choice == "5":
            idea = get_multiline_input("Give me your character notes:")
            prompt = f"Flesh out this character with depth and complexity:\n\n{idea}"
            result = generate(system_prompt, prompt)

        elif choice == "6":
            idea = get_multiline_input("Paste your last scene or where you left off:")
            direction = get_multiline_input("Where do you want it to go next?")
            prompt = f"Continue this story naturally.\n\nLast scene:\n{idea}\n\nDirection:\n{direction}"
            result = generate(system_prompt, prompt)

        elif choice == "7":
            print("\n👋 Happy writing!\n")
            break

        else:
            print("Invalid choice, try again.")
            continue

        print("\n═══════════════════════════════")
        print(result)
        print("═══════════════════════════════")

        save = input("\n💾 Save this output? (y/n): ").strip().lower()
        if save == "y":
            filename = input("Name this file (e.g. chapter1.txt): ").strip()
            save_output(result, filename)

if __name__ == "__main__":
    main()
