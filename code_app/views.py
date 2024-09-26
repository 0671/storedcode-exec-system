from django.shortcuts import render
import sys
import importlib.util
from django.http import JsonResponse
from .models import StoreCode
from celery import shared_task
from celery.result import AsyncResult

def get_exec_result(task_id):
    try:
        result = AsyncResult(task_id)
        if result.ready():
            return {
                'status':'success',
                'result': result.result
            }
        else:
            return {
                'status': 'running',
                'result': 'Task is still running.',
            }
    except Exception as e:
        return {
            'status': 'error',
            'result': f'Task is unknown error. Error: {e}',
        }

@shared_task
def execute_code(store_code):
        try:
            spec = importlib.util.spec_from_loader('temp_module',None)
            temp_module = importlib.util.module_from_spec(spec)
            sys.modules['temp_module']=temp_module
            exec(store_code, temp_module.__dict__)
            code_exec_result = temp_module.result
            return {
                'status': 'success', 
                'result': code_exec_result
            }
        except StoreCode.DoesNotExist:
            return {
                'status': 'error', 
                'result': 'Code not found.'
            }
        except Exception as e:
            return {
                'status': 'error', 
                'result': f'Error executing code: {e}'
            }

# Create your views here.
def save_code_to_db(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            stored_code = StoreCode(code=code)
            stored_code.save()
            return JsonResponse({'status': 'success', 'result': f'Code saved successfully. Code id is {stored_code.id}'})
        else:
            return JsonResponse({'status': 'error', 'result': 'No code provided.'})
    else:
        return JsonResponse({'status': 'error', 'result': 'Invalid request method.'})


def check_code_web(request):
    if request.method == 'POST':
        code_id = request.POST.get('id')
        if code_id:
            try:
                store_code = StoreCode.objects.get(id=code_id)
                return JsonResponse({
                    'status': 'success', 
                    'result': {'ID':code_id,'Code': store_code.code}
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error', 
                    'result': f'Error executing code: {e}'
                })
        else:
            return JsonResponse({
                'status': 'error', 
                'result': f'No code ID provided.'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'result': 'Invalid request method.'
        })

def execute_code_web(request):
    if request.method =='POST':
        code_id = request.POST.get('id')
        if code_id:
            try:
                store_code = StoreCode.objects.get(id=code_id)
                result = execute_code.delay(store_code.code)
                store_code.last_task_id = result.task_id
                store_code.save()
                return JsonResponse({
                    'status': 'success', 
                    'result': {'task_id':result.task_id}
                })
            except StoreCode.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'result': 'Code not found.'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error', 
                    'result': f'Error executing code: {e}'
                })
        else:
            return JsonResponse({
                'status': 'error', 
                'result': f'No code ID provided.'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'result': 'Invalid request method.'
        })

def get_last_exec_result_web(request):
    if request.method =='POST':
        code_id = request.POST.get('id')
        if code_id:
            try:
                store_code = StoreCode.objects.get(id=code_id)
                if store_code.last_task_id == '':
                    return JsonResponse({
                        'status': 'error', 
                        'result': 'Code not exec.'
                    })
                else:
                    result =  get_exec_result(store_code.last_task_id)
                    if result['status'] == 'success':
                        return JsonResponse({
                            'status': 'success', 
                            'task_id': store_code.last_task_id,
                            'result': result['result'],
                        })
                    elif result['status'] == 'running':
                        return JsonResponse({
                            'status': 'running', 
                            'task_id': store_code.last_task_id,
                            'result': result['result'],
                        })
                    else:
                        return JsonResponse({
                            'status': 'error', 
                            'task_id': store_code.last_task_id,
                            'result': result['result'],
                        })
            except StoreCode.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'result': 'Code not found.'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error', 
                    'result': f'Error executing code: {e}'
                })
        else:
            return JsonResponse({
                'status': 'error', 
                'result': f'No code ID provided.'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'result': 'Invalid request method.'
        })

def index(request):
    return render(request, 'index.html')

def get_all_stored_codes(request):
    store_codes = StoreCode.objects.all()
    return JsonResponse([{'id': sc.id, 'code': sc.code} for sc in store_codes], safe=False)