# 💰 Income Bucket Dashboard
**A Technical Screener for Covered Call Yields**

This dashboard identifies high-yield covered call opportunities using a "Double Covered" approach for income funds (like QQQI) and a "Theta-Harvesting" approach for high-liquidity tech stocks.

---

### 🛠 Strategy & Filters
* **Trend Filter:** Only stocks trading above their **200-day Simple Moving Average (SMA)** are included to ensure we aren't "catching a falling knife."
* **Entry Timing:** High **RSI (14)** values (above 70) indicate overbought conditions—the ideal time to sell call premium.
* **Goal:** Target **1.5% - 3.0% Monthly Yield** (Period Return) while maintaining downside protection.

---

### 📊 Live Yield Scan
*The table below updates automatically every trading day.*

| Ticker | Price | RSI | Strike | Premium | Period Yield % | Annualized % | Protection % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| *Running initial scan...* | | | | | | | |
---

### ⚠️ Risk Disclaimer
Selling covered calls caps your upside potential. If a stock rallies past your strike, your shares may be called away. Always monitor the **Ex-Dividend date** (especially for QQQI) to avoid early assignment.

*Last automated update: 2026-03-07*
