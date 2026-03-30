from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
    # LLM-powered action item extraction using Ollama (llama3.1:8b)
    # Generated for "Scaffold a New Feature" - Week 2 Assignment

from typing import List
import json

def extract_action_items_llm(text: str) -> List[str]:
    """
    Uses Ollama (llama3.1:8b) to extract actionable items as a list of strings from the input text.

    Returns an empty list if the LLM's response cannot be parsed as a JSON array of strings.
    """
        # Import here to avoid top-level dependency for users who don't need LLM mode
    try:
        import ollama
    except ImportError:
            # Ollama Python client not installed
        return []

    prompt = (
        "Extract a list of actionable tasks from the following text as a JSON array of strings. "
        "Only return the JSON array itself (no explanation or prose).\n\n"
        f"Text:\n{text.strip()}\n\n"
        "JSON:"
    )

    try:
        response = ollama.chat(
            model="llama3.1:8b",
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            options={
                "temperature": 0.1,
            },
        )

        output = response["message"]["content"].strip()
        # If model wraps JSON in code blocks, strip them out
        if output.startswith("```"):
            output = output.strip("`")
            # try to find JSON inside code block
            lines = output.splitlines()
            json_strs = [line for line in lines if not line.strip().startswith("json")]
            output = "\n".join(json_strs).strip()

            # Parse as JSON array of strings
        data = json.loads(output)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data
        else:
            return []
    except Exception:
        return []
