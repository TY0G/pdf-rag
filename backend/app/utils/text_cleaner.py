import re


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_summary(texts: list[str], max_chars: int = 220) -> str:
    merged = " ".join([t.strip() for t in texts if t.strip()])
    merged = re.sub(r"\s+", " ", merged)
    return merged[:max_chars] + ("..." if len(merged) > max_chars else "")
