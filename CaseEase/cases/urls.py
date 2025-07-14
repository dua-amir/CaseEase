from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterCaseView.as_view(), name='register_case'),

    path('assign/<int:case_id>/', views.AssignHandlerView.as_view(), name='assign_handler'),

    path('case/<int:pk>/', views.CaseDetailView.as_view(), name='case_detail'),


    # path('my-cases/', views.MyCasesView.as_view(), name='my_cases'),
    # path('all/', views.AllCasesView.as_view(), name='all_cases'),
    # path('approve/<int:case_id>/', views.approve_case, name='approve_case'),
    # path('assign/<int:case_id>/', views.AssignHandlerView.as_view(), name='assign_handler'),
    # path('handler/dashboard/', views.HandlerDashboardView.as_view(), name='handler_dashboard_cases'),

]
