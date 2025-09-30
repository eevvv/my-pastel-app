
# myapp/middleware.py
# myapp/middleware.py
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        available_languages = [lang[0] for lang in settings.LANGUAGES]

        # 1. Если в URL есть параметр lang - это самый высокий приоритет
        if 'lang' in request.GET:
            lang_code = request.GET['lang']
            if lang_code in available_languages:
                request.session['django_language'] = lang_code
                translation.activate(lang_code)
                request.LANGUAGE_CODE = lang_code

                # Убираем lang из URL через редирект
                path = request.path
                query_string = request.META.get('QUERY_STRING', '')
                if query_string:
                    new_params = [p for p in query_string.split('&')
                                  if p and not p.startswith('lang=')]
                    if new_params:
                        path += '?' + '&'.join(new_params)

                return HttpResponseRedirect(path)

        # 2. Используем язык из сессии, если он есть
        lang_code = request.session.get('django_language')

        # 3. Если в сессии нет языка, используем английский по умолчанию
        if not lang_code or lang_code not in available_languages:
            lang_code = 'en'  # Явно указываем английский

        # Активируем язык
        translation.activate(lang_code)
        request.LANGUAGE_CODE = lang_code

        # Сохраняем в сессии
        request.session['django_language'] = lang_code

    def process_response(self, request, response):
        lang_code = getattr(request, 'LANGUAGE_CODE', None)
        if lang_code:
            response['Content-Language'] = lang_code
        return response