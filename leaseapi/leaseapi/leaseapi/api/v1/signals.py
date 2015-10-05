from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

