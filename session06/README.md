# session06 (IoT講座 第6回 演習編)

## ファイル構成

- cleansing.py       : STEP1 統計的クレンジング
- smoothing.py       : STEP2 平滑化フィルタ
- llm_normalize.py   : STEP3 LLM正規化(OpenAI)
- pipeline.py        : STEP4 E2Eテスト
- visualize.py       : Bonus Lv.1 matplotlibグラフ化
- test_data.py       : テストデータ生成
- requirements.txt   : 依存ライブラリ一覧

---

## セットアップ

```bash
pip install -r requirements.txt
```

.env ファイルを作成してAPIキーを設定します。

```
OPENAI_API_KEY=sk-xxxx
```

---

## 実行方法

### E2Eテスト実行

```bash
python pipeline.py
```

### Bonus Lv.1 グラフ化

```bash
python visualize.py
```

matplotlibのウィンドウが開き、以下を比較できます。

- 汚れたデータ
- クレンジング後データ
- 移動平均
- 加重移動平均
- 指数平滑化

---