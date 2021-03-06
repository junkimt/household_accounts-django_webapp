# KAKEIBO（家計簿アプリ）

## 概要
家計簿データ（日付，費目，名前，値段）などを入力・編集可能なDjangoのアプリケーションです。
<br>
月ごとに「毎日どれくらいお金を使っているか」，「費目ごとにどれくらいの割合でお金を使っているか」をグラフで表示したページを作成しました。

## 使い方

（db.sqlite3を読み込んでデモを実行します）

MacOS/Linux用準備コマンド

1. git clone https://github.com/junkimt/household_accounts-django_webapp
2. cd household_accounts-django_webapp
3. python3 -m venv kakeibo
4. source kakeibo/bin/activate
5. pip install -r requirements.txt
6. python manage.py runserver
7. ブラウザで`http://127.0.0.1:8000`にアクセス


## 機能紹介

### トップページ

家計簿を入力するページです。
<br>
1ページに最新の10個のデータを表示し，それ以外のデータは次のページに表示されます。

![トップページ](./imgs/top_page.png)


### 前のページ，次のページ

- ページの左下にあるボタン（<< 1 2 3 >>）でページの移動を実行します。

  ![ページを移動した結果](./imgs/top_page_2.png)

### 新規

- 家計簿データを新規作成します。

  ![登録・更新ページ](./imgs/register_page.png)

### 検索

- 入力されている家計簿データから絞り込みして表示ができます。

  ![検索ページ](./imgs/search_page.png)

- 検索条件を入力します。

  ![検索条件の入力](./imgs/search_condition.png)

- 検索結果が表示されます。
- 検索結果の表示を終了する場合は，左上にあるグレーのボタン（検索を解除）を押します。

  ![検索結果の表示](./imgs/search_result.png)

### 削除

- 入力されている家計簿データを削除できます。

  ![削除](./imgs/delete_page.png)

### 月ごとにグラフで見る

- 新しいページで家計簿データを月ごとにグラフで見ることができます。

- 毎日どれくらい使っているか

  - 日毎にどれくらいお金を使っているかを見ることができます。
  - 大きな出費をした日を把握することができます。

- 費目ごとにどれくらい使っているか

  - お金の使い方に偏りがあるかどうか確認できます。
  - どの費目にどれくらい使いたいかの目安を考えることができます。

- 月ごとにグラフを表示

  ![月ごとにグラフで見る 2019年04月](./imgs/visualization_page_1.png)

  ![月ごとにグラフで見る 2019年05月](./imgs/visualization_page_2.png)

  ![月ごとにグラフで見る 2019年06月](./imgs/visualization_page_3.png)

## Requirement

```
Django==2.1.15
django-crispy-forms==1.7.2
django-filter==2.0.0
pytz==2018.5
pandas==0.23.4
```

## 参考
[okoppe8/instant-django](https://github.com/okoppe8/instant-django) をベースにプログラムを作成。
