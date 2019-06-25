from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from django.shortcuts import render

from .filters import ItemFilterSet
from .forms import ItemForm
from .models import Item

import sqlite3
import json
from datetime import datetime
import calendar
from copy import deepcopy
import pandas as pd


# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin

class ItemFilterView(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Item

    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return Item.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        return super().get_context_data(object_list=object_list, **kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
    """
    ビュー：詳細画面
    """
    model = Item

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        return super().get_context_data(**kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """
        item = form.save(commit=False)
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        更新処理
        """
        item = form.save(commit=False)
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Item
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(self.success_url)


########################################

class AboutView(TemplateView):
    template_name = 'app/about.html'

    def get(self, request, **kwargs):

        # about.html へ渡す変数の辞書
        dic = {}

        # sqliteにクエリ送信しデータ取得
        dbname = 'db.sqlite3'
        query = 'select * from app_item;'
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        cursor.execute(query)

        # sqlite3からpandasのDataframeとしてデータを取得
        df = pd.read_sql(query, conn)
        conn.close()

        # 日付データから年月，日のデータの列を追加
        year_months = ['-'.join(s.split('-')[:2]) for s in df['date']]
        df['year_month'] = year_months
        days = [s.split('-')[2] for s in df['date']]
        df['day'] = days

        # 支出と収入のデータを分割
        inc_df = df[df['inc_or_exp']=='収入']
        exp_df = df[df['inc_or_exp']=='支出']


        #### about.htmlで必要なデータを各月ごとに取得 ####

        year_month_keys = sorted(list(set(exp_df['year_month'])))
        int_year_months = {k:[int(s) for s in k.split('-')] for k in year_month_keys}

        dic['nb_swiper_slider'] = len(year_month_keys) - 1

        costitem_keys = list(set(exp_df['cost_item']))

        ## 一日ごとの使用金額を取得
        # 各月が何日あるか取得
        month_ranges = {k: calendar.monthrange(li[0], li[1])[1] for k,li in int_year_months.items()}
        # 各日の合計金額を算出
        day_exp_sum = dict(exp_df.groupby(['year_month', 'day'])['price'].sum())
        # 該当する月の全日のデータを作成
        day_exp = {k:[[i,0] for i in range(v+1)] for k,v in month_ranges.items()}
        for (k_ym, k_d),v in day_exp_sum.items():
            day_exp[k_ym][int(k_d)][1] = v
        dic['day_exp'] = day_exp
        #print(day_exp)

        ## １日ごとの累積使用金額を取得
        day_accum_exp = deepcopy(day_exp)
        for k,v in day_exp.items():
            accum = 0
            for idx, vv in enumerate(v):
                accum += vv[1]
                day_accum_exp[k][idx][1] = accum
        dic['day_accum_exp'] = day_accum_exp

        ## 各費目ごとの使用金額を取得
        costitem_exp_sum = dict(exp_df.groupby(['year_month', 'cost_item'])['price'].sum())
        costitem_exp = {k:[] for k in year_month_keys}
        for (k_ym, ci),v in costitem_exp_sum.items():
            costitem_exp[k_ym].append({'name':ci, 'value':v})
        dic['costitem_exp'] = costitem_exp
        #print(costitem_exp)

        ## 各費目ごとの使用金額の割合を取得
        costitem_rate_exp = {k:[] for k in year_month_keys}
        for k,v in costitem_exp.items():
            total_exp = sum([d['value'] for d in v])
            for d in v:
                costitem_rate_exp[k].append(
                        {'name':d['name'], 'value':round(d['value'] / total_exp * 100)})
        dic['costitem_rate_exp'] = costitem_rate_exp
        #print(costitem_rate_exp)



        #return self.render_to_response(data)
        return render(request, self.template_name, dic)
