import os
from docx import Document
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box
from rich.rule import Rule
from rich.prompt import Confirm

console = Console()

STORIES_DIR = os.path.expanduser("~/Documents/stories")
BIBLE_DIR = os.path.expanduser("~/writing-assistant/story-bible")

# ═══════════════════════════════
# HEADER
# ═══════════════════════════════
def show_header():
    console.clear()
    console.print(Panel.fit(
        "[bold magenta]STYLE ANALYZER 🔍[/bold magenta]\n"
        "[dim]Reads your stories · Learns your voice[/dim]\n"
        "[dim]Private · Never leaves your Mac[/dim]",
        border_style="magenta",
        padding=(1, 4)
    ))

# ═══════════════════════════════
# READ DOCX
# ═══════════════════════════════
def read_docx(filepath):
    doc = Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# ═══════════════════════════════
# LOAD STORIES
# ═══════════════════════════════
def load_all_stories():
    if not os.path.exists(STORIES_DIR):
        console.print(Panel(
            f"[red]❌ Stories folder not found!\nExpected: {STORIES_DIR}[/red]",
            border_style="red"
        ))
        exit()

    stories = {}
    files = [f for f in os.listdir(STORIES_DIR) if f.endswith(".docx")]

    if not files:
        console.print(Panel(
            "[red]❌ No .docx files found in ~/Documents/stories/[/red]",
            border_style="red"
        ))
        exit()

    table = Table(
        title="📚 Your Stories",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan"
    )
    table.add_column("File", style="white")
    table.add_column("Size", style="dim")
    table.add_column("Status", style="green")

    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]{task.description}"),
        console=console
    ) as progress:
        for filename in files:
            task = progress.add_task(f"Loading {filename}...", total=None)
            path = os.path.join(STORIES_DIR, filename)
            content = read_docx(path)
            stories[filename] = content
            size = f"{len(content.split())} words"
            table.add_row(filename, size, "✅ Loaded")
            progress.remove_task(task)

    console.print()
    console.print(table)
    return stories

# ═══════════════════════════════
# ANALYZE STYLE
# ═══════════════════════════════
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

    with Progress(
        SpinnerColumn(style="magenta"),
        TextColumn("[magenta]Analyzing your writing style..."),
        console=console
    ) as progress:
        task = progress.add_task("analyzing", total=None)
        response = ollama.chat(model="mistral", messages=[
            {"role": "user", "content": prompt}
        ])
        progress.remove_task(task)

    return response["message"]["content"]

# ═══════════════════════════════
# SAVE PROFILE
# ═══════════════════════════════
def save_style_profile(analysis):
    os.makedirs(BIBLE_DIR, exist_ok=True)
    path = os.path.join(BIBLE_DIR, "style_profile.txt")
    with open(path, "w") as f:
        f.write(analysis)
    console.print(f"\n[green]✅ Style profile saved → {path}[/green]")

# ═══════════════════════════════
# MAIN
# ═══════════════════════════════
def main():
    show_header()

    console.print("\n[dim]Loading your stories from ~/Documents/stories/...[/dim]\n")
    stories = load_all_stories()

    console.print(f"\n[bold cyan]Found {len(stories)} stories — analyzing your style...[/bold cyan]\n")

    analysis = analyze_style(stories)

    console.print()
    console.print(Panel(
        analysis,
        title="[bold magenta]✨ Your Writing Style Profile[/bold magenta]",
        border_style="magenta",
        padding=(1, 2)
    ))

    console.print()
    if Confirm.ask("[cyan]Save this style profile?[/cyan]"):
        save_style_profile(analysis)
        console.print()
        console.print(Panel(
            "[bold green]✅ Style profile saved![/bold green]\n"
            "[dim]sam_writer.py will use this automatically.[/dim]\n"
            "[dim]Run this again whenever you add new stories.[/dim]",
            border_style="green",
            padding=(1, 2)
        ))
    else:
        console.print("\n[dim]Profile not saved.[/dim]")

if __name__ == "__main__":
    main()
