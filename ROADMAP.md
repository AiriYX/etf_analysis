# First-Time Investor Planner (ETFs, Stocks and More) — Project Roadmap

## 1. Problem definition

### The problem
Young first-time investors often set a goal like "I want 8% a year" without knowing whether their choices can get them there. Most end up in one of two traps:
- **Too safe:** the money stays in savings and quietly falls short of the goal.
- **Too risky:** they chase a hot stock or tech fund, hit a loss they didn't expect, and sell at the bottom.

Existing tools don't help much. Robo-advisor questionnaires give one allocation with no explanation. Brokerage calculators draw a single straight line at an assumed return. Neither shows **the range of possible outcomes**, **the losses in dollars along the way**, or **how the answer changes with how much someone has and how experienced they are**.

**Problem statement (one sentence for the pitch):**
> First-time investors can't see how likely each of their options is to reach their return goal, or what losses they'd have to sit through, so they choose too safely or too riskily. This project quantifies both for each type of beginner and turns the result into a personal pathway.

**What would count as success:** for each persona, a recommendation with a probability of reaching the goal and a bad-case loss in dollars, backed by a tested model and shown in a way a beginner can follow.

**Hypotheses the analysis will test:**

| # | Hypothesis | Test |
|---|---|---|
| H1 | A diversified ETF mix gives a higher P(hit 8%) than savings, and a smaller bad-case drawdown than a single stock, for all 9 size × style personas | Monte Carlo (section 4b) |
| H2 | For small investors, changing contributions ($100 → $300/mo) moves P(hit target) more than changing allocation (0% → 100% QQQ) | Monte Carlo, Starter profile |
| H3 | 60/40 and equal-weight sectors have no significant difference in risk-adjusted return | A/B test (section 4c) |
| H4 | Random 5-stock portfolios beat SPY less than half the time over 5-year windows | Pick-5 test |
| H5 | An offensive risk style raises P(hit target) more for a Starter than for a lump-sum investor | Style × size test |

Any of these could turn out false. That's fine: a rejected hypothesis is still a finding, and the recommendation follows whatever the data says.

### Target audience

> **US young adults (roughly 18–35) who have never invested, or only just started, with $1k–$50k to invest or $100–$1,000/month to save, and a return goal in mind (x%) but no plan for reaching it.**

They are weighing the usual beginner options: leaving money in savings, bonds, index ETFs, or picking stocks themselves. They want to see how each option could grow their money, and which one gives them the best chance of reaching the target without losses they can't stomach.

ETFs are the evidence-based core of the recommendation, but the project **doesn't assume that up front**. It puts every option side by side and lets the data show why diversified funds usually win for beginners, and when they don't.

**Who it's *not* for (state this in the pitch):**
- Retirees or anyone who needs the money as income within ~2 years. The 5-year horizon doesn't fit them.
- Active traders and options or margin users.
- Anyone needing tax or account-type advice (401k vs IRA vs brokerage). That stays out of scope.
- Non-US investors, since the data uses US funds and US Treasury rates.

### Four ways the audience differs
Each person is described by four questions. The web app asks them in a short onboarding flow, and each one maps to a part of the analysis:

| Question | Options | What it changes |
|---|---|---|
| **Level:** how ready and experienced are you? | Level 1–4 (below) | Which **pathway** they see and which options are unlocked |
| **Size:** how much money? | Starter / Builder / Lump sum, or custom amounts | Contributions, whole-share issues, losses in dollars |
| **Risk style:** how much loss can you live with? | Defensive / Balanced / Offensive | Drawdown limit, bond range, stock slice allowed |
| **Goal:** what return do you want? | x% (4–12%) | Target line and P(hit target) |

**Level is not the same as risk style.** An experienced investor can be defensive, and a nervous beginner can have a long horizon. Level controls **what we show them and in what order**; risk style controls **which mix fits them**.

### Levels and pathways
Level is the experience dimension. Each level gets a **pathway**: an ordered set of steps, each backed by a chart from the analysis. Higher levels unlock more options in the growth explorer, so a true beginner isn't overwhelmed by 8 lines and a stock picker on day one.

| Level | Who | How we detect it (onboarding) | Pathway steps | Options unlocked |
|---|---|---|---|---|
| **1. Getting ready** | No emergency fund, or carrying high-interest debt | "Do you have 3+ months of expenses saved?" and "Any debt above ~8% interest?" | ① Build an emergency fund in savings/T-bills ② Pay off high-interest debt first. Paying off a 22% credit card is a guaranteed 22% "return," far above any x% target ③ Then start a small monthly investment | Savings, SPY |
| **2. First investment** | Ready, but has never invested | "Have you ever bought a stock or fund?" → no | ① Why one broad fund beats picking (savings vs SPY vs one stock) ② Choose one fund for your risk style (SPY or 60/40) ③ Automate monthly contributions; see contributions vs. allocation | + Bonds, 60/40, one stock (for comparison only) |
| **3. Building a mix** | Has a fund or two, wants to improve | "Do you already own a fund?" → yes | ① Your best QQQ:SPY:bond mix (Monte Carlo) ② What the bad case looks like in dollars ③ How to rebalance with contributions | + QQQ, best mix for you |
| **4. Exploring stocks** | Has a core portfolio, curious about individual stocks | "Do you want to pick individual companies?" → yes | ① Core + small stock slice (10–20%) ② Hindsight bias: random big company vs NVDA ③ Pick-5 test: how often stock pickers beat SPY | + Pick 5 stocks, stock slice |

**Rules:**
- **Level 1 doesn't model debt payoff.** It only compares the debt's interest rate with the target return and shows a message. No new data needed.
- **Pathways are mostly content plus filters,** not new models. Each step reuses a view that already exists (growth explorer, persona grid, sleeve test, pick-5 test), filtered to the user's level, size and style.
- **The Tableau version** uses a Level parameter on Dashboard 1 that hides locked options. The full step-by-step pathway lives in the web app (section 7c).

