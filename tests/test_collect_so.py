"""Tests for Stack Overflow benchmark collector utilities."""

from eval.collect_so_benchmark import _clean_title, _infer_topic, _is_quality


class TestInferTopic:
    def test_specific_tag_wins(self):
        assert _infer_topic(["openshift", "openshift-operator"]) == "operators"

    def test_networking_tags(self):
        assert _infer_topic(["openshift", "networkpolicy"]) == "networking"
        assert _infer_topic(["openshift-router"]) == "networking"

    def test_general_fallback(self):
        assert _infer_topic(["openshift"]) == "general"
        assert _infer_topic([]) == "general"

    def test_storage(self):
        assert _infer_topic(["persistent-volume"]) == "storage"

    def test_auth(self):
        assert _infer_topic(["openshift-rbac"]) == "authentication"


class TestCleanTitle:
    def test_adds_question_mark(self):
        assert _clean_title("How to install OpenShift") == "How to install OpenShift?"

    def test_preserves_question_mark(self):
        assert _clean_title("How to install?") == "How to install?"

    def test_strips_trailing_period(self):
        assert _clean_title("Install OpenShift.") == "Install OpenShift?"

    def test_decodes_html_entities(self):
        assert _clean_title("Can&#39;t deploy pods") == "Can't deploy pods?"

    def test_strips_whitespace(self):
        assert _clean_title("  spaced  ") == "spaced?"


class TestIsQuality:
    def _make_q(self, **overrides):
        base = {
            "score": 5,
            "is_answered": True,
            "title": "How do I configure OpenShift networking properly?",
        }
        base.update(overrides)
        return base

    def test_passes_good_question(self):
        assert _is_quality(self._make_q(), min_score=1) is True

    def test_rejects_low_score(self):
        assert _is_quality(self._make_q(score=0), min_score=1) is False

    def test_rejects_unanswered(self):
        assert _is_quality(self._make_q(is_answered=False), min_score=1) is False

    def test_rejects_closed(self):
        assert (
            _is_quality(self._make_q(closed_reason="duplicate"), min_score=1) is False
        )

    def test_rejects_short_title(self):
        assert _is_quality(self._make_q(title="Short"), min_score=1) is False

    def test_rejects_unwanted_patterns(self):
        assert (
            _is_quality(
                self._make_q(title="please help me with OpenShift"), min_score=1
            )
            is False
        )
