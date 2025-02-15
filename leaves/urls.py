from django.urls import path
from .views import add_leave_quota, edit_leave, signup, dashboard, apply_leave, manage_leaves, approve_leave, reject_leave, user_logout

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('apply/', apply_leave, name='apply_leave'),
    path('manage-leaves/', manage_leaves, name='manage_leaves'),
    path('approve-leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('reject-leave/<int:leave_id>/', reject_leave, name='reject_leave'),
    path('leave-quota/', add_leave_quota, name='leave_quota'),
    path('edit-leave/<int:leave_id>/', edit_leave, name='edit_leave'),
]
