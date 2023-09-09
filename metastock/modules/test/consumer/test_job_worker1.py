from metastock import Logger
from metastock.modules.rabbitmq.job_worker import JobWorker


class TestJobWorker1(JobWorker):
    def job_id(self):
        return 'test_job_worker_1'

    def handle(self, ch, method, properties, body):
        Logger().info('Process TestJobWorker1')
