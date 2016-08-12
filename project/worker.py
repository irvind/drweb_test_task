import os
import time

from datetime import datetime
from multiprocessing import Process

import django
from django.db import transaction, DatabaseError
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


from tasks.models import Task, TaskResult

PROCESSES = []


def _default_proc():
    filepath = os.path.join(settings.BASE_DIR, 'test.py')
    with open(filepath, 'r') as f:
        content = f.read()

    exec(content)


class WorkerProcess(object):
    def __init__(self, task_id):
        self.task_id = task_id
        self.proc = None

    def run(self):
        PROCESSES.append(self)
        Task.objects.filter(id=self.task_id).update(status=Task.STATUS_RUNNING)
        self.proc = self.spawn_process()

    def finish(self):
        PROCESSES.remove(self)

        if self.proc and self.proc.is_alive():
            self.proc.terminate()

        with transaction.atomic():
            try:
                task_model = Task.objects.get(id=self.task_id)
            except Task.DoesNotExist:
                return

            task_model.status = Task.STATUS_FINISHED
            task_model.save(update_fields=['status'])

            TaskResult.objects.create(
                id=self.task_id,
                create_time=task_model.timestamp,
                finish_time=datetime.now()
            )

    @classmethod
    def spawn_process(cls, target=None):
        p = Process(target=target or _default_proc)
        p.start()
        return p


def main():
    while True:
        for process in PROCESSES[:]:
            if not process.proc.is_alive():
                process.finish()

        k = 2 - len(PROCESSES)

        with transaction.atomic():
            try:
                queryset = Task.objects.select_for_update(nowait=True)\
                    .filter(status=Task.STATUS_PENDING).order_by('timestamp')[:k]
            except DatabaseError:
                pass
            else:
                for task_model in queryset:
                    WorkerProcess(task_model.id).run()

        time.sleep(0.05)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print(PROCESSES)
        for process in PROCESSES[:]:
            process.finish()
