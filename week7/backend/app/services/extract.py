import re


ACTION_PREFIX_RE = re.compile(r"^(?P<prefix>todo|action|task|bug)\s*:\s*(?P<body>.*)$", re.IGNORECASE)


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip().lstrip("- ").strip() for line in text.splitlines() if line.strip()]
    results: list[str] = []
    for line in lines:
        match = ACTION_PREFIX_RE.match(line)
        if match:
            prefix = match.group("prefix").upper()
            body = match.group("body").strip()
            if body:
                results.append(f"{prefix}: {body}")
            continue

        if line.endswith("!"):
            results.append(line)

    return results