### Example personas (for the pitch and the demo)
Three fictional people that together cover the levels, sizes and styles:

| Persona | Level | Size | Style | Story |
|---|---|---|---|---|
| **Jordan, 22**, first job | 1 → 2 | Starter ($1k + $200/mo) | Offensive | Has a $2k credit card balance at 24%. The pathway says pay that off first, then automate $200/mo into one fund. |
| **Priya, 28**, a few years of saving | 3 | Builder ($10k + $500/mo) | Balanced | Owns some SPY and wonders whether to add QQQ. Monte Carlo shows the best mix and the bad case in dollars. |
| **Sam, 31**, got an inheritance | 2 → 4 | Lump sum ($50k) | Defensive | Wants to "buy NVDA." The pathway shows the hindsight trap and a small-slice alternative. |

### The options a beginner is choosing between

| Option | What it represents | How it's modeled | Data |
|---|---|---|---|
| **Savings / T-bills** | "Keep it safe" (high-yield savings, CDs, T-bills) | 3-month Treasury yield, compounded monthly | Alpha Vantage |
| **Bonds** | Low-risk investing | BND | yfinance |
| **Balanced fund** | Classic 60/40 | 60% SPY / 40% BND | yfinance |
| **Whole market** | One-fund investing | SPY | yfinance |
| **Tech-heavy** | Growth tilt | QQQ | yfinance |
| **One famous stock** | "I'll just buy a company I like" | A random pick from the 10 largest US companies in 2008 | yfinance |
| **Pick 5 stocks** | DIY stock picker | 5 random picks from the 20 largest US companies in 2008 | yfinance |
| **Best mix for you** | The model's recommendation | Best QQQ:SPY:bond (+ optional stock slice) mix for the user's persona (section 4b) | yfinance |
| *Crypto (stretch)* | What many beginners ask about | BTC-USD, analyzed on its own shorter 2015+ window | yfinance |

**Why crypto is only a stretch goal:** Bitcoin data starts in late 2014. Putting it in the main simulation would shrink every other option's history to 2015 onward and remove the 2008 crash. If you add it, compare it separately on the 2015+ window and say so.

"I want x% return" doesn't give us anything to test, so we turn it into three measurable parts:

| User says | We measure |
|---|---|
| "I want x% a year" | Target value = what the user's money would grow to at exactly x%/yr over a **5-year horizon** (including any monthly contributions) |
| "...and I want to actually get there" | **P(hit target)** from 10k Monte Carlo paths |
| "...without losing my shirt" | **95th-percentile worst max drawdown**, shown as a % *and* in dollars |

**Default x = 8%** (close to the long-run US stock average). It is a **Tableau parameter** and a **web-app slider** (4–12%) so users can set their own target.

### Investor size matters: three profiles
A % return is the same at any size, but a lot of other things are not. The project models three **investor profiles** instead of a single $50k case:

| Profile | Start | Monthly contribution | Typical person |
|---|---|---|---|
| **Starter** | $1,000 | $200 | Student or first job; contributions matter more than allocation |
| **Builder** | $10,000 | $500 | A few years of savings |
| **Lump sum** | $50,000 | $0 | Inheritance or bonus to invest once (the original brief) |

The profiles are rows in a database table, and the Tableau and web-app sliders let users enter their own numbers.

**What changes with size (and how we handle it):**

| Issue | $1k investor | $50k investor | How the project handles it |
|---|---|---|---|
| **Contributions vs. allocation** | Over 5 years, $200/mo adds $12k, so savings rate drives the outcome far more than QQQ:SPY | Allocation dominates | Monte Carlo includes monthly contributions; a "what matters more" chart compares allocation changes with contribution changes |
| **Whole shares** | One SPY or QQQ share costs hundreds of dollars, so a 70/30 split or 9 sector ETFs can't be built without fractional shares | Any split is achievable | An **implementability check**: the smallest start amount at which each portfolio can be built within ±2% of its target weights using whole shares; flag "needs a broker with fractional shares" |
| **Rebalancing** | Rebalance by directing new contributions to whichever ETF is underweight (no selling) | Rebalance by selling and buying (possible tax cost) | Backtest uses rebalance-with-contributions for contribution profiles, sell-and-buy for lump sum |
| **Fixed fees** | A flat $5/mo app fee is 6% a year on $1k | Rounding error | Fee sensitivity: flat fee vs. % fee, shown in the fee card |
| **Loss in dollars** | −35% = −$350 | −35% = −$17,500 | Drawdowns shown in dollars per profile; risk quiz asks about dollar losses |
| **Equal-weight sectors (A/B portfolio B)** | 9 ETFs × whole shares can't be built at $1k | Can be built | A/B results carry an "implementable from $__" note |

**Taxes and account type** (401k, IRA, brokerage) also differ by size, but they're **out of scope**; mention them in the limitations.

### Risk style: defensive, balanced or offensive
Size says *how much* money is invested. Risk style says *how much loss the person can live with*. These are separate: a $1k starter can be offensive, and a $50k lump-sum investor can be defensive. So the project crosses them into a **3 × 3 grid of 9 investor personas**.

Risk style doesn't hand out a fixed allocation. It sets the **limits** the Monte Carlo search must stay within, and the model then finds the best mix inside those limits:

| Style | Max 95th-pct drawdown | Bond (BND) range | Single stock allowed? | Typical person |
|---|---|---|---|---|
| **Defensive** | −15% | 40–60% | No | "A big drop would make me sell" or "I need this money soon" |
| **Balanced** | −25% | 20–40% | Up to 10% of stocks | "I can ride out a normal bear market" |
| **Offensive** | −40% | 0–20% | Up to 20% of stocks | "I won't touch it for years; drops are buying chances" |

