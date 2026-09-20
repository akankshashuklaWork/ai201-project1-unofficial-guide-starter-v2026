"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_sections(text: str) -> tuple[str, list[tuple[str | None, str]]]:
    """
    Split one document's text into (title, sections).

    Each section is a (heading, body) pair, cut at the document's own
    `## Heading` markers rather than at a fixed character count. The intro
    paragraph before the first heading (if there is one) comes back as a
    section with heading=None. A document with no intro paragraph at all
    (several of the cross-town guides jump straight from the title into
    "## Something") produces no such section, rather than an empty one.
    """
    lines = text.strip().split("\n", 1)
    title = lines[0].lstrip("#").strip()
    rest = lines[1] if len(lines) > 1 else ""

    parts = re.split(r"\n##\s+(.+)", rest)

    sections: list[tuple[str | None, str]] = []
    preamble = parts[0].strip()
    if preamble:
        sections.append((None, preamble))

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if body:
            sections.append((heading, body))

    return title, sections


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents at their own `## Heading` markers instead of at a fixed
    character count.

    Why: `city_guides` documents are already organised into labelled sections
    (Getting there, Eat and drink, ...), and the fixed 800-character chunker
    cuts straight through them — Milestone 1 measured this as 51 chunks from
    14 documents, with the shortest chunk only 24 characters and several
    chunks starting or ending mid-word. Cutting at the headings the documents
    already have avoids that: every chunk is a complete section, and there's
    no character count to tune because the boundary isn't arbitrary.

    Every chunk is also prefixed with its document's title. A section like
    "Practical notes" reads fine inside its document, but on its own — which
    is how retrieval hands it to the model — it never says which town it's
    about. `guide_kestrelford.md`'s "Practical notes" section, sampled with
    the old chunker, was exactly this: a chunk about a hospital with no
    indication of which town's hospital. Prefixing the title fixes that
    without changing what the section says.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        title, sections = _split_sections(doc.text)
        for index, (heading, body) in enumerate(sections):
            text = f"{title} — {heading}\n\n{body}" if heading else f"{title}\n\n{body}"
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
