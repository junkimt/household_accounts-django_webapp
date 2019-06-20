from django.db import models

from users.models import User


class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    select_items = ['支出', '収入']
    select_items = tuple((s, s) for s in select_items)
    inc_or_exp = models.CharField(
        verbose_name='費目',
        max_length=20,
        choices=select_items,
        blank=True,
        null=True,
        default='支出',
    )

    select_items = ['食費', '日用品', '娯楽費', '特別費']
    select_items = tuple((s, s) for s in select_items)
    cost_item = models.CharField(
        verbose_name='費目',
        max_length=20,
        choices=select_items,
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name='名前',
        max_length=20,
        blank=True,
        null=True,
    )

    price = models.IntegerField(
        verbose_name='値段',
        blank=True,
        null=True,
    )

    purchase_place = models.CharField(
        verbose_name='購入場所',
        max_length=20,
        blank=True,
        null=True,
    )

    memo = models.TextField(
        verbose_name='メモ',
        blank=True,
        null=True,
    )

    select_items = ['わるいね', 'ふつう', 'いいね']
    select_items = tuple((i, s) for i,s in enumerate(select_items))
    evaluation = models.IntegerField(
        verbose_name='評価',
        choices=select_items,
        blank=True,
        null=True,
    )


    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.name

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サンプル'
        verbose_name_plural = 'サンプル'
