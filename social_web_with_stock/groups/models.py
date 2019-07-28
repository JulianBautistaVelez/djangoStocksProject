from django import template
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import misaka
# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

register = template.Library()

FINANCIAL_CHOICES = [
    ('Company Chart', (
        ('CHTMMM', '3M'),
        ('CHTAAPL', 'Apple'),
        ('CHTAXP', 'American Express'),
        ('CHTBA', 'Boeing'),
        ('CHTCAT', 'Caterpillar'),
        ('CHTCSCO', 'Cisco'),
        ('CHTKO', 'Coca-Cola'),
        ('CHTGS', 'Goldman Sachs'),
        ('CHTIBM', 'IBM'),
        ('CHTINTC', 'Intel'),
        ('CHTNKE', 'Nike'),
        ('CHTPFE', 'Pfizer'),
        ('CHTVZ', 'Verizon'),
        ('CHTV', 'Visa'),
        ('CHTWTM', 'Wallmart'),
    )
    ),
    ('Information', (
        ('INFMMM', '3M'),
        ('INFAAPL', 'Apple'),
        ('INFAXP', 'American Express'),
        ('INFBA', 'Boeing'),
        ('INFCAT', 'Caterpillar'),
        ('INFCSCO', 'Cisco'),
        ('INFKO', 'Coca-Cola'),
        ('INFGS', 'Goldman Sachs'),
        ('INFIBM', 'IBM'),
        ('INFINTC', 'Intel'),
        ('INFNKE', 'Nike'),
        ('INFPFE', 'Pfizer'),
        ('INFVZ', 'Verizon'),
        ('INFV', 'Visa'),
        ('INFWTM', 'Wallmart'),
    )
    ),
    ('DJC', 'Dow Jones Companies Today'),
    ('BVC', 'Bitcoin Value Chart'),
]


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMember')
    grouptype = models.CharField(
        max_length=8, choices=FINANCIAL_CHOICES, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    @property
    def get_is_chart(self):
        if self.grouptype[:3] == 'CHT':
            return True
        else:
            return False

    @property
    def get_is_info(self):
        if self.grouptype[:3] == 'INF':
            return True
        else:
            return False

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(
        Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
