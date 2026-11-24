"""The hand-written CSV parser behind review exports."""

import pytest

from proofline._csv import parse_csv


def test_simple_rows() -> None:
    assert parse_csv("a,b,c\n1,2,3") == [["a", "b", "c"], ["1", "2", "3"]]


def test_trailing_newline_adds_no_row() -> None:
    assert parse_csv("a,b\n") == [["a", "b"]]


def test_empty_text_has_no_records() -> None:
    assert parse_csv("") == []


def test_empty_fields() -> None:
    assert parse_csv("a,,c\n,,") == [["a", "", "c"], ["", "", ""]]


def test_quoted_field_keeps_its_comma() -> None:
    assert parse_csv('"a,b",c') == [["a,b", "c"]]


def test_escaped_quote_inside_a_quoted_field() -> None:
    assert parse_csv('"say ""hi"""') == [['say "hi"']]


def test_quoted_field_keeps_its_newline() -> None:
    assert parse_csv('"a\nb",c') == [["a\nb", "c"]]


def test_empty_quoted_field() -> None:
    assert parse_csv('""') == [[""]]


def test_crlf_line_endings() -> None:
    assert parse_csv("a,b\r\n1,2\r\n") == [["a", "b"], ["1", "2"]]


def test_lone_cr_line_endings() -> None:
    assert parse_csv("a,b\r1,2") == [["a", "b"], ["1", "2"]]


def test_spaces_are_part_of_the_field() -> None:
    assert parse_csv(" a ,b") == [[" a ", "b"]]


def test_unterminated_quote_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_csv('"abc')


def test_text_after_a_closing_quote_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_csv('"a"x')
