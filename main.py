import argparse
import json
from evaluator.framework import EvaluationFramework


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate AI-generated responses using rule-based criteria.")
    parser.add_argument("--question", type=str, help="Question or prompt given to the model.")
    parser.add_argument("--response", type=str, help="Model response to evaluate.")
    parser.add_argument("--expected", type=str, default="", help="Expected answer or reference answer.")
    parser.add_argument("--input-file", type=str, help="Path to a JSON file with question, response, and optional expected.")
    return parser.parse_args()


def load_input_from_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    args = parse_args()

    if args.input_file:
        data = load_input_from_file(args.input_file)
        question = data.get("question", "")
        response = data.get("response", "")
        expected = data.get("expected", "")
    else:
        question = args.question or ""
        response = args.response or ""
        expected = args.expected or ""

    framework = EvaluationFramework()
    result = framework.evaluate(question=question, response=response, expected=expected)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
