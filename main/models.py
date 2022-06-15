from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Organization(models.Model):
    name = models.CharField('Название', max_length=50)
    col = models.IntegerField('Кол-во сотрудников', default=0)

    def get_absolute_url(self):
        return reverse('organization', kwargs={'organization_id': self.id})


class Services(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    ip_address = models.CharField('Ip Адрес', max_length=50)
    login = models.CharField('Логин', max_length=50)
    password = models.CharField('Пароль', max_length=50)

    def get_absolute_url(self):
        return reverse('services', kwargs={'services_id': self.id})


class Get_Password(models.Model):
    id_services = models.ForeignKey(Services, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('Время получения', auto_now_add=True)

    def get_absolute_url(self):
        return reverse('get_password', kwargs={'get_password_id': self.id})

    """
    date_application = models.DateTimeField('Дата подачи заявки')
    time = models.TimeField('Время подачи', default=datetime.datetime.now())
    date_receipt = models.DateField('Дата приема')
    type_question = models.ForeignKey(Type_question, on_delete=models.CASCADE)
    id_employee = models.IntegerField('id пользователя')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    purpose_visit = models.CharField('Цель визита', max_length=50)
    status = models.CharField('Состояние заявки', default='New Applications', max_length=50)
    # Confirmed Applications and Rejected Applications
    text = models.TextField('Решение')
    FIO = models.CharField('ФИО', max_length=100)
    telephone = models.IntegerField('Телефон')
    email = models.CharField('Почта', max_length=50)

    def get_absolute_url(self):
        return reverse('application', kwargs={'application_slug': self.slug})
    """
