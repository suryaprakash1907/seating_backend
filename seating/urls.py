from django.urls import path
from .views import (
    UploadStudentsView,
    UploadTimetableView,
    GenerateSeatingView,
    RoomsForDateView,
    ViewSeatingView,
    ViewSeatingGroupedView,
    DownloadSeatingExcelView,
)

urlpatterns = [
    path("upload/students/", UploadStudentsView.as_view()),
    path("upload/timetable/", UploadTimetableView.as_view()),
    path("generate/", GenerateSeatingView.as_view()),
    path("rooms/<date>/", RoomsForDateView.as_view()),
    path("view/<date>/", ViewSeatingView.as_view()),
    path("view_grouped/<date>/", ViewSeatingGroupedView.as_view()),
    path("download/<date>/", DownloadSeatingExcelView.as_view()),
]
