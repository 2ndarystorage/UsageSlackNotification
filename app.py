import streamlit as st
import requests
import hashlib
import os

from datetime import datetime
try:
    from plyer import notification
    plyer_available = True
except ImportError:
    plyer_available = False

st.title("Webページ監視アプリ")
# URL入力欄と開くボタンを横並びで表示
col1, col2 = st.columns([5,1])
with col1:
    url1 = st.text_input("監視するURL1を入力してください", "https://platform.openai.com/usage")
with col2:
    if url1:
        st.markdown(f'<a href="{url1}" target="_blank"><button>URL1を開く</button></a>', unsafe_allow_html=True)
col3, col4 = st.columns([5,1])
with col3:
    url2 = st.text_input("監視するURL2を入力してください", "https://console.anthropic.com/settings/billing")
with col4:
    if url2:
        st.markdown(f'<a href="{url2}" target="_blank"><button>URL2を開く</button></a>', unsafe_allow_html=True)
col5, col6 = st.columns([5,1])
with col5:
    url3 = st.text_input("監視するURL3を入力してください", "https://console.cloud.google.com/billing")
with col6:
    if url3:
        st.markdown(f'<a href="{url3}" target="_blank"><button>URL3を開く</button></a>', unsafe_allow_html=True)
# 空エントリを除外
raw_urls = [url1, url2, url3]
urls = [u for u in raw_urls if u]
interval = st.number_input("チェック間隔(秒)", min_value=10, value=60)
notify = st.checkbox("デスクトップ通知を有効にする", value=plyer_available)
if notify and not plyer_available:
    st.warning("plyerがインストールされていないため、通知が無効化されました。")
# Slack通知用Webhook URLを直接入力する場合は以下
# slack_webhook = st.text_input("Slack Incoming Webhook URL（任意）", "https://hooks.slack.com/services/XXXX/XXXX/XXXX")

# 環境変数からWebhook URLを取得
webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
slack_webhook = st.text_input("Slack Incoming Webhook URL（任意）", value=webhook_url)

# 初回起動時にURLを開く＆Slack通知
if 'init_done' not in st.session_state:
    # 空でないURLを新しいタブで自動オープン
    if urls:
        urls_js = ";".join([f'window.open("{u}", "_blank")' for u in urls])
        st.components.v1.html(f"<script>{urls_js};</script>", height=0)
    # Slackへの起動時通知
    if slack_webhook:
        for u in urls:
            try:
                slack_resp = requests.post(slack_webhook, json={"text": f"アプリ起動: {u} を監視開始しました"})
                slack_resp.raise_for_status()
                st.info(f"{u} の起動Slack通知完了")
            except Exception as e:
                st.error(f"{u} の起動Slack通知エラー: {e}")
    st.session_state['init_done'] = True

# セッション用ハッシュ初期化
if 'prev_hashes' not in st.session_state or st.session_state.get('urls') != urls:
    st.session_state.prev_hashes = {u: None for u in urls}
    st.session_state['urls'] = urls

# 自動リロード用JavaScript埋め込み
st.components.v1.html(f"""
<script>
setTimeout(function(){{
    window.location.reload();
}}, {interval*1000});
</script>
""", height=0)

# ページ取得と比較
try:
    for u in urls:
        response = requests.get(u)
        response.raise_for_status()
        content = response.text
        current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prev = st.session_state.prev_hashes.get(u)
        if prev is None:
            st.info(f"{now} : {u} 初回チェック完了")
        elif current_hash != prev:
            st.success(f"{now} : {u} 更新を検知しました！")
            # Slackへ通知
            if slack_webhook:
                try:
                    slack_resp = requests.post(slack_webhook, json={"text": f"{now} : {u} が更新されました"})
                    slack_resp.raise_for_status()
                    st.info("Slackに通知しました")
                except Exception as slack_e:
                    st.error(f"Slack通知エラー: {slack_e}")
            if notify and plyer_available:
                notification.notify(
                    title="Webページ更新通知",
                    message=f"{u} が更新されました",
                    timeout=5
                )
        else:
            st.info(f"{now} : {u} 変更なし")
        st.session_state.prev_hashes[u] = current_hash
except Exception as e:
    st.error(f"エラーが発生しました: {e}")

# 手動Slack通知ボタン
if st.button("Slackに通知する"):
    if not slack_webhook:
        st.warning("Slack Webhook URL が設定されていません")
    else:
        for u in urls:
            try:
                slack_resp = requests.post(slack_webhook, json={"text": f"手動通知: {u} が更新されました"})
                slack_resp.raise_for_status()
                st.success(f"{u} のSlack通知完了")
            except Exception as e:
                st.error(f"{u} のSlack通知エラー: {e}") 