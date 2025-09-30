#myapp/apps.py
from django.apps import AppConfig # импорт базового  класса

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # поле первичного ключа в моделях
    name = 'myapp'