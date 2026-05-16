import csv
import re
import unicodedata
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DESTINATIONS_PATH = DATA_DIR / "destinations_catalog.csv"
ARTICLES_PATH = DATA_DIR / "articles_tourism_rag.csv"
MAX_CONTEXT_CHARS = 800

DESTINATIONS_CACHE: list[dict[str, str]] = []
ARTICLES_CACHE: list[dict[str, str]] = []
_RAG_LOADED = False
LAST_MATCH_COUNTS = {
    "destinations": 0,
    "articles": 0,
}

STOPWORDS = {
    "and",
    "avec",
    "budget",
    "days",
    "for",
    "help",
    "jour",
    "jours",
    "plan",
    "pour",
    "the",
    "trip",
    "voyage",
    "with",
}

INTENT_KEYWORDS = {
    "destination_recommendation": {"culture", "budget", "activities", "best"},
    "itinerary_request": {"activities", "areas", "duration", "transport", "food"},
    "destination_comparison": {"budget", "pros", "cons", "best", "safety"},
    "budget_optimization": {"budget", "transport", "affordable", "cheap"},
    "safety_question": {"safety", "safe", "transport"},
    "family_trip": {"family", "safety", "transport"},
    "activity_search": {"activities", "visit", "areas", "food"},
}


def load_rag_data() -> None:
    """Load local CSV rows once into memory. Missing files leave empty caches."""

    global _RAG_LOADED

    if _RAG_LOADED:
        return

    DESTINATIONS_CACHE[:] = _load_csv(DESTINATIONS_PATH)
    ARTICLES_CACHE[:] = _load_csv(ARTICLES_PATH)
    _RAG_LOADED = True


def retrieve_travel_context(user_message: str, analysis: Any) -> str:
    """Return a small local CSV context block for the current travel request."""

    load_rag_data()

    entities = getattr(analysis, "entities", {}) or {}
    intent = getattr(analysis, "intent", "") or ""
    destination_names = _find_destination_names(user_message, entities)
    query_tokens = _query_tokens(user_message, entities, intent)

    destination_rows = _destination_matches(destination_names, query_tokens, entities, intent)
    article_rows = _article_matches(destination_names, query_tokens, intent, destination_rows)
    LAST_MATCH_COUNTS["destinations"] = len(destination_rows)
    LAST_MATCH_COUNTS["articles"] = len(article_rows)

    sections = []
    if destination_rows:
        sections.append(_format_destination_context(destination_rows[0]))

    article_summaries = [_article_summary(row) for row in article_rows[:2]]
    article_summaries = [summary for summary in article_summaries if summary]
    if article_summaries:
        sections.append("Travel guide context:\n" + "\n".join(f"- {summary}" for summary in article_summaries))

    return _trim_context("\n\n".join(sections), MAX_CONTEXT_CHARS)


def get_last_match_counts() -> dict[str, int]:
    """Return match counts from the latest retrieval call for temporary debug logs."""

    return dict(LAST_MATCH_COUNTS)


def _load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            {key: (value or "").strip() for key, value in row.items() if key}
            for row in reader
        ]


def _find_destination_names(user_message: str, entities: dict[str, str]) -> list[str]:
    found: list[str] = []
    message_text = _normalize(user_message)

    for value in [entities.get("destination", ""), entities.get("destinations", "")]:
        for candidate in re.split(r"[,;/]", value):
            _append_unique(found, candidate)

    known_names = {
        row.get("destination", "")
        for row in DESTINATIONS_CACHE + ARTICLES_CACHE
        if row.get("destination")
    }
    for name in known_names:
        normalized_name = _normalize(name)
        if normalized_name and re.search(rf"\b{re.escape(normalized_name)}\b", message_text):
            _append_unique(found, name)

    return found


