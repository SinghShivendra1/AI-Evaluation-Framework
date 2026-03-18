from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from evaluator.metrics import EvaluationMetrics


@dataclass
class EvaluationBreakdown:
    relevance: float
    completeness: float
    clarity: float


class EvaluationFramework:
    def __init__(self) -> None:
        self.metrics = EvaluationMetrics()

    def evaluate(self, question: str, response: str, expected: str = "") -> Dict:
        issues: List[str] = []

        relevance, relevance_issues = self.metrics.score_relevance(question, response)
        completeness, completeness_issues = self.metrics.score_completeness(response, expected)
        clarity, clarity_issues = self.metrics.score_clarity(response)

        issues.extend(relevance_issues)
        issues.extend(completeness_issues)
        issues.extend(clarity_issues)

        final_score = round((relevance * 0.4) + (completeness * 0.35) + (clarity * 0.25), 2)

        if final_score >= 8.5:
            verdict = "strong"
        elif final_score >= 7.0:
            verdict = "acceptable"
        elif final_score >= 5.0:
            verdict = "needs improvement"
        else:
            verdict = "poor"

        suggestions = self._build_suggestions(issues)

        return {
            "question": question,
            "response": response,
            "expected": expected,
            "breakdown": {
                "relevance": relevance,
                "completeness": completeness,
                "clarity": clarity,
            },
            "score": final_score,
            "issues": sorted(set(issues)),
            "suggestions": suggestions,
            "verdict": verdict,
        }

    def _build_suggestions(self, issues: List[str]) -> List[str]:
        suggestions: List[str] = []

        if "empty response" in issues:
            suggestions.append("Provide a direct answer before refining style or detail.")
        if "low relevance to prompt" in issues:
            suggestions.append("Address the actual question more directly and reuse key prompt concepts.")
        if "partially relevant" in issues:
            suggestions.append("Cover more of the prompt requirements instead of answering only one part.")
        if "too short" in issues or "limited detail" in issues:
            suggestions.append("Add concrete detail, examples, or step-by-step explanation.")
        if "missing important reference concepts" in issues:
            suggestions.append("Include the main points expected in the reference answer.")
        if "sentences may be too long" in issues or "single long block reduces readability" in issues:
            suggestions.append("Break the response into shorter, clearer sentences or bullets.")
        if "unclear trailing thoughts" in issues:
            suggestions.append("Replace incomplete trailing phrases with complete, concise statements.")

        if not suggestions:
            suggestions.append("Response quality is solid. Minor polishing can improve precision and depth.")

        return suggestions
