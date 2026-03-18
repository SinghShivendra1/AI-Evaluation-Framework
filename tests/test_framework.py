from evaluator.framework import EvaluationFramework


def test_evaluation_returns_expected_keys():
    framework = EvaluationFramework()
    result = framework.evaluate(
        question="What is AI?",
        response="AI is the simulation of human intelligence in machines.",
        expected="AI is a field of computer science focused on building systems that perform tasks requiring intelligence.",
    )

    assert "score" in result
    assert "verdict" in result
    assert "breakdown" in result
    assert isinstance(result["issues"], list)
    assert isinstance(result["suggestions"], list)


def test_empty_response_scores_poorly():
    framework = EvaluationFramework()
    result = framework.evaluate(question="Explain AI", response="", expected="Artificial intelligence is ...")

    assert result["score"] < 5.0
    assert result["verdict"] == "poor"
