from django.http import HttpResponse
from supportdesk.models import Project, CallLog

import twilio.twiml
from django.utils import timezone

def begin_call(request):
    to_telephone = request.GET.get('To')

    resp = twilio.twiml.Response()

    support_agent = None
    try:
        project = Project.objects.get(support_telephone=to_telephone)
        resp.say(project.welcome_message)

        shifts = project.get_on_duty_shifts()

        if len(shifts) == 0:
            resp.say('Sorry, no support officers are available to take your call. Goodbye.')
        else:
            support_agent = shifts[0].user.supportagent
            resp.dial(support_agent.telephone)
            # If the dial fails:
            resp.say('The call failed, or the support officer hung up. Goodbye.')

    except Project.DoesNotExist:
        resp.say('Sorry, the help desk you are looking for does not exist. Goodbye.')

    call_log = CallLog()
    call_log.call_sid = request.GET.get('CallSid')
    call_log.to_telephone = request.GET.get('To')
    call_log.from_telephone = request.GET.get('From')
    call_log.start_datetime = timezone.now()
    call_log.support_agent = support_agent
    call_log.save()

    print request.GET.get('CallSid')

    return HttpResponse(str(resp))


def complete_call(request):
    print request.GET.get('CallSid')

    call_sid = request.GET.get('CallSid')
    call_log = CallLog.objects.get(call_sid=call_sid)
    call_log.end_datetime = timezone.now()
    call_log.save()

    return HttpResponse('Complete')
