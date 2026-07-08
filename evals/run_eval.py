import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {"question", "expected_tool", "category"}


def load_cases(path: str) -> list[dict[str, Any]]:
    cases = []
    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            case = json.loads(line)
            missing_fields = REQUIRED_FIELDS - set(case)
            if missing_fields:
                fields = ", ".join(sorted(missing_fields))
                raise ValueError(f"{path}:{line_number} missing required fields: {fields}")
            cases.append(case)
    return cases


def summarize_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    expected_tools = Counter(case["expected_tool"] for case in cases)
    categories = Counter(case["category"] for case in cases)
    return {
        "total_cases": len(cases),
        "expected_tools": dict(sorted(expected_tools.items())),
        "categories": dict(sorted(categories.items())),
        "safety_cases": categories.get("safety", 0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize the local AI-agent eval dataset.")
    parser.add_argument(
        "--cases",
        default=str(Path(__file__).with_name("questions.jsonl")),
        help="Path to a JSONL eval dataset.",
    )
    args = parser.parse_args()

    cases = load_cases(args.cases)
    print(json.dumps(summarize_cases(cases), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
