from django import template
from PhysioSlim.models import Notifications

register = template.Library()

@register.inclusion_tag('physio-slim/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notifications.objects.filter(to_user=request_user).exclude(user_seen=True).order_by('-created_on')
    return {'notifications':notifications}