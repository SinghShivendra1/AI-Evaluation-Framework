from __future__ import annotations

from typing import List, Tuple


class EvaluationMetrics:
    """Rule-based metrics for quick evaluation of model responses."""

    def score_relevance(self, question: str, response: str) -> Tuple[float, List[str]]:
        issues: List[str] = []
        if not response.strip():
            return 0.0, ["empty response"]

        question_tokens = {token.lower().strip(".,!?()[]{}:;\"'") for token in question.split() if len(token) > 3}
        response_tokens = {token.lower().strip(".,!?()[]{}:;\"'") for token in response.split()}

        if not question_tokens:
            return 8.0, issues

        overlap = len(question_tokens & response_tokens)
        ratio = overlap / max(len(question_tokens), 1)

        if ratio >= 0.5:
            return 9.0, issues
        if ratio >= 0.25:
            issues.append("partially relevant")
            return 7.0, issues

        issues.append("low relevance to prompt")
        return 4.0, issues

    def score_completeness(self, response: str, expected: str = "") -> Tuple[float, List[str]]:
        issues: List[str] = []
        word_count = len(response.split())

        if word_count < 5:
            issues.append("too short")
            return 3.0, issues
        if word_count < 20:
            issues.append("limited detail")
            base = 6.0
        else:
            base = 8.0

        if expected:
            expected_tokens = {t.lower().strip(".,!?()[]{}:;\"'") for t in expected.split() if len(t) > 3}
            response_tokens = {t.lower().strip(".,!?()[]{}:;\"'") for t in response.split()}
            missing = expected_tokens - response_tokens
            if expected_tokens and len(missing) > len(expected_tokens) * 0.5:
                issues.append("missing important reference concepts")
                base -= 2.0

        return max(base, 0.0), issues

    def score_clarity(self, response: str) -> Tuple[float, List[str]]:
        issues: List[str] = []
        if not response.strip():
            return 0.0, ["empty response"]

        sentences = [s for s in response.replace("\n", " ").split(".") if s.strip()]
        avg_len = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)

        score = 8.5
        if avg_len > 30:
            issues.append("sentences may be too long")
            score -= 1.5
        if response.count("...") > 1:
            issues.append("unclear trailing thoughts")
            score -= 1.0
        if len(sentences) == 1 and len(response.split()) > 35:
            issues.append("single long block reduces readability")
            score -= 1.0

        return max(score, 0.0), issues
