from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from api.v1.models import BackupRequest
from api.v1.services import BackupService
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=BackupRequest, weak=False)
def preSaveHandler(sender, instance, *args, **kwargs):    
    logger.info("Start PRE SAVE Signal")
    service = BackupService()
    if instance.pk is None:
        service.create(backup=instance)
    elif instance.status == "D":
        service.delete(backup=instance)
    else:
        service.update(backup=instance)
    
    logger.info("End PRE SAVE Signal")


@receiver(post_save, sender=BackupRequest)
def postSaveHandler(sender, instance, *args, **kwargs):
    logger.info("Start POST SAVE Signal")
    #service = BackupService()	
    #service.log(backup=instance)
    #service.sendMail(backup=instance)
    logger.info("End POST SAVE Signal")

