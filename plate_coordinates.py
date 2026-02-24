"""Helpers for extracting non-empty well coordinates from a plate plan."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

import pandas as pd


def extract_plate_coordinates(
    plate_plan: Iterable[Iterable[Any]],
    ignored_values: set[str] | None = None,
) -> tuple[dict[Any, list[str]], list[str]]:
    """Return (sample->coordinates mapping, flat coordinate list).

    Coordinates are generated as A1, A2, ... using row index -> letters and
    column index -> 1-based numbers.
    """
    if ignored_values is None:
        ignored_values = {"0_", "_", ""}

    coordinates_dict: defaultdict[Any, list[str]] = defaultdict(list)
    non_empty_coordinates: list[str] = []

    for row_idx, row in enumerate(plate_plan):
        for col_idx, sample_name in enumerate(row):
            sample_text = "" if pd.isna(sample_name) else str(sample_name).strip()
            if sample_text in ignored_values:
                continue

            coordinate = f"{chr(65 + row_idx)}{col_idx + 1}"
            non_empty_coordinates.append(coordinate)
            coordinates_dict[sample_name].append(coordinate)

    return dict(coordinates_dict), non_empty_coordinates
