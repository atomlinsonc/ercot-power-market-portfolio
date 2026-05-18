"""Helpers for organizing blog metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlogPost:
    """Minimal metadata for a portfolio blog post."""

    title: str
    date: str
    category: str
    summary: str
    path: str

