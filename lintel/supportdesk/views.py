from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from supportdesk.models import Project, SupportAgent, CallLog
from supportdesk.forms import ProjectModelForm, SupportAgentForm, ShiftModelForm

def dashboard(request):
    all_projects = Project.objects.all()

    return render_to_response(
        'supportdesk/dashboard.html',
        context_instance=RequestContext(
            request,
            {'projects': all_projects}
            )
        )

def projects(request):
    all_projects = Project.objects.all()

    return render_to_response(
        'supportdesk/projects.html',
        context_instance=RequestContext(
            request,
            {'projects': all_projects}
            )
        )

def projects_new(request):
    if request.method == 'POST':
        project_form = ProjectModelForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.save()

            return HttpResponseRedirect(
                reverse('projects')
                )

    else:
        project_form = ProjectModelForm()

    return render_to_response(
        'supportdesk/projects_new.html',
        context_instance=RequestContext(
            request,
            {'project_form': project_form}
            )
        )

def projects_manage(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        shift_form = ShiftModelForm(request.POST)
        if shift_form.is_valid():
            shift = shift_form.save(commit=False)
            shift.project = project
            shift.save()

            return HttpResponseRedirect(
                reverse('projects_manage', args=[project.id])
                )

    else:
        shift_form = ShiftModelForm()

    return render_to_response(
        'supportdesk/projects_manage.html',
        context_instance=RequestContext(
            request,
            {'project': project, 'shift_form': shift_form}
            )
        )





def support_agents(request):
    all_support_agents = SupportAgent.objects.all()

    return render_to_response(
        'supportdesk/support_agents.html',
        context_instance=RequestContext(
            request,
            {'support_agents': all_support_agents}
            )
        )

def support_agents_new(request):
    print request.method
    if request.method == 'POST':
        support_agent_form = SupportAgentForm(request.POST)
        if support_agent_form.is_valid():
            first_name = support_agent_form.cleaned_data['first_name']
            last_name = support_agent_form.cleaned_data['last_name']
            email = support_agent_form.cleaned_data['email']
            telephone = support_agent_form.cleaned_data['telephone']

            new_user = User()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.username = email
            new_user.set_password('password')

            new_user.save()

            new_support_agent = SupportAgent()
            new_support_agent.user = new_user
            new_support_agent.telephone = telephone
            new_support_agent.save()

            new_user.supportagent = new_support_agent
            new_user.save()

            return HttpResponseRedirect(
                reverse('support_agents')
                )

    else:
        support_agent_form = SupportAgentForm()

    return render_to_response(
        'supportdesk/support_agents_new.html',
        context_instance=RequestContext(
            request,
            {'support_agent_form': support_agent_form}
            )
        )

def support_agents_manage(request, support_agent_id):
    support_agent = get_object_or_404(SupportAgent, id=support_agent_id)

    return render_to_response(
        'supportdesk/support_agents_manage.html',
        context_instance=RequestContext(
            request,
            {'support_agent': support_agent}
            )
        )




def calls(request):
    calls = CallLog.objects.all().order_by('-start_datetime', '-end_datetime')

    return render_to_response(
        'supportdesk/calls.html',
        context_instance=RequestContext(
            request,
            {'calls': calls}
            )
        )
