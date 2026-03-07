"""Tests for content validation routines."""

import pytest

from hololive_coliseum import content_validator


def test_validate_all_reports_ok() -> None:
    pytest.importorskip("pygame")
    ok, errors = content_validator.validate_all()
    assert isinstance(ok, bool)
    assert isinstance(errors, list)
    assert ok is True


def test_item_catalog_has_required_fields() -> None:
    catalog = content_validator._build_item_catalog()
    assert catalog
    sample = catalog[0]
    assert {"id", "type", "value", "stackable"}.issubset(sample.keys())
