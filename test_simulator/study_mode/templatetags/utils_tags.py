from django import template
from django.utils.safestring import mark_safe
from tests.models import Question


register = template.Library()

@register.inclusion_tag('input_question_template.html')
def render_user_question_data(user, question):
    result = question.get_user_question_data(user.username)
    if(result.count() > 0):
        print(result[0].annotation)
        return {'user': user, 'question': question, 'annotation': result[0].annotation, 'tag': result[0].tag }
    else:
        return {'user': user, 'question': question, 'annotation': ""}

@register.inclusion_tag('render_user_question_icons.html')
def render_user_question_icons(user, question):
    result = question.get_user_question_data(user.username)
    if(result.count() > 0):
        return {'user': user, 'question': question, 'tag': result[0].tag }
    else:
        return {'user': user, 'question': question, 'tag': "NONE"}
    
@register.simple_tag
def render_img_tags(text):

    index = text.find('{img')
    if index == -1:
        return text

    while True:  
        index = text.find('{img')
        if index == -1:
            return mark_safe(text)
        
        getted_img = ""
        final = -1
        count = index
        while True:
            getted_img += text[count]
            if text[count] == '}':
                final = count
                break
            count += 1
        
        getted_href = text[index+4:final]
        text = text.replace(getted_img, '<img src="' + getted_href + '" style="max-width:100%;"><br>')