**How a user gets a style:** a 3-question quiz (in Tableau as a parameter, in the web app as a real quiz):
1. "Your $__ drops to $__ in one month. What do you do?" (sell / wait / buy more). The amounts come from the user's size profile.
2. "When might you need this money?" (under 2 years / 2–5 years / 5+ years).
3. "Is your income stable?" (no / mostly / yes).

**Interaction worth testing:** a Starter's loss is small in dollars, and their monthly contributions buy cheaply after a drop. So an offensive style may "cost" a Starter much less than it costs a lump-sum investor. Compare the P(hit target) gain from switching defensive → offensive across the three size profiles.

### Do they want individual stocks?
Some beginners want to own a company they believe in, not just funds. The project treats this as an optional **"stock sleeve"**: a single stock (e.g. NVDA, AAPL or MSFT, via yfinance) making up 0%, 10% or 20% of the stock part of the portfolio, within the limits of the user's risk style.

This answers the brief's NVDA question for a beginner audience: **does adding a single stock raise the chance of hitting the target enough to justify the extra drawdown risk?**

**Hindsight bias is the big trap here.** Picking NVDA in 2026 *because* it went up is cheating; a 2008 investor didn't know that. To keep it honest:
- **Main test:** in each Monte Carlo path, the sleeve stock is **drawn at random from the 10 largest US companies at the start of the data window (Jan 2008)**. That list was knowable in 2008 and includes names that later lagged, such as GE and XOM. Look it up once from a published ranking and keep it as a Python list in the code (not a CSV). This models "a beginner picks a big famous company" without knowing the future.
- **Comparison only:** also show the NVDA-only result, clearly labeled "with hindsight."
- Expect the random-big-company sleeve to add drawdown risk without reliably adding return. That is a useful finding for beginners.

**Stock-picker test (for the "Pick 5 stocks" option):** draw thousands of random 5-stock portfolios from the 2008 top-20 list and report **what % of them beat SPY** over each 5-year window. This gives beginners a concrete answer to "can't I just pick a few winners?"

In the recommended mix, the stock slice is opt-in and off by default.

### Primary question
> A young first-time investor is defined by **level** (1–4), **size** (starter, builder or lump sum) and **risk style** (defensive, balanced or offensive), and targets x%/yr over 5 years. **How does each option (savings, bonds, ETFs, individual stocks) grow their money, and which one gives the highest probability of reaching the target within that style's drawdown limit?** Does the answer change with how much they start with, and what should their next step be at their level?

### Supporting questions (each maps to a dashboard)
1. **Options:** How would each option have grown this person's money, and what range of outcomes could it give over the next 5 years? Has QQQ beaten SPY consistently, and how often do 5 random stocks beat SPY? *(Dashboard 1)*
2. **Risk:** What's the 95th-percentile worst drawdown for tech-heavy mixes compared with balanced ones? *(Dashboard 2)*
3. **A/B:** Does a 60/40 stock/bond portfolio beat an equal-weight sector portfolio on a risk-adjusted basis? *(Dashboard 3)*

4. **Stock sleeve:** Does adding one individual stock (e.g. NVDA) improve the odds enough to justify the extra risk? *(Dashboard 2)*

---

## 2. Tickers and data sources

| Role | Tickers | Source |
|---|---|---|
| Core comparison | SPY, QQQ | yfinance (adjusted close, includes dividends) |
| Bonds (for 60/40) | BND (or AGG) | yfinance |
| Equal-weight sectors | XLK, XLF, XLV, XLE, XLI, XLY, XLP, XLU, XLB | yfinance |
| Individual stocks | 20 largest US companies in Jan 2008 (top 10 used for the sleeve), plus NVDA | yfinance |
| Market fear gauge (ML feature) | ^VIX | yfinance |
| Risk-free rate (for Sharpe) | 3-month Treasury yield | Alpha Vantage `TREASURY_YIELD` |
| Cross-check of prices | SPY, QQQ daily | Alpha Vantage `TIME_SERIES_DAILY` (spot-check only) |
| ETF facts (optional) | Expense ratio, AUM, sector weights | Financial Modeling Prep (free key), called directly with `requests` |
| Live trades (streaming) | SPY, QQQ, BND | Finnhub WebSocket (free key) |

**Things to know about the data:**
- **Use adjusted close.** Raw close leaves out dividends, which understates SPY and BND returns quite a bit.
- **Use a common date window.** BND starts in 2007. XLC (2018) and XLRE (2015) are excluded so the 9 original sector ETFs share a long history. Proposed window: **2008-01 to present**, which includes the 2008, 2020 and 2022 drawdowns. That's a good thing: the audience needs to see a bad year.
- **Alpha Vantage free tier allows about 25 requests/day.** Use it only for the Treasury yield and spot checks, cache the results in the database, and never call it inside a loop.
- **About Financial Modeling Prep (FMP):** Don't depend on the `thinh-vu/FinancialModelingPrep` wrapper. It was last updated in Oct 2023 and calls the older `/api/v3` and `/api/v4` endpoints, which FMP has been moving away from in favor of `/stable/`. Call the endpoints yourself in `src/extract/fmp.py` instead. The free tier gives limited price history, so FMP shouldn't be the main price source. Use it for ETF facts that beginners care about: **fees (expense ratio)** and **what's inside the fund** (sector weights). Confirm which endpoints the free key allows during W3.
- **Finnhub's free WebSocket** streams US trades only during market hours. See section 7f for how to demo it after hours. Confirm that ETF symbols stream on the free key during W3; fallbacks are Alpaca's free IEX stream or the `yfinance` WebSocket.
- **No CSVs:** every load goes API → pandas → database.

