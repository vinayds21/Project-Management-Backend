from __future__ import unicode_literals

from django.db import models
from django.core.validators import URLValidator
from TaskApp.models import BaseModel

# Create your models here.

class Organization(BaseModel):
	''''''
	name = models.CharField(max_length=255)
	company_type = models.CharField(max_length=255)
	company_website = models.TextField(validators=[URLValidator()])
	address_line_1 = models.CharField(max_length=255)
	address_line_2 = models.CharField(max_length=255, blank=True)
	state = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	pin = models.CharField(max_length=10)

	class Meta:
		db_table = 'organization'
		verbose_name = 'organization'
		verbose_name_plural = 'organizations'

	def __unicode__(self):
		return  'Organization: {0}'.format(str(self.name))

class User(BaseModel):
	''''''
	USER_TYPE={
		0 : 'Employee',
		1 : 'Manager'
	}

	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	user_mobile = models.CharField(max_length=10)
	user_mail = models.CharField(max_length=255)
	user_designation = models.CharField(max_length=255)
	user_type = models.SmallIntegerField(default=0)
	user_password = models.CharField(max_length=255)
	token = models.CharField(max_length=255)
	organization = models.ForeignKey(Organization)

	class Meta:
		db_table = 'user'
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def __unicode__(self):
		return  'User: {0} {1}'.format(str(self.first_name), str(self.last_name))