from django import template

from ..models import TaskList

register = template.Library()

@register.simple_tag
def get_task_lists(limit):
    return TaskList.objects.all().order_by('list_name')[:limit]