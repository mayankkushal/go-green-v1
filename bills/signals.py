from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from .models import Bill 


@receiver(post_save, sender=Bill)
def set_bill_no(sender, instance, created, **kwargs):
	"""
	Adds the bill no after the bill instance is created and generates nofication
	"""
	bill_no = ""
	cus = User.objects.get(profile__phone_no=instance.customer_no)
	if created:
		if instance.original:
			instance.bill_no = '100000'+str(instance.id)
			
			instance.save()
		notify.send(instance.store, 
				recipient=cus, 
				verb='Payment successful, you have a new bill, numbered #'+instance.bill_no,
				url=instance.get_absolute_url(), 
				pk=instance.pk
				)


post_save.connect(set_bill_no, sender=Bill)