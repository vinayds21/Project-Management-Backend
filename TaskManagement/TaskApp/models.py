from __future__ import unicode_literals

from django.db import models

# Create your models here.

class BaseModel(models.Model):
	created_on = models.DateTimeField(auto_now_add = True, db_index=True, \
									verbose_name='created_on', null=True, blank=True)
	updated_on = models.DateTimeField(auto_now = True, db_index=True, \
									verbose_name='updated_on', null=True, blank=True)
	is_deleted = models.BooleanField(default=False, verbose_name='deleted')

	class Meta:
		abstract = True

class Project(BaseModel):
	''''''
	STATUS_DICT ={
		0 : 'Open',
		1 : 'In Progress',
		2 : 'Completed',
		3 : 'Deleted'
	}
	project_name = models.CharField(max_length=255)
	description = models.TextField()
	status = models.SmallIntegerField(default=0)

	class Meta:
		db_table = 'project'
		verbose_name = 'project'
		verbose_name_plural = 'projects'

	def __unicode__(self):
		return  'Project Name: {0}'.format(str(self.project_name))

	# def _seraliser(self):
	# 	data = {}
	# 	data['project_name'] = self.project_name
	# 	return data

class Task(BaseModel):
	''''''
	STATUS_DICT ={
		0 : 'Open',
		1 : 'Assigned',
		2 : 'In progress',
		3 : 'In QA',
		4 : 'Testing Done',
		5 : 'In Production',
		6 : 'Deleted'
	}

	TYPE_DICT ={
		0 : 'Requirement',
		1 : 'Bug'
	}

	task_name = models.CharField(max_length=255)
	description = models.TextField()
	status = models.SmallIntegerField(default=0)
	task_type = models.SmallIntegerField(default=0)
	project = models.ForeignKey(Project)

	class Meta:
		db_table = 'task'
		verbose_name = 'task'
		verbose_name_plural = 'tasks'

	def __unicode__(self):
		return  'Task Name: {0}'.format(str(self.task_name))