# Webページ監視アプリ

このアプリは Streamlit で作られたシンプルな Web ページ更新監視ツールです。最大 3 つの URL を定期的にチェックし、更新を検知したときに Slack とデスクトップ通知（plyer をインストールしていれば）でお知らせします。

---

## ⭐️ 主な機能

- **複数 URL 監視**: 最大 3 つの URL を同時に監視
- **差分検知**: ページ内容の SHA256 ハッシュを比較して更新を検知
- **Slack 通知**: Incoming Webhook による通知 (環境変数または入力欄から設定)
- **デスクトップ通知**: plyer を使ってローカルに通知
- **初回起動時オープン**: アプリ起動時に指定 URL をブラウザで自動オープン
- **手動通知ボタン**: いつでも Slack に手動通知できるボタン

## 💻 動作環境・依存ライブラリ

- Python 3.7 以上
- ライブラリ:
  - `streamlit`  
  - `requests`  
  - `hashlib` (標準ライブラリ)  
  - `plyer` (デスクトップ通知機能を使う場合)

### インストール例
```bash
pip install streamlit requests plyer
```

## ⚙️ 設定

1. Slack の **Incoming Webhook URL** を発行し、環境変数 `SLACK_WEBHOOK_URL` に設定するか、アプリ起動後の入力欄にコピペして使います。
Windowsの場合、環境変数にSLACK_WEBHOOK_URLという名前でSlackのWebhook URLを保存しておいてもよい。
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX"
   ```
2. **plyer** を入れておくとデスクトップ通知も有効化されます。

## 🚀 使い方

1. ターミナルからアプリを起動：
   ```bash
   streamlit run app.py
   ```
2. 表示された画面で：
   - 監視したい URL1～3 を入力
   - 必要なら「デスクトップ通知を有効にする」をチェック
   - Slack Webhook URL が空の場合は入力
3. アプリ起動時に自動で URL を別タブで開く
4. 指定秒数ごとにページをリロードし、更新を検知したら通知
5. 「Slack に通知する」ボタンで任意タイミングの手動通知も可能

## 💡 注意点

- ブラウザのポップアップブロックが有効だと自動オープンが抑制されるので、許可設定をお願いします。
- プライベートページや認証が必要なサイトは別途認証処理が必要です。

---

© 2024 あなたの名前 or Your Organization 

---

## Program Summary
- Streamlit app that monitors up to three URLs, hashes page content, and alerts on changes.
- Sends notifications via Slack Incoming Webhook and optionally desktop notifications (plyer).
- Auto-opens the monitored URLs in new browser tabs on first load.

## How to Use
- Install dependencies: `pip install streamlit requests plyer`
- Set `SLACK_WEBHOOK_URL` or enter it in the UI.
- Run: `streamlit run app.py`
- Not verified.

## Completion Status
- Usable: Core monitoring and notification flow is implemented in `app.py`, but behavior (auth-protected pages, popup blockers, Slack setup) depends on environment and is not verified here.

## Program Summary
- Streamlit-based URL monitor that fetches each page, hashes content, and reports changes on a timed reload cycle.
- Sends Slack notifications on startup and on detected updates; optional desktop notifications via `plyer`.
- Provides per-URL “open in new tab” buttons and auto-opens URLs on first load.

## How to Use
- Install dependencies: `pip install streamlit requests plyer`
- Set `SLACK_WEBHOOK_URL` (or enter it in the UI), then run: `streamlit run app.py`
- Adjust interval, enter up to three URLs, and keep the app open to monitor.
- Not verified.

## Completion Status
- Usable: Core monitoring, Slack notification, and basic UI flows are in place, but behavior depends on site access/auth and client-side popup/auto-reload constraints; not verified.

## Program Summary
- Streamlit UI to monitor up to three URLs by hashing response bodies and detecting changes on reload.
- Sends Slack Incoming Webhook messages on app start, on detected updates, and via a manual button; optional desktop notifications if `plyer` is installed.
- Auto-opens monitored URLs in new tabs on first load and reloads the page on a timer.

## How to Use
- Install dependencies: `pip install streamlit requests plyer`
- Set `SLACK_WEBHOOK_URL` or enter it in the UI, then run: `streamlit run app.py`
- Enter up to three URLs, set the check interval, and keep the app open to monitor.
- Not verified.

## Completion Status
- Usable: Core monitoring, Slack notifications, auto-reload, and basic UI are implemented in `app.py`, but behavior depends on site access/auth and browser popup/reload constraints; not verified.
