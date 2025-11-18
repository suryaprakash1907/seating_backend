from django.contrib import admin
from .models import UploadedFile, Student, TimetableRow, Room, Seating

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file','description','uploaded_at')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll','year','uploaded_file')

@admin.register(TimetableRow)
class TimetableRowAdmin(admin.ModelAdmin):
    list_display = ('date','i_year_subject','ii_year_subject','iii_year_subject')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('code','capacity')

@admin.register(Seating)
class SeatingAdmin(admin.ModelAdmin):
    list_display = ('roll','year','room','exam_date','row_index','col_index')
    list_filter = ('exam_date','room')
