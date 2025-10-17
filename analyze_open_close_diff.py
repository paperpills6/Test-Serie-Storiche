from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SVG_WIDTH = 1000
SVG_HEIGHT = 600
MARGIN_LEFT = 80
MARGIN_RIGHT = 40
MARGIN_TOP = 50
MARGIN_BOTTOM = 80


def read_price_rows(csv_path: Path) -> Iterable[Tuple[datetime, float, float]]:
    with csv_path.open("r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row["Date"], "%m/%d/%Y")
            open_price = float(row["Open"].replace("$", ""))
            close_price = float(row["Close/Last"].replace("$", ""))
            yield date, open_price, close_price


def compute_monthly_average_diff(
    rows: Iterable[Tuple[datetime, float, float]]
) -> List[Tuple[datetime, float]]:
    grouped: Dict[Tuple[int, int], List[float]] = defaultdict(list)

    for date, open_price, close_price in rows:
        key = (date.year, date.month)
        grouped[key].append(close_price - open_price)

    averaged: List[Tuple[datetime, float]] = []
    for (year, month), diffs in grouped.items():
        avg_diff = sum(diffs) / len(diffs)
        averaged.append((datetime(year, month, 1), avg_diff))

    averaged.sort(key=lambda item: item[0])
    return averaged


def scale_points(points: List[Tuple[datetime, float]]):
    dates = [pt[0] for pt in points]
    values = [pt[1] for pt in points]

    min_date, max_date = min(dates), max(dates)
    min_value, max_value = min(values), max(values)

    if max_value == min_value:
        max_value += 1
        min_value -= 1

    total_width = SVG_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    total_height = SVG_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

    def date_to_x(date: datetime) -> float:
        span = (max_date - min_date).days or 1
        return MARGIN_LEFT + ((date - min_date).days / span) * total_width

    def value_to_y(value: float) -> float:
        return MARGIN_TOP + (1 - (value - min_value) / (max_value - min_value)) * total_height

    scaled = [(date_to_x(date), value_to_y(value)) for date, value in points]
    return scaled, (min_date, max_date, min_value, max_value, date_to_x, value_to_y)


def build_svg(points: List[Tuple[datetime, float]]) -> str:
    scaled_points, (min_date, max_date, min_value, max_value, date_to_x, value_to_y) = scale_points(points)
    path_data = " ".join(f"L{x:.2f},{y:.2f}" for x, y in scaled_points)
    if path_data:
        path_data = "M" + path_data[1:]

    # Y-axis ticks
    tick_count = 6
    value_ticks = [min_value + i * (max_value - min_value) / (tick_count - 1) for i in range(tick_count)]

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
        "<style>text { font-family: Arial, sans-serif; font-size: 14px; }</style>",
        f'<rect x="0" y="0" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="white" stroke="none"/>',
        f'<path d="M{MARGIN_LEFT},{MARGIN_TOP} V{SVG_HEIGHT - MARGIN_BOTTOM} H{SVG_WIDTH - MARGIN_RIGHT}" stroke="black" fill="none" stroke-width="2"/>',
        f'<path d="{path_data}" fill="none" stroke="#1f77b4" stroke-width="2"/>' if path_data else "",
        f'<text x="{SVG_WIDTH / 2}" y="{MARGIN_TOP - 15}" text-anchor="middle">Average Difference Between Close and Open Prices (Monthly)</text>',
        f'<text x="{SVG_WIDTH / 2}" y="{SVG_HEIGHT - 20}" text-anchor="middle">Month</text>',
        f'<text x="{MARGIN_LEFT - 60}" y="{MARGIN_TOP + (SVG_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM)/2}" text-anchor="middle" transform="rotate(-90 {MARGIN_LEFT - 60},{MARGIN_TOP + (SVG_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM)/2})">Average Close - Open ($)</text>',
    ]

    # Add points
    for (x, y), (_, value) in zip(scaled_points, points):
        svg_lines.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#1f77b4"/>')

    # Add y-axis ticks and labels
    for value in value_ticks:
        y = value_to_y(value)
        svg_lines.append(f'<line x1="{MARGIN_LEFT - 5}" y1="{y:.2f}" x2="{MARGIN_LEFT}" y2="{y:.2f}" stroke="black"/>')
        svg_lines.append(f'<text x="{MARGIN_LEFT - 10}" y="{y + 5:.2f}" text-anchor="end">{value:.2f}</text>')

    # Add x-axis labels at quarterly intervals
    current = datetime(min_date.year, min_date.month, 1)
    while current <= max_date:
        x = date_to_x(current)
        svg_lines.append(f'<line x1="{x:.2f}" y1="{SVG_HEIGHT - MARGIN_BOTTOM}" x2="{x:.2f}" y2="{SVG_HEIGHT - MARGIN_BOTTOM + 5}" stroke="black"/>')
        svg_lines.append(
            f'<text x="{x:.2f}" y="{SVG_HEIGHT - MARGIN_BOTTOM + 25}" text-anchor="middle">{current:%b %Y}</text>'
        )
        if current.month >= 10:
            next_month = datetime(current.year + 1, ((current.month + 3 - 1) % 12) + 1, 1)
        else:
            next_month = datetime(current.year, current.month + 3, 1)
        current = next_month

    svg_lines.append("</svg>")
    return "\n".join(line for line in svg_lines if line)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    data_path = repo_root / "HistoricalData_1760090934890.csv"
    if not data_path.exists():
        raise FileNotFoundError(f"Could not find dataset at {data_path}")

    rows = list(read_price_rows(data_path))
    monthly_diff = compute_monthly_average_diff(rows)

    svg_content = build_svg(monthly_diff)

    output_dir = repo_root / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "average_open_close_difference.svg"
    output_file.write_text(svg_content, encoding="utf-8")

    print(f"Saved plot to {output_file}")


if __name__ == "__main__":
    main()
