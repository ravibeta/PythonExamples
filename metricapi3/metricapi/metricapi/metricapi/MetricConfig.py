'''
from django.apps import AppConfig


class MetricConfig(AppConfig):
    name = 'metric'

    def ready(self):
        Metric = self.get_model('Metric')
        #watson.register(Metric.objects.exclude(id=None))
'''
