from django.urls import path
from .views import save_code_to_db, execute_code_web, check_code_web, get_all_stored_codes, get_last_exec_result_web, index

urlpatterns = [
    path('save_code_to_db/', save_code_to_db, name='save_code_to_db', ),
    path('execute_code_web/', execute_code_web, name='execute_code_web', ),
    path('check_code_web/', check_code_web, name='check_code_web', ),
    path('get_all_stored_codes/', get_all_stored_codes, name='get_all_stored_codes', ),
    path('get_last_exec_result_web/', get_last_exec_result_web, name='get_last_exec_result_web', ),
    
    path('', index),
]