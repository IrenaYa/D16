from .models import News
from modeltranslation.translator import register, TranslationOptions # импортируем декоратор для перевода и класс


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text') # указываем, какие именно поля надо переводить в виде кортежа