# AtCoder Problems Contest Builder
AtCoder Problemsで毎日開催のバーチャルコンテストを立てやすくするためのツールです。

指定した範囲のDifficultyの問題セットを作って自動で追加します。

# 使い方
## コンテストの設定
`config.py`の`contest_sets`にコンテストの設定を書き込みます。
複数のコンテストセットを登録すれば実行時にどちらを選ぶか聞かれるようになります。

プロパティは以下のようになっています。
| 名前 | 値 |
|---|---|
| name | コンテストセットの名前 |
| title | タイトル(strftimeが通されます) |
| memo | コンテストのコメント |
| everyday\_start\_time | 毎日何時に開始するか |
| duration\_second | 何秒間のコンテストか |
| penalty\_second | ペナルティは何秒か |
| problem\_infos | 抽選される問題の条件の配列 |

problem\_infosの中身は以下の形式をしたオブジェクトの配列になります。
| 名前 | 値 |
|---|---|
| difficulty\_range | Diffの最小値・最大値のタプル |
| point | 点数 |
| include\_experimental | 試験管Diffを含むか |
| duplicate\_remove\_days | 直近何日の問題を抽選から除外するか |

## 実行
`main.py` を実行するとconfigの通りにバチャが立ちます。

```
$ python3 main.py
作成するコンテストの開催日を入力してください（YYYY-MM-DD）: 2023-02-23
AtCoder Problemsのトークンを入力してください: gho_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
コンテストを作成しました: https://kenkoooo.com/atcoder/#/contest/show/2266400f-18f4-44f7-9402-8a8c1fce55ce
コンテストの問題を設定しました
完了しました
```

初回は開催日が聞かれるので入力します。
トークンはAtCoder Problemsにログインしたブラウザに保存されているCookieから確認してコピペします。

```
$ python3 main.py
次回のコンテストは2023-02-24に設定されています
変更しますか？（y/n）: n
AtCoder Problemsのトークンを入力してください: gho_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
コンテストを作成しました: https://kenkoooo.com/atcoder/#/contest/show/2266400f-18f4-44f7-9402-8a8c1fce55ce
コンテストの問題を設定しました
完了しました
```

前回2023-02-23のコンテストを立てれば、翌日である2023-02-24が提案されます。
変更しますか？のあと`y`を入力すれば設定し直すこともできます。
