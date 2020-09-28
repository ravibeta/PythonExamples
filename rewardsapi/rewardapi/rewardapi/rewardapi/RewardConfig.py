'''
from django.apps import AppConfig


class RewardConfig(AppConfig):
    name = 'reward'

    def ready(self):
        Reward = self.get_model('Reward')
        #watson.register(Reward.objects.exclude(id=None))
'''
