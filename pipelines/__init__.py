from celery import Celery
from dagster_celery.tasks import create_task


celery = Celery('dagster')
execute_plan = create_task(celery)

if __name__ == '__main__':
    celery.worker_main()