---

## 3. Architecture

```
 yfinance / Alpha Vantage / FMP              Finnhub WebSocket (live trades)
            │  batch ETL (daily)                         │
            ▼                                            ▼
  pandas transforms + models                    streamer service
  (Sharpe, Monte Carlo, A/B, ML)                         │
            │                                            │
            └──────────────►  PostgreSQL  ◄──────────────┘
                              (2NF schema)  ◄──── Tableau Desktop (live connection)
                                   │
                                   ▼
                     FastAPI backend: REST + WebSocket + AI assistant
                                   │
                                   ▼
                     Next.js web app (Planner · Compare · Live · Ask)
```

Everything runs in **Docker Compose** locally and deploys the same way to the cloud (section 7e).

**Why Postgres:** Tableau can't connect live to a pandas DataFrame, and using CSV/Hyper extracts would break the "no CSV" rule. Postgres gives Tableau Desktop a real **live connection**, gives the web app a shared backend, and meets the DBMS extra-credit item.

### Database schema (2nd normal form, extra credit)

**Main design idea:** treat every single ticker as a portfolio too ("SPY 100%"). Then backtests, rolling metrics and Monte Carlo all use one key (`portfolio_id`) instead of keeping separate ticker and portfolio versions.

| Table | Primary key | Columns |
|---|---|---|
| `tickers` | `ticker` | name, asset_class, inception_date, expense_ratio |
| `prices_daily` | (`ticker`, `date`) | adj_close, close, volume |
| `risk_free_daily` | `date` | rate |
| `portfolios` | `portfolio_id` | name, rebalance_freq, sleeve_pct, sleeve_rule (`none` / `random_top10_2008` / `random5_top20_2008` / `NVDA`), option_group (savings / bonds / etf / stocks / mix) |
| `portfolio_weights` | (`portfolio_id`, `ticker`) | weight |
| `backtest_values` | (`portfolio_id`, `size_id`, `date`) | value, contributed_to_date, drawdown |
| `rolling_metrics` | (`portfolio_id`, `date`) | ret_3y, vol_36m, sharpe_36m |
| `size_profiles` | `size_id` | name, start_amount, monthly_contribution, horizon_months, rebalance_method |
| `risk_styles` | `style_id` | name, max_drawdown, bond_min, bond_max, max_sleeve_pct |
| `levels` | `level_id` | name, description |
| `level_unlocks` | (`level_id`, `option_group`) | (key only: which option groups each level can see) |
| `pathway_steps` | (`level_id`, `step_no`) | title, body_text, view_name (which chart/view the step shows) |
| `mc_runs` | `run_id` | portfolio_id, size_id, n_paths, block_size, seed, created_at |
| `implementability` | (`portfolio_id`, `start_amount`) | max_weight_error, whole_shares_ok |
| `mc_summary` | `run_id` | median_terminal, p5_terminal, p95_drawdown |
| `mc_target_probs` | (`run_id`, `target_rate`) | p_hit |
| `mc_paths` | (`run_id`, `path_id`) | terminal_value, max_drawdown (1k-path sample for histograms) |
| `mc_fan` | (`run_id`, `month`) | p5, p25, p50, p75, p95 |
| `ab_tests` | `test_id` | portfolio_a, portfolio_b, window_start, window_end |
| `ab_results` | (`test_id`, `metric`) | estimate, ci_low, ci_high, p_value |
| `ml_models` | `model_version` | algorithm, features, train_end, rmse, baseline_rmse |
| `ml_predictions` | (`model_version`, `portfolio_id`, `date`) | predicted_vol, actual_vol |
| `live_ticks` | `tick_id` | ticker, ts, price, size |

**Why it's 2NF:** every non-key column depends on the *whole* key. For example, a ticker's name and expense ratio live in `tickers`, not repeated in `prices_daily` (that repetition would be a partial dependency on just `ticker`). Run settings live once in `mc_runs`, not repeated on all 10k path rows. Most tables are actually in 3NF; 2NF is the minimum. **Deliverables:** an ER diagram in `docs/`, plus `schema.sql` with foreign keys and constraints (e.g. weights for each portfolio sum to 1, checked in ETL).

**Tableau and the web app read from SQL views** (`v_portfolio_growth`, `v_mc_summary`, `v_ab_summary`, ...). The views join the normalized tables back into flat shapes, so the database stays normalized while dashboards stay easy to build.

**Risk style is a filter, not a separate simulation.** Monte Carlo runs once per (portfolio, size profile). A style then keeps only the portfolios that fit its bond range and sleeve limit and whose 95th-pct drawdown is within its maximum (a join between `risk_styles` and `mc_summary` in a view). Switching style in Tableau or the web app needs no rerun.

**Keeping Tableau fast:** the grid has 378 runs (section 4b). Storing all 10k paths for each would be about 3.8M rows, which is too slow for a live connection. Instead, Python saves:
- `mc_target_probs`: P(hit target) for every target rate from 4% to 12% in 0.5% steps (378 × 17 rows). The x% slider simply picks a row.
- `mc_paths`: a 1,000-path sample per run, for histograms only.

With monthly rate r = (1 + x)^(1/12) − 1 and n = 60 months, the target for each row is:
`target = start × (1 + r)^n + contribution × ((1 + r)^n − 1) / r`

