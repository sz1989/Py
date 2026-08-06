import os
import time
from datetime import datetime
from decimal import Decimal
import yfinance as yf

def fetch_ticker_data(ticker_symbols: str):
    return yf.Tickers(ticker_symbols)

def calculate_weighted_change(ticker_obj, weight: float):
    fast_info = ticker_obj.fast_info
    current_price = fast_info["lastPrice"]
    previous_close = fast_info["previousClose"]
    pct_change = ((current_price - previous_close) / previous_close) * 100
    return pct_change, (weight / 100) * pct_change

def display_header():
    os.system("cls" if os.name == "nt" else "clear")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔄 FSPCX LIVE PREDICTOR | Last Refreshed: {current_time}")
    print("=" * 60)

def predict_nav(yesterday_nav: Decimal, holdings: dict) -> None:
    """ Predicts the NAV of a mutual fund based on the live intraday price changes of its"""
    total_weight = sum(holdings.values())
    ticker_symbols = " ".join(holdings.keys())

    while True:
        display_header()
        weighted_sum = 0.0

        try:
            tickers_data = fetch_ticker_data(ticker_symbols)

            for ticker, weight in holdings.items():
                try:
                    ticker_obj = tickers_data.tickers[ticker]
                    pct_change, weighted_impact = calculate_weighted_change(ticker_obj, weight)
                    weighted_sum += weighted_impact

                    print(f"{ticker:<5} | Weight: {weight:>5}% | "
                          f"Change: {pct_change:>+6.2f}% | Impact: {weighted_impact:>+6.2f}%")

                except Exception as e:
                    print(f"⚠️ Error parsing data for {ticker}: {e}")

            print("-" * 60)

            estimated_change = weighted_sum / (total_weight / 100)
            predicted = yesterday_nav * (1 + Decimal(str(estimated_change)) / 100)

            print(f"Top 10 Aggregate Weight:  {total_weight:.2f}%")
            print(f"Estimated Fund % Change:  {estimated_change:>+6.2f}%")
            print(f"Yesterday's Base NAV:     ${yesterday_nav:.2f}")
            print(f"🚀 PREDICTED TODAY'S NAV: ${predicted:.2f}")
            print("=" * 60)
            print("Ctrl+C to stop the live tracking.")

        except Exception as network_error:
            print(f"⚠️ Network error while fetching data: {network_error}")
            print("Retrying...")

        time.sleep(60)

def load_holdings(name_of_fund: str) -> dict:
    if name_of_fund.lower() == "fspcx":
        # Official top 10 holdings and percentages from Fidelity 
        return {
            "CB": float("13.68"),   # Chubb Ltd.
            "PGR": float("9.64"),   # Progressive Corp.
            "AJG": float("7.95"),   # Arthur J. Gallagher
            "HIG": float("6.13"),   # Hartford Financial
            "RGA": float("6.11"),   # Reinsurance Group
            "TRV": float("5.49"),   # Travelers Companies
            "AFG": float("4.77"),   # American Financial
            "ACGL": float("4.70"),  # Arch Capital Group
            "MET": float("4.64"),   # MetLife Inc.
            "AON": float("4.61")    # Aon PLC
        }
    raise ValueError(f"Holdings for fund '{name_of_fund}' are not implemented.")
    

if __name__ == "__main__":
    # Update this value with the most recent official closing price before running
    YESTERDAY_CLOSING_NAV = Decimal("97.52") 
    
    try:
        predict_nav(YESTERDAY_CLOSING_NAV, load_holdings("fspcx"))
    except KeyboardInterrupt:
        print("\n👋 Live tracking stopped by user.")
