from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Task, TaskResult


class NoCsrfMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class IndexView(TemplateView):
    template_name = 'tasks/index.html'


class TasksViewCreateView(NoCsrfMixin, View):
    def get(self, request):
        tasks = list(Task.objects.order_by('-timestamp'))
        result_mapping = {res.id: res for res in TaskResult.objects.all()}

        def format_time(time):
            return time.strftime('%H:%M %d.%m.%Y')

        resp = []
        for task in tasks:
            item = {
                'id': task.id,
                'create_time': format_time(task.timestamp),
                'status': task.get_status_display(),
            }

            if task.status == Task.STATUS_FINISHED:
                result_model = result_mapping.get(task.id)
                if result_model:
                    item['finish_time'] = format_time(result_model.finish_time)

            resp.append(item)

        return JsonResponse(resp, safe=False)

    def post(self, request):
        Task.objects.create(status=Task.STATUS_PENDING)
        return JsonResponse({'success': True})


class ResetTasksView(NoCsrfMixin, View):
    def post(self, request):
        TaskResult.objects.all().delete()
        Task.objects.all().delete()
        return JsonResponse({'success': True})
