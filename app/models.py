"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import json
from demo import names

all_names = [(v, v) for k, v in names.items()]


class Object(models.Model):
    name = models.CharField("名字", max_length=32, unique=True, choices=all_names)
    classes = models.CharField("种类", max_length=128, blank=True, null=True)
    latin_name = models.CharField("拉丁名称", max_length=128, blank=True, null=True)
    head = models.CharField("目", max_length=128, blank=True, null=True)
    family = models.CharField("科", max_length=128, blank=True, null=True)
    gender = models.CharField("属", max_length=128, blank=True, null=True)
    feeding_habits = models.TextField("食性", blank=True)
    detail = models.TextField("分布区域", blank=True)

    class Meta:
        verbose_name = "昆虫详情"
        verbose_name_plural = "昆虫详情"

    def to_dict(self):
        return {
            'name': self.name,
            'classes': self.classes,
            'latin_name': self.latin_name,
            'head': self.head,
            'family': self.family,
            'gender': self.gender,
            'feeding_habits': self.feeding_habits,
            'detail': self.detail
        }

    def __str__(self):
        return self.name


class OcrLog(models.Model):
    """This model is used to store the ocr log"""
    username = models.CharField(max_length=32)
    result = models.TextField()
    origin = models.CharField(max_length=255)
    target = models.CharField(max_length=32)
    add_time = models.DateTimeField(auto_now_add=True)
    ocr_time = models.FloatField()

    class Meta:
        verbose_name = "识别历史"

    def to_dict(self):
        return {
            'username': self.username,
            'add_time': self.add_time,
            'result': json.loads(self.result),
            'target': self.target,
            "origin": self.origin,
            'ocr_time': self.ocr_time
        }
