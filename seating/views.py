from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import render
from django.db.models import Max
import pandas as pd
import datetime

from .models import UploadedFile, Student, TimetableRow, Seating, Room
from .services.seating_generator import parse_rolls_from_dataframe, generate_seating_for_date


# ---------------------- UPLOAD STUDENTS ----------------------
class UploadStudentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        f = request.FILES.get('file')
        year = int(request.data.get('year')) if request.data.get('year') else None

        if not f:
            return Response({"detail": "No file"}, status=400)

        uf = UploadedFile.objects.create(file=f)

        df = pd.read_excel(f)
        rolls = parse_rolls_from_dataframe(df)

        if year is None:
            name = f.name.lower()
            if 'iii' in name or '3' in name:
                year = 3
            elif 'ii' in name or '2' in name:
                year = 2
            else:
                year = 1

        for r in rolls:
            Student.objects.get_or_create(roll=str(r), year=year, defaults={'uploaded_file': uf})

        return Response({"created": len(rolls)})


# ---------------------- UPLOAD TIMETABLE ----------------------
class UploadTimetableView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        f = request.FILES.get('file')
        if not f:
            return Response({"detail": "No file"}, status=400)

        df = pd.read_excel(f)
        df["DATE"] = pd.to_datetime(df["DATE"]).dt.date

        for _, row in df.iterrows():
            TimetableRow.objects.update_or_create(
                date=row["DATE"],
                defaults={
                    "i_year_subject": row.get("I YEAR SUBJECT", ""),
                    "ii_year_subject": row.get("II YEAR SUBJECT", ""),
                    "iii_year_subject": row.get("III YEAR SUBJECT", "")
                }
            )

        return Response({"rows": len(df)})


# ---------------------- GENERATE SEATING ----------------------
class GenerateSeatingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        date = request.data.get('date')
        capacity = int(request.data.get('capacity', 90))
        rooms = int(request.data.get('rooms', 0))
        start = request.data.get('start', 'MC101')

        exam_date = datetime.date.fromisoformat(date)
        created = generate_seating_for_date(exam_date, capacity, rooms or 999, start)

        return Response({"created_entries": len(created)})


# ---------------------- ROOMS FOR DATE ----------------------
class RoomsForDateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date, format=None):
        rooms = (
            Seating.objects.filter(exam_date=date)
            .values_list("room__code", flat=True)
            .distinct()
        )
        return Response(list(rooms))


# ---------------------- VIEW SEATING (FLAT LIST) ----------------------
class ViewSeatingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date, format=None):
        qs = Seating.objects.filter(exam_date=date).order_by(
            "room__code", "row_index", "col_index"
        )

        data = [
            {
                "room": seat.room.code,
                "row": seat.row_index,
                "col": seat.col_index,
                "roll": seat.roll,
            }
            for seat in qs
        ]

        return Response(data)


# ---------------------- VIEW SEATING GROUPED (TABLE FORMAT) ----------------------
class ViewSeatingGroupedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date, format=None):
        qs = Seating.objects.filter(exam_date=date).order_by(
            "room__code", "row_index", "col_index"
        )

        grouped = {}

        for seat in qs:
            room_code = seat.room.code

            if room_code not in grouped:
                grouped[room_code] = []

            while len(grouped[room_code]) <= seat.row_index:
                grouped[room_code].append(["" for _ in range(9)])  # 9 columns fixed

            grouped[room_code][seat.row_index][seat.col_index] = seat.roll

        return Response(grouped)


# ---------------------- DOWNLOAD EXCEL ----------------------
class DownloadSeatingExcelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date, format=None):
        return Response({"detail": "Not implemented"})
