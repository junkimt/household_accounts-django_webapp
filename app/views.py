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
        dbname = 'db.sqlite3'
        query = 'SELECT * FROM app_item;'
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        cursor.execute(query)

        data = []
        for row in cursor.fetchall():
            x = dict(zip([d[0] for d in cursor.description], row))
            data.append(x)

        dic = {}
        for d in data:
            for k,v in d.items():
                if k in dic.keys():
                    dic[k].append(v)
                else:
                    dic[k] = []

        conn.close()


        #### total spend ####
        balance = 50000
        dic['price'] = [v for v in dic['price'] if v is not None]
        total_spend = sum(dic['price'])
        dic['total_spend'] = (balance - total_spend) / balance * 100
        #print(total_spend)
        #print(dic['total_spend'])

        #### total spend every cost item ####
        total_spend_dic = {}
        for d in data:
            if not d['cost_item'] in total_spend_dic.keys():
                total_spend_dic[d['cost_item']] = 0
            if d['price'] is None:
                continue
            total_spend_dic[d['cost_item']] += d['price']
        #print(total_spend_dic)
        #total_spend_list = [{'name':k, 'value':v} for k,v in total_spend_dic.items()]
        total_spend_list = []
        for k,v in total_spend_dic.items():
            if k is None:
                k = '入力なし'
            total_spend_list.append({'name':k, 'value':v})
        dic['total_spend_list'] = total_spend_list
        #print(dic['total_spend_list'])

        dic['total_spend_keys'] = list(total_spend_dic.keys())
        dic['total_spend_values'] = list(total_spend_dic.values())

        dic['json_ts'] = json.dumps(total_spend_list, indent=4, ensure_ascii=False)

        dic['list_val'] = [10000, 25000]
        dic['dict_val'] = {'a':8000, 'b':3000}

        #### 日付と支出の折れ線グラフ ###
        line_graph_dic = {}
        for d in data:
            date = d['date']
            if date is None:
                continue
            date = date.split('-')
            year_day_key = '{0}-{1}'.format(date[0], date[1])
            year_day_key = int(date[2])
            if not year_day_key in line_graph_dic.keys():
                line_graph_dic[year_day_key] = 0
            if d['price'] is None:
                continue
            line_graph_dic[year_day_key] += d['price']
        line_graph_list = []
        for k,v in line_graph_dic.items():
            line_graph_list.append({'name':k, 'value':v})
        dic['line_graph_list'] = line_graph_list
        print('==========aiueo')
        print(dic['line_graph_list'])

        line_graph_list_2 = []
        for k,v in line_graph_dic.items():
            line_graph_list_2.append([k, v])
        dic['line_graph_list_2'] = line_graph_list_2

        #### 日付と支出の折れ線グラフ every month ###
        line_graph_dic = {}
        for d in data:
            date = d['date']
            if date is None:
                continue
            date = [int(s) for s in date.split('-')]
            #year_month_key = '{0}年 {1}月'.format(date[0], date[1])
            year_month_key = 'ym-{0}-{1}'.format(date[0], date[1])
            day = int(date[2])
            if not year_month_key in line_graph_dic.keys():
                _, month_day = calendar.monthrange(date[0], date[1])
                line_graph_dic[year_month_key] = [[i, 0] for i in range(month_day+1)]
            if d['price'] is None:
                continue
            print('-----', year_month_key, day)
            print(day, line_graph_dic[year_month_key][day], len(line_graph_dic[year_month_key]))
            line_graph_dic[year_month_key][day][1] += d['price']

        print('=====')
        print(line_graph_dic)

        dic['line_graph_dic_every_month'] = line_graph_dic


        ########
        total_spend = sum([d['value'] for d in total_spend_list])
        total_spend_rate_list = []
        for d in total_spend_list:
            total_spend_rate_list.append(
                    {'name':d['name'], 'value':int(d['value'] / total_spend * 100)}
                    )
        dic['total_spend_rate_list'] = total_spend_rate_list




        #return self.render_to_response(data)
        return render(request, self.template_name, dic)
