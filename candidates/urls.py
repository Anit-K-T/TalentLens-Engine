from django.urls import path
from . import views

urlpatterns = [
    path("", views.candidate_list, name="candidate_list"),
    path("add/", views.add_candidate, name="add_candidate"),
    path("edit/<int:candidate_id>/", views.edit_candidate, name="edit_candidate"),
    path("<int:pk>/", views.candidate_detail, name="candidate_detail"),
    path("delete/<int:candidate_id>/", views.delete_candidate, name="delete_candidate"),
    path(
    "candidate/<int:pk>/evaluate/",
    views.evaluate_candidate,
    name="evaluate_candidate",
    ),
    path(
    "report/<int:candidate_id>/",
    views.download_ai_report,
    name="download_ai_report"),
    path(
    "export/csv/",
    views.export_candidates_csv,
    name="export_candidates_csv"
    ),

    path(
    "export/excel/",
    views.export_candidates_excel,
    name="export_candidates_excel"
    ),
]