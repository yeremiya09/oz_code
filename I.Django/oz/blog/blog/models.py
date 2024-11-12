from django.contrib.auth.middleware import get_user
from django.contrib.auth import get_user_model

from django.db import models


User = get_user_model()

# Create your models here.
class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지')

    )

    category = models.CharField('카테고리',max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField('제목',max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #  models.CASCADE -> 같이 삭제
    #  models.PROTECT -> 삭제가 불가능 (유저를 삭제하려고 할 때 블로그가 있으면 유저 삭제가 불가능
    #  models.SET_NULL -> 널값을 넣습니다 -> 유저 삭제시 블로그의 author가 null이 됨
    
    created_at = models.DateTimeField('작성일자',auto_now_add=True)
    updated_at = models.DateTimeField('수정일자',auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'
# 제목
# 본문
# 작성자 ->pass 추후
# 작성일자
# 수정일자
# 카테고리

# 작성자 -> 패스 추후 업데이트


# 썸네일이미지
# 태그
