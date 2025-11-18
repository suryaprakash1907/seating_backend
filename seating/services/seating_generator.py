import io
from collections import deque
from math import ceil
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Border, Side, Font

from ..models import Student, Room, Seating

# helper utilities (ported)
def parse_rolls_from_dataframe(df):
    # find roll-like column
    for col in df.columns:
        if any(k in str(col).lower() for k in ["roll","rno","reg","register","admission","hall"]):
            vals = df[col].astype(str).str.strip()
            return [v for v in vals if v and v.lower() != "nan"]
    # otherwise use first column
    vals = df[df.columns[0]].astype(str).str.strip()
    return [v for v in vals if v and v.lower() != "nan"]

def has_exam(cell_value):
    if pd.isna(cell_value): return False
    if str(cell_value).strip() in ["", "-", "—"]: return False
    return True


def generate_seating_for_date(exam_date, capacity, num_rooms, start_room_code="MC101"):
    """
    Generates seating in DB for given exam_date.
    Returns: list of created Seating objects (or count).
    """
    if capacity % 9 != 0 or capacity == 0:
        raise ValueError("Room capacity must be a non-zero multiple of 9")

    ROWS_PER_ROOM = capacity // 9
    TOTAL_COLUMNS = 9

    # collect students by year
    years_data = {1:[],2:[],3:[]}
    for s in Student.objects.all():
        years_data[s.year].append(s.roll)

    # figure which years have exam on date
    from ..models import TimetableRow
    try:
        row = TimetableRow.objects.get(date=exam_date)
    except TimetableRow.DoesNotExist:
        raise ValueError("No timetable entry for this date")

    exam_years = []
    if has_exam(row.i_year_subject): exam_years.append(1)
    if has_exam(row.ii_year_subject): exam_years.append(2)
    if has_exam(row.iii_year_subject): exam_years.append(3)
    if not exam_years:
        raise ValueError("No exams for any year on that date")

    selected_students = []
    for y in exam_years:
        selected_students.extend(years_data[y])

    total_students = len(selected_students)
    recommended_rooms = ceil(total_students / capacity)
    if num_rooms < recommended_rooms:
        raise ValueError(f"Need at least {recommended_rooms} rooms based on students and capacity")

    queues = {y: deque(years_data[y]) for y in exam_years}

    def build_pattern():
        counts = {y: len(years_data[y]) for y in exam_years}
        sorted_years = sorted(exam_years, key=lambda y: counts[y], reverse=True)
        pattern = []
        while len(pattern) < TOTAL_COLUMNS:
            pattern.extend(sorted_years)
        return pattern[:TOTAL_COLUMNS]

    pattern = build_pattern()

    def chunk_rooms():
        while any(queues[y] for y in exam_years):
            room_pairs = []
            counts = {1:0,2:0,3:0}
            for yr in pattern:
                for _ in range(ROWS_PER_ROOM):
                    if queues[yr]:
                        roll = queues[yr].popleft()
                        room_pairs.append((yr, roll))
                        counts[yr] += 1
                    else:
                        room_pairs.append((yr, ""))
            yield room_pairs, counts

    # create or get Room objects
    room_code = start_room_code
    created_seatings = []
    gen = chunk_rooms()
    for _ in range(num_rooms):
        try:
            rp, cnt = next(gen)
        except StopIteration:
            break
        # create Room if not exists
        room_obj, _ = Room.objects.get_or_create(code=room_code, defaults={"capacity": capacity})
        # save seatings
        for idx, (yr, roll) in enumerate(rp[:TOTAL_COLUMNS * ROWS_PER_ROOM]):
            col = idx // ROWS_PER_ROOM
            row_idx = idx % ROWS_PER_ROOM
            seating = Seating.objects.create(
                room=room_obj,
                exam_date=exam_date,
                year=yr,
                roll=roll or "",
                row_index=row_idx,
                col_index=col
            )
            created_seatings.append(seating)
        # increment room code like MC101 -> MC102 (attempt numeric part)
        # naive parse:
        import re
        m = re.search(r'(\D*)(\d+)$', room_code)
        if m:
            prefix, num = m.group(1), int(m.group(2))
            room_code = f"{prefix}{num+1}"
        else:
            # fallback append index
            room_code = f"{room_code}a"

    return created_seatings
