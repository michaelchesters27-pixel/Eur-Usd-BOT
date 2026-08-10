# EUR/USD 5×5 Campaign Bot

This is one complete project containing:

- an MT5 Expert Advisor for EUR/USD;
- a Railway-hosted live dashboard and control API;
- persistent dashboard settings;
- automated tests for the Railway service.

## Locked bot behaviour

1. A campaign places **5 Buy Stops and 5 Sell Stops** around the current EUR/USD price.
2. Every pending order has its own take-profit.
3. The whole campaign has a fixed **$5 combined profit target**. Combined profit means realised campaign profit plus current floating profit/loss.
4. At $5, the EA closes every open campaign trade, deletes every untriggered order and begins a fresh 5×5 campaign.
5. The Railway dashboard accepts any positive **overall profit target** and **maximum loss**. These apply to the complete run across all campaigns.
6. When the next order on one side triggers, every earlier open order on that same side moves to breakeven:
   - Buy 2 protects Buy 1;
   - Buy 3 protects Buy 1 and Buy 2;
   - the rule continues through Buy 5 and is identical for sells.
7. When combined campaign P/L first becomes positive, a $0 campaign floor is armed. If it returns to $0, every open campaign trade closes and all remaining pending orders are deleted. A fresh campaign then begins.
8. When the overall profit target or maximum loss is reached, everything closes, all pending orders are deleted and the bot stops.
9. The dashboard has one trading control: **TURN BOT OFF**. It performs the same full close, delete and stop operation.
10. After OFF, remove and reattach the EA in MT5 to begin a new run. The same attached session cannot turn itself back on.

Market execution can slip by a few cents around an exact money threshold. The EA acts on the first tick at or beyond the threshold.

## Current adjustable MT5 inputs

The order spacing and individual order TP were not yet locked, so they are safe MT5 inputs and do not require another code build:

- first pending order distance: **5 pips** by default;
- spacing between pending orders: **5 pips** by default;
- individual TP distance: **5 pips** by default;
- lot size: **0.01** by default;
- breakeven price offset: **0 pips** by default.

The EA requires an **MT5 hedging account** because individual ladder positions must remain separate.

## Deploy the Railway dashboard

1. Put this project in a GitHub repository.
2. In Railway, create a new project from that repository.
3. Add a Railway volume mounted at `/data` so limits and OFF state survive restarts.
4. Add these Railway variables:

   ```text
   BOT_API_KEY=make-this-a-long-private-key
   DASHBOARD_PASSWORD=your-private-dashboard-password
   SECRET_KEY=make-this-another-long-private-key
   STATE_DB_PATH=/data/eurusd-5x5.db
   ```

5. Generate the Railway public domain. Opening it displays the dashboard.

## Compile and attach the MT5 EA

1. Open MetaTrader 5.
2. Press **F4** to open MetaEditor.
3. Open the `MQL5/Experts` folder.
4. Copy `mt5/EURUSD_5x5_CampaignBot.mq5` into that folder.
5. Open the file and press **F7** to compile it.
6. In MT5 go to **Tools → Options → Expert Advisors**.
7. Tick **Allow WebRequest for listed URL** and add your Railway address, for example:

   ```text
   https://your-service.up.railway.app
   ```

8. Open an EUR/USD M5 chart and attach the EA.
9. In the EA inputs, paste the same Railway URL and `BOT_API_KEY` used in Railway.
10. Enable Algo Trading.

Enter the overall profit target and maximum loss on the dashboard **before attaching the EA**. If they are not set, the EA waits and places no orders.

## Backtest in MT5

For an offline MT5 Strategy Tester run:

1. Choose `EURUSD_5x5_CampaignBot` and EUR/USD.
2. Select M5 and **Every tick based on real ticks**.
3. Set `InpUseRailway` to `false`.
4. Type the test's overall target into `InpTesterOverallProfitTarget`.
5. Type the maximum loss into `InpTesterMaximumLoss`.
6. Keep `InpCampaignTargetMoney` at `5.0`.
7. Test different spacing and individual TP values through the MT5 Inputs tab.

## Run the Railway tests locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```
