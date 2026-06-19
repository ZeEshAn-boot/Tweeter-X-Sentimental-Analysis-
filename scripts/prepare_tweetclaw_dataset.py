"""Convert reviewed TweetClaw exports into a local app dataset."""

from __future__ import annotations

import argparse
import csv
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any


FIELDNAMES = ("target", "ids", "date", "flag", "user", "text")

FIELD_PATHS = {
    "text": (
        ("text",),
        ("tweet",),
        ("full_text",),
        ("fullText",),
        ("rawContent",),
        ("data", "text"),
        ("tweet", "text"),
        ("legacy", "full_text"),
    ),
    "ids": (
        ("id",),
        ("tweet_id",),
        ("tweetId",),
        ("rest_id",),
        ("data", "id"),
        ("tweet", "id"),
    ),
    "date": (
        ("created_at",),
        ("createdAt",),
        ("date",),
        ("timestamp",),
        ("data", "created_at"),
        ("tweet", "created_at"),
    ),
    "user": (
        ("author_username",),
        ("username",),
        ("screen_name",),
        ("author", "username"),
        ("author", "screen_name"),
        ("user", "username"),
        ("user", "screen_name"),
        ("tweet", "author", "username"),
        ("tweet", "author", "screen_name"),
    ),
}


def value_at_path(record: Mapping[str, Any], path: tuple[str, ...]) -> str:
    current: Any = record
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return ""
        current = current[key]
    if current is None or isinstance(current, (Mapping, list)):
        return ""
    return str(current).strip()


def first_value(record: Mapping[str, Any], field: str) -> str:
    for path in FIELD_PATHS[field]:
        value = value_at_path(record, path)
        if value:
            return value
    return ""


def normalize_record(record: Mapping[str, Any]) -> dict[str, str] | None:
    text = " ".join(first_value(record, "text").split())
    if not text:
        return None
    ids = first_value(record, "ids")
    return {
        "target": "4",
        "ids": ids,
        "date": first_value(record, "date"),
        "flag": "NO_QUERY",
        "user": first_value(record, "user") or "tweetclaw_export",
        "text": text,
    }


def records_from_csv(path: Path) -> Iterable[Mapping[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        yield from csv.DictReader(handle)


def records_from_json_data(data: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(data, list):
        for item in data:
            if isinstance(item, Mapping):
                yield item
        return

    if isinstance(data, Mapping):
        for key in ("tweets", "data", "items", "results"):
            value = data.get(key)
            if isinstance(value, list):
                yield from records_from_json_data(value)
                return
        yield data


def records_from_json_or_jsonl(path: Path) -> Iterable[Mapping[str, Any]]:
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        return

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                item = json.loads(stripped)
            except json.JSONDecodeError as error:
                message = f"Invalid JSONL on line {line_number}: {error}"
                raise ValueError(message) from error
            if isinstance(item, Mapping):
                yield item
        return

    yield from records_from_json_data(data)


def load_records(path: Path) -> Iterable[Mapping[str, Any]]:
    if path.suffix.lower() == ".csv":
        yield from records_from_csv(path)
        return
    yield from records_from_json_or_jsonl(path)


def prepare_rows(input_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for record in load_records(input_path):
        row = normalize_record(record)
        if row is None:
            continue
        dedupe_key = row["ids"] or row["text"].casefold()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        rows.append(row)
    return rows


def write_dataset(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert reviewed TweetClaw JSON, JSONL, or CSV exports into tweets.csv."
    )
    parser.add_argument("input", type=Path, help="Path to the TweetClaw export.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tweets.csv"),
        help="Output path. Defaults to tweets.csv.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = prepare_rows(args.input)
    if not rows:
        raise SystemExit("No tweet text found in the input export.")
    write_dataset(rows, args.output)


if __name__ == "__main__":
    main()
