import os
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.rule import Rule
from datetime import datetime

console = Console()

BASE = os.path.expanduser("~/writing-assistant")

# ═══════════════════════════════
# HEADER
# ═══════════════════════════════
def show_header():
    console.clear()
    now = datetime.now().strftime("%B %d, %Y — %H:%M")
    console.print(Panel.fit(
        "[bold magenta]SAM'S WRITING SUITE[/bold magenta] [white]🖊️[/white]\n"
        "[dim]Kathmandu, Nepal[/dim]\n"
        f"[dim]{now}[/dim]",
        border_style="magenta",
        padding=(1, 4)
    ))

# ═══════════════════════════════
# STATS
# ═══════════════════════════════
def show_stats():
    console.clear()
    console.print(Panel.fit(
        "[bold magenta]📊 YOUR WRITING STATS[/bold magenta]",
        border_style="magenta",
        padding=(1, 4)
    ))

    # Novels
    novels_dir = f"{BASE}/novels"
    novel_table = Table(
        title="📖 Novels",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan"
    )
    novel_table.add_column("Novel", style="white")
    novel_table.add_column("Chapters", style="cyan")
    novel_table.add_column("Words", style="green")

    total_novel_words = 0
    if os.path.exists(novels_dir):
        for novel in os.listdir(novels_dir):
            novel_path = f"{novels_dir}/{novel}"
            if os.path.isdir(novel_path):
                chapters = [f for f in os.listdir(novel_path) if f.endswith(".txt")]
                words = 0
                for ch in chapters:
                    with open(f"{novel_path}/{ch}") as f:
                        words += len(f.read().split())
                total_novel_words += words
                novel_table.add_row(
                    novel.replace("_", " "),
                    str(len(chapters)),
                    f"{words:,}"
                )

    if novel_table.row_count == 0:
        novel_table.add_row("[dim]No novels yet[/dim]", "—", "—")

    # Short stories
    short_dir = f"{BASE}/short-stories"
    short_table = Table(
        title="📄 Short Stories",
        box=box.ROUNDED,
        border_style="green",
        header_style="bold green"
    )
    short_table.add_column("Story", style="white")
    short_table.add_column("Words", style="green")
    short_table.add_column("Saved", style="dim")

    total_short_words = 0
    if os.path.exists(short_dir):
        for story in os.listdir(short_dir):
            if story.endswith(".txt"):
                path = f"{short_dir}/{story}"
                with open(path) as f:
                    content = f.read()
                words = len(content.split())
                total_short_words += words
                modified = os.path.getmtime(path)
                date = datetime.fromtimestamp(modified).strftime("%Y-%m-%d")
                short_table.add_row(
                    story.replace("_", " ").replace(".txt", ""),
                    f"{words:,}",
                    date
                )

    if short_table.row_count == 0:
        short_table.add_row("[dim]No short stories yet[/dim]", "—", "—")

    console.print()
    console.print(novel_table)
    console.print()
    console.print(short_table)

    # Summary
    total_words = total_novel_words + total_short_words
    console.print()
    console.print(Panel(
        f"[bold cyan]Total words written:[/bold cyan] [bold white]{total_words:,}[/bold white]\n"
        f"[bold cyan]Novels in progress:[/bold cyan] [bold white]{novel_table.row_count}[/bold white]\n"
        f"[bold cyan]Short stories:[/bold cyan] [bold white]{short_table.row_count}[/bold white]",
        title="[bold magenta]Summary[/bold magenta]",
        border_style="magenta",
        padding=(1, 2)
    ))

    input("\n[Press Enter to go back]")

# ═══════════════════════════════
# RUN TOOL
# ═══════════════════════════════
def run_tool(script):
    path = f"{BASE}/{script}"
    if os.path.exists(path):
        subprocess.run([sys.executable, path])
    else:
        console.print(f"\n[red]❌ Tool not found: {path}[/red]")
        input("\n[Press Enter to go back]")

# ═══════════════════════════════
# CLEAN STORAGE
# ═══════════════════════════════
def clean_storage():
    console.clear()
    console.print(Panel.fit(
        "[bold red]🗑️  STORAGE MANAGER[/bold red]\n"
        "[dim]Clean up generated files[/dim]",
        border_style="red",
        padding=(1, 4)
    ))

    dirs = {
        "1": ("Output folder", f"{BASE}/output"),
        "2": ("Sessions", f"{BASE}/sessions"),
        "3": ("All novels", f"{BASE}/novels"),
        "4": ("All short stories", f"{BASE}/short-stories"),
    }

    # Show current sizes
    table = Table(
        box=box.ROUNDED,
        border_style="red",
        header_style="bold red"
    )
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Folder", style="white")
    table.add_column("Files", style="dim")
    table.add_column("Size", style="dim")

    for key, (name, path) in dirs.items():
        if os.path.exists(path):
            files = []
            total_size = 0
            for root, _, filenames in os.walk(path):
                for f in filenames:
                    files.append(f)
                    total_size += os.path.getsize(os.path.join(root, f))
            table.add_row(key, name, str(len(files)), f"{total_size // 1024} KB")
        else:
            table.add_row(key, name, "0", "0 KB")

    console.print()
    console.print(table)
    console.print("\n  [dim]5[/dim] → Back to main menu")

    choice = Prompt.ask("\n[bold red]Choose[/bold red]", choices=["1", "2", "3", "4", "5"])

    if choice == "5":
        return

    name, path = dirs[choice]
    if console.input(f"\n[red]⚠️  Delete all in {name}? (y/n): [/red]").lower() == "y":
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path)
            os.makedirs(path)
            console.print(f"\n[green]✅ {name} cleaned![/green]")
        input("\n[Press Enter to go back]")

# ═══════════════════════════════
# MAIN MENU
# ═══════════════════════════════
def main():
    while True:
        show_header()

        console.print(Panel(
            "[bold cyan]1[/bold cyan]  ✍️   Write         → novels and short stories\n"
            "[bold green]2[/bold green]  🔍  Analyze        → update your style profile\n"
            "[bold yellow]3[/bold yellow]  🔎  Research       → quick web research\n"
            "[bold magenta]4[/bold magenta]  📊  Stats          → your writing progress\n"
            "[bold red]5[/bold red]  🗑️   Clean storage  → manage your files\n"
            "[bold dim]6[/bold dim]  🚪  Exit",
            title="[bold magenta]What do you want to do?[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        ))

        choice = Prompt.ask(
            "[bold magenta]Choose[/bold magenta]",
            choices=["1", "2", "3", "4", "5", "6"]
        )

        if choice == "1":
            run_tool("sam_writer.py")
        elif choice == "2":
            run_tool("story_memory.py")
        elif choice == "3":
            run_tool("research.py")
        elif choice == "4":
            show_stats()
        elif choice == "5":
            clean_storage()
        elif choice == "6":
            console.print(Panel(
                "[bold magenta]Happy writing! 🖊️[/bold magenta]\n"
                "[dim]Your stories are safe on your Mac.[/dim]",
                border_style="magenta",
                padding=(1, 2)
            ))
            break

if __name__ == "__main__":
    main()