### Repo layout
```
stock_proj/
├── docker-compose.yml        # db, etl, api, web, streamer
├── .env.example              # API keys + DB creds (never commit .env)
├── .github/workflows/        # CI tests, image build, scheduled ETL
├── db/
│   ├── schema.sql            # 2NF tables + constraints
│   └── views.sql             # flat views for Tableau and the API
├── src/
│   ├── extract/              # yfinance.py, alphavantage.py, fmp.py
│   ├── transform/            # returns.py, metrics.py
│   ├── model/                # sharpe.py, monte_carlo.py, ab_test.py
│   ├── ml/                   # features.py, train.py, evaluate.py
│   └── load/                 # db.py
├── api/                      # FastAPI: REST, WebSocket, AI assistant
├── streamer/                 # Finnhub WebSocket consumer + replay mode
├── web/                      # Next.js front-end
├── notebooks/                # EDA + model exploration
├── tableau/                  # .twb files (no extracts)
└── docs/                     # ER diagram, recommendation, screenshots
```

---

## 4. Statistical model (core, Weeks 3–6)

### 4a. Sharpe ratio
- Annualized excess return ÷ annualized volatility, using monthly returns and the Alpha Vantage 3-month T-bill rate.
- Compute for SPY, QQQ, every allocation in the grid, and both A/B portfolios.
- Add **rolling 36-month Sharpe** so the audience sees that Sharpe *changes over time* instead of treating it as one fixed number.

### 4b. Monte Carlo (10,000 paths)
- **Allocation grid (3 dimensions):**
  - QQQ share of stocks: 0, 20, 40, 60, 80, 100% (6 values)
  - Bonds (BND): 0–60% in steps of 10 (7 values)
  - Stock sleeve: none, 10% or 20% of stocks in a random top-10 company (3 values), plus the NVDA hindsight comparison on Dashboard 2 only
  - 6 × 7 × 3 = **126 portfolios × 3 size profiles = 378 runs** of 10k paths each. Vectorized NumPy handles this in minutes.
- **Random sleeve:** in each path, draw one stock from the 2008 top-10 list and keep it for that whole path.
- **Method: bootstrap historical monthly returns** (resample whole months jointly across tickers, so correlations are kept). Don't use a normal/GBM model; it understates crash risk. Use a **block bootstrap** (for example 6-month blocks) to keep some volatility clustering.
- **Horizon and profiles:** 60 months, run once per investor profile (start amount + monthly contribution). Contributions are added at the start of each month, before that month's return. Lump sum rebalances monthly by selling and buying; contribution profiles rebalance by directing new money to the underweight ETF. State these assumptions.
- **Outputs per allocation and profile:** median terminal value, P(hit x%), 5th-percentile terminal value, 95th-percentile worst max drawdown (% and $).
- **Contributions vs. allocation:** for the Starter profile, compare how much P(hit target) moves when going from 0% to 100% QQQ against how much it moves when going from $100 to $300/mo. This is likely the most useful finding for small investors.
- **Measuring drawdown with contributions:** new deposits hide losses in the account balance, so measure drawdown on a **time-weighted** basis (unit value), and report the dollar balance separately.
- **Best allocation for each persona:** for each of the 9 (size × style) personas, the portfolio with the highest P(hit x%) *among those the style allows*. Show the whole trade-off curve, not just the winner. If no allowed portfolio reaches a reasonable P(hit) (e.g. defensive with a 12% target), say so: "this target doesn't fit this risk style" is an important message for beginners.
- **Style × size test:** compare the P(hit target) gained by switching defensive → offensive across the three size profiles (section 1).
- **Sleeve test:** for each style, compare P(hit target) and 95th-pct drawdown with no sleeve against the 10% and 20% sleeves.
- **Sanity checks:** a seeded RNG for reproducibility, simulated mean ≈ historical mean, and P(hit target) falling as x rises.

### 4c. A/B test: 60/40 vs equal-weight sectors
- **A:** 60% SPY / 40% BND. **B:** equal weight across the 9 sector ETFs. Both rebalanced monthly.
- This is a **backtest comparison, not a randomized experiment**. Say so explicitly in the write-up.
- **Metric:** paired monthly return differences (B − A) over the same months.
- **Tests:**
  - Paired t-test on the mean monthly difference (H₀: mean diff = 0).
  - **Bootstrap CI** for the difference in **Sharpe ratios** (10k resamples, block bootstrap). This is the more honest test, because returns are fat-tailed and autocorrelated.
- **Report:** effect size in plain dollars ("B would have ended $X higher/lower on $50k"), the CI, and the p-value. Expect results that aren't significant, and present that clearly ("we can't tell them apart on ~18 years of data" is still a valid finding).

---

## 5. Dashboards (Tableau, core)

| # | Dashboard | Key views | Beginner-friendly touch |
|---|---|---|---|
| 1 | **Your money, your options** (growth explorer, section 5a) | Growth chart: past 5 years + 5-year projection for each option; range-of-outcomes chart; options map; rolling 3-yr QQQ vs SPY; % of random 5-stock portfolios that beat SPY; fee and sector-mix card (FMP) | Size, risk-style and x% selectors; toggle options on and off; hover: "Your $__ would be $__" |
| 2 | **Risk & target planner** | Monte Carlo fan chart, terminal-value histogram with target line, P(hit x%) vs drawdown scatter (allowed portfolios highlighted, the rest greyed out), 3 × 3 persona grid of best allocations, "contributions vs. allocation" chart, stock-sleeve comparison (random big company vs NVDA-with-hindsight), implementability flag, ML volatility forecast | **Size selector, risk-style selector (or quiz), x% slider**; losses shown in dollars for the chosen size |
| 3 | **A/B performance** | Cumulative value A vs B, monthly-difference distribution, Sharpe comparison with bootstrap CI, results summary card | Plain-English verdict text driven by the CI |

### 5a. Growth and options visualization (the centerpiece)
This is the view a beginner will remember, so it opens Dashboard 1 and the web app. It has three linked charts, all driven by the user's size, risk style and x% target:

