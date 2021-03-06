from django.shortcuts import get_object_or_404, redirect
from django.views import generic, View
import services

from forms import *
from projects import mixins
from comments.forms import CommentForm


class IssueListView(mixins.ProjectMixin, mixins.ProjectAccessCheckMixin, generic.ListView):
    model = Issue

    def get_queryset(self):
        return self.get_project().issue_set.filter(closed=False)

    def get_context_data(self, **kwargs):
        project = self.get_project()

        context = super(IssueListView, self).get_context_data(**kwargs)
        context['active'] = 'issues'
        context['project'] = project
        context['membership'] = project.get_membership(self.request.user)

        return context


class ClosedIssueListView(IssueListView):
    def get_queryset(self):
        return self.get_project().issue_set.filter(closed=True)


class IssueDetailView(mixins.ProjectMixin, mixins.ProjectAccessCheckMixin, generic.DetailView):
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['tags'] = services.pack_issue_tags(self.object)
        return context


class IssueCreateView(mixins.ProjectMixin, mixins.ProjectAccessCheckMixin, generic.CreateView):
    model = Issue
    form_class = IssueForm

    def post(self, request, *args, **kwargs):
        print request.POST
        return super(IssueCreateView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(IssueCreateView, self).get_form_kwargs()
        kwargs['project'] = self.get_project()
        kwargs['issue'] = None
        return kwargs

    def form_valid(self, form):
        project = self.get_project()

        form.instance.owner = self.request.user
        form.instance.project = project

        form.instance.index = project.issue_index

        project.issue_index += 1
        project.save()

        return super(IssueCreateView, self).form_valid(form)


class IssueUpdateView(mixins.ProjectMixin, mixins.ProjectAccessCheckMixin, generic.UpdateView):
    model = Issue
    form_class = IssueForm

    def get_form_kwargs(self):
        kwargs = super(IssueUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.get_project()
        kwargs['issue'] = self.object
        return kwargs


class IssueTagsUpdateView(mixins.ProjectAccessCheckMixin, generic.UpdateView):
    model = Issue
    form_class = IssueTagsForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class IssueCloseView(mixins.ProjectAccessCheckMixin, generic.DetailView):
    model = Issue

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if not issue.closed:
            State(issue=issue, closed=True, owner=self.request.user).save()

            if issue.pinned:
                # TODO: check if this could provoke issues later.
                issue.pinned = False
                issue.save()
        return redirect(issue.get_absolute_url())


class IssueOpenView(mixins.ProjectAccessCheckMixin, generic.DetailView):
    model = Issue

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.closed:
            State(issue=issue, closed=False, owner=self.request.user).save()
        return redirect(issue.get_absolute_url())


class IssuePinToggleView(mixins.ProjectAccessCheckMixin, generic.DetailView):
    model = Issue

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if not issue.pinned:
            issue.set_pin(True, self.request.user)
        else:
            issue.set_pin(False, self.request.user)
        return redirect(issue.get_absolute_url())
