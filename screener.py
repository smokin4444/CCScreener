import yfinance as yf
import pandas as pd
from datetime import datetime
import re

def get_income_scan(tickers):
    final_list = []
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="2y")
            if df.empty or len(df) < 200: continue
            
            # Flatten columns for 2026 Yahoo format
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Technicals using pure Pandas (No pandas-ta needed)
            current_price = df['Close'].iloc[-1]
            # Simple Moving Average
            sma_200 = df['Close'].rolling(window=200).mean().iloc[-1]
            
            # RSI Logic
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            
            # Trend Check
            if current_price < sma_200: continue 

            # Options Selection
            expiries = ticker.options
            if not expiries: continue
            target_expiry = expiries[1] if len(expiries) > 1 else expiries[0]
            days_to_exp = (datetime.strptime(target_expiry, '%Y-%m-%d') - datetime.now()).days
            
            chain = ticker.option_chain(target_expiry).calls
            otm_calls = chain[chain['strike'] > current_price * 1.03]
            if otm_calls.empty: continue
            
            best_call = otm_calls.iloc[0]
            period_yield = (best_call.bid / current_price)
            annualized = period_yield * (365 / max(days_to_exp, 1))

            final_list.append({
                "Ticker": symbol, "Price": round(current_price, 2),
                "RSI": round(rsi, 1), "Strike": best_call.strike,
                "Premium": best_call.bid, "Period Yield %": f"{period_yield:.2%}",
                "Annualized %": f"{annualized:.1%}", "Protection %": f"{period_yield:.2%}"
            })
        except: continue
    return pd.DataFrame(final_list)

# Execution and README Update
my_watch = ['QQQI', 'SPYI', 'NVDA', 'AMD', 'AAPL', 'MSFT', 'TSLA']
df_results = get_income_scan(my_watch)
markdown_table = df_results.sort_values("Period Yield %", ascending=False).to_markdown(index=False) if not df_results.empty else "No data met filters."

with open("README.md", "r") as f:
    content = f.read()

new_content = re.sub(r".*", 
                     f"\n{markdown_table}\n", 
                     content, flags=re.DOTALL)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
new_content = re.sub(r"Last automated update:.*", f"Last automated update: {now}", new_content)

with open("README.md", "w") as f:
    f.write(new_content)
