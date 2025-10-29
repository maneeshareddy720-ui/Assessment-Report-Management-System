from django.urls import path
from . import views

urlpatterns = [
    # -------------------------
    # Public Intern Application URLs
    # -------------------------
    path("", views.intern_form, name="form"),
    path("apply-form/", views.intern_form, name="intern_form"),
    path("success/<int:intern_id>/", views.success_view, name="success"),

    # -------------------------
    # Authentication & Profile URLs
    # -------------------------
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("profile/", views.profile_view, name="profile"),

    # -------------------------
    # Main Dashboards
    # -------------------------
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("main_dashboard/", views.dashboard_home, name="dashboard_home"),

    # -------------------------
    # Superuser-only Staff/User Management
    # -------------------------
    path("super-admin/", views.super_admin_view, name="super_admin"),
    path("admin-user/", views.admin_user_view, name="admin_user"),
    path("add-staff/", views.add_staff_user, name="add_staff_user"),
    path("staff/<int:user_id>/edit/", views.edit_staff_user, name="edit_staff_user"),

    # -------------------------
    # Intern Management (CRUD)
    # -------------------------
    path("edit/<int:intern_id>/", views.admin_edit_intern, name="admin_edit_intern"),
    path("delete/<int:intern_id>/", views.admin_delete_intern, name="admin_delete_intern"),

    # -------------------------
    # Assessment Management
    # -------------------------
    path("assessment/create/", views.create_assessment, name="intern_reports"),
    path("assessment/delete/trainee/<int:trainee_id>/", views.delete_assessment, name="delete_assessment"),
    path("trainee/<int:trainee_id>/assessments/", views.trainee_assessments, name="trainee_assessments"),

    # -------------------------
    # Assessment Edit Steps (using UUIDs)
    # -------------------------
    path("assessment/<uuid:assessment_id>/edit/step1/", views.edit_assessment_step1, name="edit_assessment_step1"),
    path("assessment/<uuid:assessment_id>/edit/step2/", views.edit_assessment_step2, name="edit_assessment_step2"),

    # -------------------------
    # AJAX/API Endpoints
    # -------------------------
   
    path("trainee/<int:trainee_id>/domain/<str:domain>/assessments/json/", views.trainee_domain_assessments_json, name="trainee_domain_assessments_json"),

    path("dashboard/export_excel/", views.export_dashboard_excel, name="export_dashboard_excel"),

   path("trainee/<int:trainee_id>/export_excel/",
        views.export_trainee_excel,
        name="export_trainee_excel"),

]