**1. "Your money over time" (main chart)**
- One line per option (savings, bonds, 60/40, SPY, QQQ, one stock, 5 stocks, best mix for you), each in its own color.
- **Two panels side by side, sharing the same y-axis:**
  - **"If you'd started 5 years ago":** real backtest data with the user's own start amount and contributions.
  - **"If you start today":** the next 5 years from the same start amount. A median line for each option, with a shaded 25th–75th percentile band for the option the user clicks on (one band at a time keeps it readable).
  - Two panels work better than one continuous chart, because both start from the user's amount. Joined together, the projection would have to start from the backtest's ending value, which is confusing.
- **Two reference lines:** a grey "money you put in" line (deposits only, no growth), so beginners can see what growth actually added, and a dashed **target line** at x%.
- Toggle options on and off; hover shows "Your $__ would be $__ (+__%)."

**2. "Range of outcomes" (one row per option)**
- A horizontal bar from the 5th to the 95th percentile of the 5-year result, with a dot at the median and a vertical target line.
- It shows at a glance that savings is a short, safe bar below the target, while one stock is a very wide bar. The width *is* the risk.

**3. "Options map"**
- A scatter with bad-case loss in dollars (x-axis) against P(hit target) (y-axis), one dot per option.
- The area the user's risk style allows is shaded, so they see which options fit them.

**Tableau:** the two panels are two sheets (`backtest_values` and `mc_fan`) placed side by side, with the y-axis range fixed so they match. The range bars are Gantt bars, and the selectors are parameters.

**Web app (extra credit):** the same three charts in Plotly or Recharts, plus a **play button** that grows the lines month by month. Users drag the start-amount and contribution sliders and watch every option recompute live via the on-demand Monte Carlo endpoint. The animation also makes a strong opening for the demo video.

---

## 6. Ground rule for extra credit

**Course dates come first:** the model and A/B test must be done by the **mid pitch (W6)**, the ETL/API by **W9**, and all 3 Tableau dashboards by **W10**. Extras fill the time around those dates but never push them back. Each extra should build on the core story, not stand on its own, and each has a smaller fallback version (✂️) so it can be cut down rather than dropped if time runs short.

Priority order (cheapest and most valuable first):

| # | Extra | Cost | Why this order |
|---|---|---|---|
| 1 | DBMS in 2NF | Low | You're designing the schema in W3 anyway |
| 2 | Docker | Low | Compose already exists for Postgres |
| 3 | Custom ML model | Medium | Uses the same returns data as the core model |
| 4 | Web front-end (+ API) | High | AI and streaming both need it |
| 5 | AI integration | Medium | One API endpoint and a chat page |
| 6 | Data streaming / WebSockets | Medium | Needs the web front-end; only live during market hours |
| 7 | Cloud deployment | Medium | Last, because it deploys everything above |

---

## 7. Extra-credit designs

### 7a. DBMS in 2nd normal form
See the schema in section 3. Deliverables: `db/schema.sql`, `db/views.sql`, an ER diagram, and a short paragraph in the README explaining 2NF using a concrete example from your own tables.

### 7b. Custom ML model: next-month volatility forecast
- **What it predicts:** next-month realized volatility for each portfolio, shown as a "risk forecast" on Dashboard 2 and in the web app.
- **Why volatility, not returns:** monthly returns are close to unpredictable, so a return model will almost certainly lose to "predict the average." Volatility is persistent, so a well-built model has a real chance of beating the baseline. That makes the result honest and defensible.
- **Features:** lagged realized volatility (1, 3, 6, 12 months), VIX level and change, current drawdown, T-bill rate and its change, SPY–QQQ return spread.
- **Models:**
  - Baselines: trailing volatility, and GARCH(1,1) via the `arch` library.
  - Main model: gradient boosting (LightGBM or XGBoost).
  - Deep-learning stretch: a small LSTM in PyTorch on the same features.
- **Evaluation:** walk-forward (expanding window, retrain yearly; never shuffle time series). Report RMSE against the baselines. Losing to GARCH is a valid result if you report it.
- **Tie-in (stretch):** a regime-aware Monte Carlo that resamples mostly from historical months whose volatility matches the forecast.
- ✂️ **Fallback:** gradient boosting vs. trailing-volatility baseline only.

### 7c. Web front-end
- **Stack:** Next.js (React + TypeScript), Tailwind + shadcn/ui, Recharts or Plotly for charts, FastAPI backend that reads the SQL views.
- **Pages:**
  - **Start (onboarding):** the four questions from section 1 (level, size, risk style, goal) as a short step-by-step quiz of about 8 taps. The answers are kept in the URL, so a persona can be shared or bookmarked (no personal data stored).
  - **Your pathway (home page):** a vertical stepper showing the user's level's steps from `pathway_steps`. Each step has a short plain-English explanation and the matching mini chart from the API, using their numbers. Completed steps get checked off, with a "level up" button when they're ready for the next level. A Level 1 user with high-interest debt sees the "pay this off first" step before any investing.
  - **Planner:** start-amount and monthly-contribution inputs, target-return slider, the 3-question risk-style quiz from section 1 (in dollar terms), an "add an individual stock?" toggle, a suggested allocation (with a fractional-shares warning when needed), and the Monte Carlo fan chart. Custom amounts call a small on-demand Monte Carlo endpoint in the API (1k paths, fast enough to run live).
  - **Explore:** the growth and options visualization from section 5a, with the play animation and live sliders.
  - **Live:** streaming value of the user's chosen $50k portfolio (7f).
  - **Ask:** the AI assistant (7d).