def _destination_matches(
    destination_names: list[str],
    query_tokens: set[str],
    entities: dict[str, str],
    intent: str,
) -> list[dict[str, str]]:
    if destination_names:
        names = {_normalize(name) for name in destination_names}
        return [
            row
            for row in DESTINATIONS_CACHE
            if _normalize(row.get("destination", "")) in names
        ][:2]

    style_tokens = _tokens(entities.get("travel_style", ""))
    budget = _normalize(entities.get("budget", ""))
    intent_tokens = INTENT_KEYWORDS.get(intent, set())
    if not style_tokens and not budget and not intent_tokens:
        return []

    scored = []

    for row in DESTINATIONS_CACHE:
        searchable = " ".join(
            row.get(field, "")
            for field in [
                "destination",
                "country",
                "type",
                "budget_level",
                "best_for",
                "top_areas",
                "top_activities",
                "transport_notes",
                "pros",
                "cons",
            ]
        )
        score = _score_text(searchable, query_tokens | style_tokens | intent_tokens)
        if budget and budget in _normalize(row.get("budget_level", "")):
            score += 4
        if style_tokens and style_tokens.intersection(_tokens(row.get("type", ""))):
            score += 3
        if score > 0:
            scored.append((score, row))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [row for _, row in scored[:2]]


def _article_matches(
    destination_names: list[str],
    query_tokens: set[str],
    intent: str,
    destination_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    names = {_normalize(name) for name in destination_names}
    if not names:
        names = {
            _normalize(row.get("destination", ""))
            for row in destination_rows
            if row.get("destination")
        }

    intent_tokens = INTENT_KEYWORDS.get(intent, set())
    scored = []

    for row in ARTICLES_CACHE:
        row_destination = _normalize(row.get("destination", ""))
        if names and row_destination not in names:
            continue

        searchable = " ".join(
            row.get(field, "")
            for field in ["destination", "category", "title", "content_summary", "key_facts"]
        )
        score = _score_text(searchable, query_tokens | intent_tokens)
        if names and row_destination in names:
            score += 6
        if _normalize(row.get("category", "")) in intent_tokens:
            score += 2
        if score > 0:
            scored.append((score, row))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [row for _, row in scored[:2]]


def _format_destination_context(row: dict[str, str]) -> str:
    destination = row.get("destination", "")
    country = row.get("country", "")
    best_for = _compact_items(row.get("best_for", ""), 3)
    top_areas = _compact_items(row.get("top_areas", ""), 3)
    transport = _compact_sentence(row.get("transport_notes", ""), 95)
    safety = _compact_sentence(row.get("safety_note", ""), 80)
    budget = row.get("budget_level", "")

    lines = [f"Destination context:\n- {destination}, {country}".rstrip(", ")]
    if best_for:
        lines.append(f"- Best for: {best_for}")
    if top_areas:
        lines.append(f"- Top areas: {top_areas}")
    budget_parts = []
    if budget:
        budget_parts.append(f"{budget} budget")
    if transport:
        budget_parts.append(transport)
    if budget_parts:
        lines.append(f"- Budget notes: {'; '.join(budget_parts)}")
    if safety:
        lines.append(f"- Safety note: {safety}")

    return "\n".join(lines)


def _article_summary(row: dict[str, str]) -> str:
    summary = row.get("content_summary", "") or row.get("key_facts", "")
    return _compact_sentence(summary, 150)


def _query_tokens(user_message: str, entities: dict[str, str], intent: str) -> set[str]:
    intent_text = " ".join(INTENT_KEYWORDS.get(intent, set()))
    return _tokens(
        " ".join(
            [
                user_message,
                entities.get("travel_style", ""),
                entities.get("budget", ""),
                entities.get("destination", ""),
                entities.get("destinations", ""),
                intent_text,
            ]
        )
    )


def _score_text(text: str, query_tokens: set[str]) -> int:
    normalized_text = _normalize(text)
    return sum(1 for token in query_tokens if token and token in normalized_text)


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]{3,}", _normalize(value))
        if token not in STOPWORDS
    }


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()


def _append_unique(items: list[str], value: str) -> None:
    cleaned = (value or "").strip()
    if not cleaned:
        return

    keys = {_normalize(item) for item in items}
    if _normalize(cleaned) not in keys:
        items.append(cleaned)


def _compact_items(value: str, max_items: int) -> str:
    parts = [part.strip() for part in re.split(r"[;,]", value or "") if part.strip()]
    return ", ".join(parts[:max_items])


def _compact_sentence(value: str, limit: int) -> str:
    compacted = re.sub(r"\s+", " ", value or "").strip()
    if len(compacted) <= limit:
        return compacted
    return compacted[: limit - 3].rstrip(" ;,.-") + "..."


def _trim_context(context: str, limit: int) -> str:
    if len(context) <= limit:
        return context

    trimmed = context[:limit].rsplit("\n", 1)[0].strip()
    if trimmed:
        return trimmed

    return context[: limit - 3].rstrip(" ;,.-") + "..."
