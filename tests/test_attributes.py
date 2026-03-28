"""Tests for AsciiDoc attribute resolution."""

from retrieval.attributes import _resolve, resolve_text


class TestResolve:
    def test_simple_substitution(self):
        attrs = {"product-title": "OpenShift"}
        assert _resolve("{product-title}", attrs) == "OpenShift"

    def test_multiple_substitutions(self):
        attrs = {"product-title": "OpenShift", "product-version": "4.21"}
        result = _resolve("{product-title} {product-version}", attrs)
        assert result == "OpenShift 4.21"

    def test_missing_attr_preserved(self):
        attrs = {}
        assert _resolve("{unknown-attr}", attrs) == "{unknown-attr}"

    def test_no_placeholders(self):
        attrs = {"foo": "bar"}
        assert _resolve("plain text", attrs) == "plain text"


class TestResolveText:
    def test_nested_resolution(self):
        attrs = {"inner": "World", "outer": "Hello {inner}"}
        assert resolve_text("{outer}", attrs) == "Hello World"

    def test_deeply_nested(self):
        attrs = {"a": "{b}", "b": "{c}", "c": "done"}
        assert resolve_text("{a}", attrs) == "done"

    def test_plain_text_unchanged(self):
        assert resolve_text("no refs here", {}) == "no refs here"
