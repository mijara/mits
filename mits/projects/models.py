from django.db import models
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=64)

    description = models.TextField()

    members = models.ManyToManyField('auth.User')

    # used to assign the last created issue index number.
    issue_index = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

    def get_open_issues(self):
        return self.issue_set.filter(closed=False).all()

    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[self.pk])

    def get_report_url(self):
        return reverse('projects:project_report', args=[self.pk])

    def get_update_url(self):
        return reverse('projects:project_update', args=[self.pk])

    def get_delete_url(self):
        return reverse('projects:project_delete', args=[self.pk])

    def get_membership(self, user):
        """
        Returns the current logged in user membership.
        :return:
        """
        try:
            return user.membership_set.filter(project=self).get()
        except:
            return None

    def get_members_update_url(self):
        return reverse('projects:project_members_update', args=[self.pk])

    def get_issue_list_url(self):
        return reverse('issues:issue_list', args=[self.pk])

    def get_closed_issue_list_url(self):
        return reverse('issues:issue_list_closed', args=[self.pk])

    def get_issues_url(self):
        return reverse('issues:issue_list', args=[self.pk])

    def get_tags_url(self):
        return reverse('tags:tag_list', args=[self.pk])

    def get_checklists_url(self):
        return reverse('checklists:checklist_list', args=[self.pk])