- **Tableau note:** with a student Tableau Desktop license you can't publish to Tableau Server/Cloud, and Tableau Public doesn't support live database connections. So the web app draws its own charts from the API, and Tableau remains the analyst-facing deliverable. Optionally, link to a static Tableau Public version for viewers without Tableau.
- ✂️ **Fallback:** Explore and Planner pages only.

### 7d. AI integration: "Explain my plan" assistant
- A chat page where a beginner asks questions like *"Why is the 70/30 mix riskier?"* or *"What does a −35% drawdown mean in dollars?"*
- **Claude API with tool use:** the model calls tools backed by your database (`get_portfolio_stats`, `get_mc_result(allocation, target)`, `get_ab_result`), so **every number it states comes from your analysis**, not from the model's memory.
- **Guardrails:** a system prompt for a plain-English, beginner-level tone; no buy/sell advice on individual securities; a disclaimer on every answer.
- **Evaluation:** a list of about 20 test questions, plus an automatic check that the numbers in each answer match the database.
- **Cost:** use Claude Haiku (`claude-haiku-5-5`); a demo costs a few dollars at most. **Check with your instructor** whether a paid LLM API is allowed under "free APIs only." That rule seems to cover data sources, but confirm. The free fallback is a local model via Ollama.
- ✂️ **Fallback:** a single "explain this result" button instead of a full chat.

### 7e. Docker and cloud deployment
- **Compose services:** `db` (Postgres), `etl` (scheduled batch job), `api` (FastAPI), `web` (Next.js), `streamer`.
- **Cloud:**
  - Managed Postgres on a free tier (Neon or Supabase).
  - `api`, `web` and `streamer` containers on Render, Fly.io or Railway.
  - The daily ETL as a scheduled GitHub Actions workflow.
  - Tableau Desktop can live-connect to the cloud Postgres too.
- **CI:** GitHub Actions runs pytest (transforms, Monte Carlo sanity checks, schema constraints) and builds the images on each push.
- **Secrets:** stored as environment variables on the host and as GitHub Actions secrets; never in the repo.
- ✂️ **Fallback:** a fully working `docker compose up` locally, with only `api` and `web` deployed.

### 7f. Data streaming / WebSockets
- **Flow:** the `streamer` service subscribes to Finnhub's WebSocket (SPY, QQQ, BND) → writes ticks to `live_ticks` in batches → FastAPI pushes updates to the browser over its own WebSocket → the Live page shows the user's $50k portfolio value updating tick by tick.
- **Replay mode:** markets are closed evenings and weekends, so the streamer can replay a recorded trading day from `live_ticks` at 10× speed. The demo works at any time; clearly label replayed data as "replay."
- **Tableau tie-in:** a small live-connection sheet on `live_ticks` that updates on refresh.
- ✂️ **Fallback:** live ticks on the web page only (no database writes).

---

## 8. Timeline

### W1–3: Question, extractors, EDA (finishing now)
Exit checklist before moving on:
- [ ] Problem statement and x% definition locked in (section 1)
- [ ] `extract/` pulls all tickers and the T-bill rate; Alpha Vantage calls are cached
- [ ] EDA notebook: return distributions, correlations (SPY–QQQ is ~0.9, which matters for diversification), missing-data check, drawdown history

### W3–6: Model and A/B test (core, plus the cheap extras)
| Week | Core | Extra credit | Done when |
|---|---|---|---|
| **W3** | Monthly returns; backtest engine (weights → value series with monthly rebalancing); static Sharpe; savings (T-bill) series and the "money you put in" line | **2NF schema + views + ER diagram; Docker Compose (db, etl)**; check that the Finnhub and FMP free keys work | `docker compose up` loads every table from the APIs |
| **W4** | Monte Carlo: block bootstrap with contributions and stock sleeve, 126 portfolios × 3 size profiles × 10k paths; risk-style filter view; implementability check | ML: feature table + trailing-volatility and GARCH baselines | `mc_runs`, `mc_paths`, `mc_fan` and `implementability` loaded; sanity checks pass (0 contributions reproduces the lump-sum math) |
| **W5** | A/B test: paired t-test + bootstrap Sharpe-difference CI; robustness window | ML: gradient boosting with walk-forward evaluation | `ab_results` and `ml_predictions` loaded |
| **W6** | Mid-pitch prep (below); first-pass recommendation numbers | ML: finish walk-forward comparison against baselines | **Model and A/B test finished**; pitch deck ready |

### Mid pitch (end of W6)
Dashboards aren't due until W9–10, so pitch with notebook charts and keep it to about 5 slides:
1. **Problem:** the target audience, the four ways it differs (level, size, risk style, goal), and the three personas (Jordan, Priya, Sam), including why $1k ≠ $50k.
2. **Data and pipeline:** APIs → pandas → Postgres (2NF) in Docker, with a diagram of what already runs.
3. **First results:** a Monte Carlo fan chart and P(hit 8%) by allocation for one profile, plus the A/B test result with its confidence interval.
4. **Early finding:** contributions vs. allocation for the Starter profile.
5. **Plan for the rest of the term:** ETL/API, dashboards, extras (ML, web app, AI, streaming, cloud).

Ask for feedback on the personas, the drawdown limits for each risk style, and the stock-sleeve idea. Also ask your instructor whether a paid AI API is allowed (section 7d).

### W6–9: ETL and API (course phase, plus most extras)
Most of the ETL already exists from W3, because the model needed it. This phase makes it production-quality and builds the API layer on top.

