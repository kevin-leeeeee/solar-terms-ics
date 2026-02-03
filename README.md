# 24 節氣 ICS 行事曆 (Solar Terms ICS)

這是一個自動更新的 24 節氣 ICS 訂閱源。
每年會自動計算並更新未來兩年的節氣精確時間（使用 `ephem` 天文算法，時間為 UTC+8）。

## 訂閱連結

請使用以下連結訂閱行事曆（複製連結並在 Google Calendar / Apple Calendar 中透過 URL 新增）：

**[https://raw.githubusercontent.com/kevin-leeeeee/solar-terms-ics/master/solar_terms.ics](https://raw.githubusercontent.com/kevin-leeeeee/solar-terms-ics/master/solar_terms.ics)**

*(請將 `<YOUR_USERNAME>` 替換為您的 GitHub 使用者名稱)*

## 功能
- **精確計算**：使用 Python `ephem` 庫計算太陽黃經，精確到分秒。
- **自動更新**：透過 GitHub Actions 每年自動重新計算，確保行事曆永遠包含未來兩年的資料。
- **時區支援**：事件時間已轉換為標準時間，行事曆軟體會自動調整為您當地的時區。事件描述中附帶 UTC+8 時間參考。

## 如何使用
1. **Google Calendar**: 設定 > 新增日曆 > 來自網址 > 貼上連結。
2. **iOS / macOS**: 設定 > 行事曆 > 帳號 > 加入帳號 > 其他 > 加入已訂閱的行事曆 > 貼上連結。

## 開發
- 安裝依賴: `pip install -r requirements.txt`
- 執行生成: `python main.py`
