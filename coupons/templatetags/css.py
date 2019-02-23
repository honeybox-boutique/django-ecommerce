from django import template

register = template.Library()


@register.filter(name='add_class_and_placeholder')
def add_class_and_placeholder(value, arg):
    arg_list = [arg.strip() for arg in arg.split(',')]
    return value.as_widget(attrs={'class': arg_list[0],
        'placeholder': arg_list[1],
    })
