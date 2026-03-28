"""Tests for the AsciiDoc → Markdown preprocessing pipeline."""

from retrieval.preprocess import (
    _collapse_blanks,
    _convert_markup,
    _extract_title,
    _map_lang,
    _process_conditionals,
)


class TestProcessConditionals:
    def test_keeps_ocp_ifdef(self):
        lines = [
            "ifdef::openshift-enterprise[]",
            "OCP content here",
            "endif::[]",
        ]
        assert _process_conditionals(lines) == ["OCP content here"]

    def test_strips_rosa_ifdef(self):
        lines = [
            "ifdef::openshift-rosa[]",
            "ROSA-only content",
            "endif::[]",
        ]
        assert _process_conditionals(lines) == []

    def test_strips_dedicated_ifdef(self):
        lines = [
            "ifdef::openshift-dedicated[]",
            "OSD content",
            "endif::[]",
        ]
        assert _process_conditionals(lines) == []

    def test_ifndef_strips_ocp(self):
        lines = [
            "ifndef::openshift-enterprise[]",
            "Non-enterprise content",
            "endif::[]",
        ]
        assert _process_conditionals(lines) == []

    def test_ifndef_keeps_rosa_content(self):
        """ifndef::rosa means 'show for non-ROSA' = OCP content."""
        lines = [
            "ifndef::openshift-rosa[]",
            "Kept for OCP",
            "endif::[]",
        ]
        assert _process_conditionals(lines) == ["Kept for OCP"]

    def test_mixed_content_around_conditionals(self):
        lines = [
            "Before",
            "ifdef::openshift-rosa[]",
            "ROSA only",
            "endif::[]",
            "After",
        ]
        assert _process_conditionals(lines) == ["Before", "After"]

    def test_ifeval_stripped_entirely(self):
        lines = [
            'ifeval::["{context}" == "foo"]',
            ":some-flag:",
            "endif::[]",
            "Regular content",
        ]
        assert _process_conditionals(lines) == ["Regular content"]

    def test_nested_conditionals(self):
        lines = [
            "ifdef::openshift-enterprise[]",
            "Outer OCP",
            "ifdef::openshift-rosa[]",
            "Nested ROSA (should be stripped)",
            "endif::[]",
            "Still OCP",
            "endif::[]",
        ]
        result = _process_conditionals(lines)
        assert "Outer OCP" in result
        assert "Nested ROSA (should be stripped)" not in result
        assert "Still OCP" in result


class TestConvertMarkup:
    def test_heading_conversion(self):
        lines = ["== My Heading"]
        assert _convert_markup(lines) == ["## My Heading"]

    def test_deep_heading(self):
        lines = ["==== Deep Heading"]
        assert _convert_markup(lines) == ["#### Deep Heading"]

    def test_strips_metadata(self):
        lines = [":_mod-docs-content-type: PROCEDURE", '[id="some-id"]', "Real content"]
        assert _convert_markup(lines) == ["Real content"]

    def test_strips_include(self):
        lines = ["include::modules/foo.adoc[leveloffset=+1]"]
        assert _convert_markup(lines) == []

    def test_xref_inline(self):
        lines = ["See xref:some/path.adoc#anchor[the docs] for details."]
        assert _convert_markup(lines) == ["See the docs for details."]

    def test_link_inline(self):
        lines = ["Visit link:https://example.com[Example] now."]
        assert _convert_markup(lines) == ["Visit [Example](https://example.com) now."]

    def test_ordered_list(self):
        lines = [". First item", ". Second item"]
        assert _convert_markup(lines) == ["1. First item", "1. Second item"]

    def test_unordered_list(self):
        lines = ["* Bullet one", "** Nested bullet"]
        assert _convert_markup(lines) == ["- Bullet one", "- Nested bullet"]

    def test_source_block(self):
        lines = ["[source,yaml]", "----", "key: value", "----"]
        assert _convert_markup(lines) == ["```yaml", "key: value", "```"]

    def test_source_block_terminal_maps_to_bash(self):
        lines = ["[source,terminal]", "----", "oc get pods", "----"]
        assert _convert_markup(lines) == ["```bash", "oc get pods", "```"]

    def test_admonition_block(self):
        lines = ["[NOTE]", "====", "This is a note.", "===="]
        assert _convert_markup(lines) == ["> **NOTE:** This is a note."]

    def test_strips_role_line(self):
        lines = ['[role="_abstract"]', "Content here"]
        assert _convert_markup(lines) == ["Content here"]

    def test_strips_discrete(self):
        lines = ["[discrete]", "== Hidden heading"]
        assert _convert_markup(lines) == ["## Hidden heading"]

    def test_list_continuation_stripped(self):
        lines = ["1. Step one", "+", "Details about step one"]
        assert _convert_markup(lines) == ["1. Step one", "Details about step one"]


class TestMapLang:
    def test_known_languages(self):
        assert _map_lang("terminal") == "bash"
        assert _map_lang("yaml") == "yaml"
        assert _map_lang("json") == "json"
        assert _map_lang("sh") == "bash"

    def test_language_with_options(self):
        assert _map_lang("terminal,subs=+quotes") == "bash"
        assert _map_lang("yaml,options=nowrap") == "yaml"

    def test_unknown_language_passed_through(self):
        assert _map_lang("ruby") == "ruby"

    def test_empty_string(self):
        assert _map_lang("") == ""


class TestCollapseBlanks:
    def test_collapses_multiple_blanks(self):
        lines = ["a", "", "", "", "b"]
        assert _collapse_blanks(lines) == ["a", "", "b"]

    def test_preserves_single_blank(self):
        lines = ["a", "", "b"]
        assert _collapse_blanks(lines) == ["a", "", "b"]

    def test_no_blanks(self):
        lines = ["a", "b", "c"]
        assert _collapse_blanks(lines) == ["a", "b", "c"]


class TestExtractTitle:
    def test_extracts_first_h1(self):
        assert _extract_title("# My Title\n\nSome body") == "My Title"

    def test_returns_empty_when_no_title(self):
        assert _extract_title("Just some text\nNo heading") == ""

    def test_ignores_deeper_headings(self):
        assert _extract_title("## Not a title\n# Real Title") == "Real Title"
