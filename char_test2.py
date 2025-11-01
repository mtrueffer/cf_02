from textual.app import App, ComposeResult
from textual.widgets import Static, Input
from textual.containers import VerticalScroll
from textual.reactive import var
import unicodedata
import pyperclip

def iter_block(start: int, end: int):
    """Yield (codepoint_hex, char, name) over a unicode range [start, end]."""
    for code in range(start, end + 1):
        try:
            ch = chr(code)
            name = unicodedata.name(ch)
            yield f"{code:04X}", ch, name
        except ValueError:
            continue  # skip unassigned codepoints

UNICODE_BLOCKS = [
    ("Box Drawing",        0x2500, 0x257F),
    ("Block Elements",     0x2580, 0x259F),
    ("Geometric Shapes",   0x25A0, 0x25FF),
    ("Arrows",             0x2190, 0x21FF),
    ("Misc Symbols",       0x2600, 0x26FF),
    ("Dingbats",           0x2700, 0x27BF),
    ("Emoticons",          0x1F600, 0x1F64F),
    ("Transport & Map",    0x1F680, 0x1F6FF),
    ("Misc Symbols & Pictographs", 0x1F300, 0x1F5FF),
    ("Supplemental Symbols & Pictographs", 0x1F900, 0x1F9FF),
]

class UnicodePicker(App):
    """Interactive Unicode symbol picker with live search and clipboard copy."""
    CSS = """
    Screen { layout: vertical; }
    #search { dock: top; height: 3; }
    #symbols { overflow: auto; }
    .block-header { color: cyan; padding: 1 0 0 0; }
    .symbol-line { height: auto; }
    """
    blocks = var(list)

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search by name (e.g. castle, sword, block…)", id="search")
        with VerticalScroll(id="symbols"): pass

    async def on_mount(self) -> None:
        container = self.query_one("#symbols", VerticalScroll)
        self.blocks = []

        for label, start, end in UNICODE_BLOCKS:
            header = Static(f"\n[bold cyan]{label}[/bold cyan]", classes="block-header")
            container.mount(header)
            rows = []
            for code_hex, ch, name in iter_block(start, end):
                text = f"{code_hex}  {ch}  {name}"
                row = Static(text, classes="symbol-line")
                row.data = {"text": text.lower(), "char": ch, "code": code_hex, "name": name}
                container.mount(row)
                rows.append(row)
            self.blocks.append({"header": header, "rows": rows})

    def on_input_changed(self, event: Input.Changed) -> None:
        """Filter symbol rows by search query."""
        if event.input.id != "search":
            return
        q = event.value.strip().lower()
        for block in self.blocks:
            any_match = False
            for row in block["rows"]:
                text = row.data["text"]
                match = q in text if q else True
                row.display = match
                any_match |= match
            block["header"].display = any_match

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Copy first visible symbol to clipboard."""
        if event.input.id != "search":
            return
        for block in self.blocks:
            for row in block["rows"]:
                if row.display:
                    ch = row.data["char"]
                    code = row.data["code"]
                    name = row.data["name"]
                    pyperclip.copy(ch)
                    self.console.print(f"[green]Copied to clipboard:[/green] {code}  {ch}  {name}")
                    return
        self.console.print("[red]No visible symbol to copy.[/red]")

if __name__ == "__main__":
    UnicodePicker().run()
