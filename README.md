# IoT講座 第6回 演習編 サンプルコード

このリポジトリには、IoT講座第6回演習編で使う
テストスクリプトとサンプルプログラム一式が含まれています。

---

## 📁 フォルダ構成

```
session06/
  test_data.py
  cleansing.py
  smoothing.py
  llm_normalize.py
  pipeline.py
  visualize.py
  requirements.txt
  README.md
```

---

## 💡 使い方

### 1) 必要なライブラリのインストール

Python環境で次のコマンドを実行します:

```bash
pip install -r requirements.txt
```

---

## ✅ 2) エンドツーエンド テスト実行

```bash
python pipeline.py
```

このテストは次を行います：

- 異常値・欠損値を含むデータのクレンジング
- 移動平均による平滑化
- LLM正規化テスト（OpenAI API あり／なし）
- 3つの異なるセンサーパターンテスト

---

## 📊 3) グラフ表示（Bonus Lv.1）

matplotlib を使って、データ前後の変化を可視化します。

```bash
python visualize.py
```

表示されるグラフは：

- 元の汚れたデータ
- クレンジング後データ
- 単純移動平均
- 加重移動平均
- 指数平滑化

---

## 📌 注意点

### 🔐 OpenAI API を使う場合
LLM正規化（`llm_normalize.py`）を使うには
`.env` に次を設定してください：

```
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

.env ファイルをリポジトリに含めないでください。

---

## 📚 参考資料

- YouTube動画で解説付き
- pipeline.py でシンプルな E2E テスト
- visualize.py で視覚的イメージ

---

## 📝 Licence
適宜設定してください（MIT / Apache / CC0 など）
