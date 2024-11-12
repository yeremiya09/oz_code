from django.db import models

# Create your models here.

# model = DB의 테이블
# field = DB의 컬럼

# 북마크
# 이름 -> varchar
# URL 주소 -> varchar

class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일시',auto_now_add=True)
    updated_at = models.DateTimeField('수정일시',auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'

