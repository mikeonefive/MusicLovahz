from django import template

register = template.Library()                   # telling Django "Hey, I want to add some custom tools (filters) for templates"

@register.filter
def get_item(dictionary, key):                  # to get to the songs of a matched user (user = key, songs = values)
    # Get this item from dictionary by key
    return dictionary.get(key)