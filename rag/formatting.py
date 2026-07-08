import os
from collections.abc import Iterable

from langchain_core.documents import Document


def build_context(documents: Iterable[Document]) -> str:
    context_parts = []
    for index, doc in enumerate(documents, start=1):
        context_parts.append(
            f"[data {index}]: data: {doc.page_content} | metadata: {doc.metadata}"
        )
    return "\n".join(context_parts)


def _source_name(document: Document) -> str | None:
    source = document.metadata.get("source")
    if not source:
        return None
    return os.path.basename(str(source))


def format_sources(documents: Iterable[Document]) -> str:
    source_names = sorted(
        {source_name for doc in documents if (source_name := _source_name(doc))}
    )
    if not source_names:
        return ""

    return "Sources:\n" + "\n".join(f"- {source_name}" for source_name in source_names)


def append_sources(answer: str, documents: Iterable[Document]) -> str:
    sources = format_sources(documents)
    if not sources:
        return answer.strip()
    return f"{answer.strip()}\n\n{sources}"