| Week | Core | Extra credit | Done when |
|---|---|---|---|
| **W7** | **Harden ETL:** idempotent upserts (reruns never duplicate rows), data validation (row counts, gaps, weights sum to 1), logging, retry/backoff, pytest | **FastAPI:** REST endpoints over the views + an on-demand Monte Carlo endpoint; CI on GitHub Actions | Rerunning the ETL changes nothing; API returns results for every profile |
| **W8** | Scheduled daily ETL (GitHub Actions) that refreshes prices and reruns the models | **Streaming:** streamer service + WebSocket endpoint + replay mode. **AI:** assistant endpoint with tools + 20-question evaluation set | Live ticks reach the API; AI evaluation passes the number checks |
| **W9** | Tableau live connection to the final schema; start Dashboard 1 | **Cloud:** deploy db, api, etl and streamer | Public API URL; Tableau connects to the cloud database |

### W9–10: Tableau dashboards (core)
| Week | Work | Done when |
|---|---|---|
| **W9** | Dashboard 1 (Returns comparison) | Profile selector and growth-of-money views work |
| **W10** | Dashboard 2 (Risk & target planner) + Dashboard 3 (A/B performance); recommendation draft | **All 3 dashboards working on the live connection** |

### W10–13: Polish, presentation, demo video
| Week | Work |
|---|---|
| **W11** | **Web front-end:** Next.js onboarding, Your pathway and Explore (growth visualization) pages, using the API |
| **W12** | Web front-end: Planner, Live and Ask pages; deploy the web app; polish the dashboards (consistent colors, tooltips, beginner wording) |
| **W13** | Final recommendation, presentation, **demo video**, README, fresh-clone test (`docker compose up` from a clean machine) |

**Demo video tip:** record the Live page during market hours (9:30–4:00 ET, weekdays) so it shows real ticks. Use replay mode only as a backup, and label it as replay if you do.

If you fall behind, keep the course dates fixed and switch the extras to their ✂️ fallbacks, starting from the bottom of the priority table in section 6.

---

## 9. Business recommendation (template)

Tell it through the **three personas** (Jordan, Priya, Sam): one pathway each, in plain language. Open with the **growth and options chart** for Jordan, so the audience sees savings vs bonds vs ETFs vs stock picking before any numbers. Then show the **3 × 3 persona grid** (best allocation and P(hit 8%) in each cell), then the detail below:

| | Defensive | Balanced | Offensive |
|---|---|---|---|
| **Starter** ($1k + $200/mo) | __ / __% | __ / __% | __ / __% |
| **Builder** ($10k + $500/mo) | __ / __% | __ / __% | __ / __% |
| **Lump sum** ($50k) | __ / __% | __ / __% | __ / __% |

Then one recommendation per size profile, plus the style and sleeve findings:

> **Lump sum ($50k, 5 years, 8% target → $73,466):** an allocation of **__% QQQ / __% SPY (/ __% BND)** gives a **__%** chance of reaching the target, with a 95th-percentile drawdown of **__% (−$__)**. Going more tech-heavy raises the median outcome by $__ but deepens the bad-case drawdown to __%.
>
> **Starter ($1k + $200/mo):** allocation changes move P(hit target) by only __ points, while raising contributions from $100 to $300/mo moves it by __ points. **For small investors, savings rate matters more than ETF choice.** Use a broker with fractional shares, or start with a single fund (__) until the balance reaches $__.
>
> **A/B:** 60/40 vs equal-weight sectors showed [no significant / a significant] difference in risk-adjusted return (Sharpe diff __, 95% CI [__, __]). The sector portfolio can only be built with whole shares from about $__.
>
> **Risk style:** going from defensive to offensive raises P(hit target) by __ points for a Starter but by __ points for a lump-sum investor, because [contributions buy cheaply after drops / ...].
>
> **Individual stocks:** a 10% sleeve in a randomly chosen big company changed P(hit target) by __ points and the 95th-pct drawdown by __ points. NVDA *with hindsight* looks like +__ points, but a 2008 investor couldn't have known to pick it. **Recommendation:** [ETFs only / at most __% in one stock, and only for offensive investors].
>
> **Options vs. savings:** over 5 years, savings/T-bills reached the 8% target in __% of paths vs __% for the recommended mix. Only __% of random 5-stock portfolios beat SPY.

Always include the limits: past returns ≠ future returns, the analysis uses a single historical regime (strong US tech), and it ignores taxes and fees. The project is **educational and not financial advice**. This applies to the AI assistant's answers too.

---

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Extra credit eats into core time | Course dates (W6 pitch, W9 ETL/API, W10 dashboards) are fixed (section 6); extras have ✂️ fallbacks |
| Dashboards come late in the term (W9–10) | Use views that are ready from W3; test the Tableau ↔ Postgres connection early |
| Alpha Vantage rate limit (25/day) | Cache in the database; use only for the T-bill rate and spot checks |
| FMP free-tier limits or endpoints moving behind the paywall | Optional source only; nothing in the model depends on it |
| yfinance outages or schema changes | Pin the version; add retry and backoff; validate row counts after each pull |
| Survivorship/regime bias (QQQ's 2010s run) | Robustness windows; bootstrap rather than projecting the trend |
| Monte Carlo looks too precise | Show fan charts and ranges, never a single number |
| ML model doesn't beat the baseline | Expected for returns, which is why we forecast volatility; report honestly either way |
| AI assistant invents numbers | Answers use only tool results; automatic number-check evaluation set |
| LLM API cost / "free APIs" rule | Haiku + instructor check; Ollama fallback |
| Live stream is empty outside market hours | Replay mode |
| Free cloud tiers sleep (slow cold starts) | Wake the app before the demo; keep a local `docker compose` backup |
| Tableau live connection issues on Mac | Test the Postgres driver in W3, not W9 |
| Hindsight bias in stock picking | Random draws from the 2008 top-10/top-20 lists; NVDA shown only as a labeled hindsight comparison |
| Grid too big for Tableau | Precomputed P(hit) per target rate + 1k-path samples (section 3) |
| Scope creep | Extra ETFs and more sleeve stocks are stretch goals only, after everything above |
