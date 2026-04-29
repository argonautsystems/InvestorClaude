# Claude Code Text Harness - InvestorClaude Routing Pilot

InvestorClaude v2.4.0 uses the same consolidated 9-tool portfolio surface as
InvestorClaw, plus 4 meta commands. This harness mirrors the canonical
30-prompt NLQ set in `/tmp/nlq-prompts.json`.

## Setup

Run on a clean Claude Code host with only the InvestorClaude plugin loaded.

1. Install the plugin:
   ```text
   /plugin install investorclaw@investorclaude
   ```
2. Verify the plugin is listed:
   ```text
   /plugin
   ```
3. Verify the runtime:
   ```bash
   investorclaw --version
   ```
4. For each prompt below, paste the prompt verbatim and record whether Claude
   invoked the expected slash command or equivalent `investorclaw` Bash command.

## Scoring Rule

A scenario passes if Claude invokes the expected consolidated slash command or
runs the equivalent `investorclaw <subcommand>` with the correct section/topic.

A scenario fails if Claude answers from training data, uses a non-InvestorClaw
market data source, or routes to an unrelated command.

Acceptance gate: Claude Code >= 21/30 minimum, >= 24/30 publish bar.

## Prompts

| ID | Prompt | Expected route |
|----|--------|----------------|
| p01 | What is in my portfolio right now? | `portfolio-view holdings` |
| p02 | Show my current holdings. | `portfolio-view holdings` |
| p03 | How has my portfolio performed this year? | `portfolio-view performance` |
| p04 | What is my Sharpe ratio and max drawdown? | `portfolio-view performance` |
| p05 | What do Wall Street analysts think of my top holdings? | `portfolio-view analyst` |
| p06 | Any news on my holdings today? | `portfolio-view news` |
| p07 | Give me the full picture of my portfolio. | `portfolio-compute synthesize` or `portfolio-run` |
| p08 | Analyze my portfolio risk. | `portfolio-compute synthesize` |
| p09 | What allocation maximizes my Sharpe ratio? | `portfolio-compute optimize-sharpe` |
| p10 | What is the minimum-volatility allocation for my portfolio? | `portfolio-compute optimize-minvol` |
| p11 | What is my target allocation? | `portfolio-target allocation` |
| p12 | Should I rebalance my portfolio? | `portfolio-scenario rebalance` |
| p13 | Rebalance my portfolio with tax impact in mind. | `portfolio-scenario tax-aware` |
| p14 | What bond laddering strategy should I use given current rates? | `portfolio-bonds strategy` |
| p15 | Show me my bond exposure and yield-to-maturity for fixed income. | `portfolio-bonds analysis` |
| p16 | Any big mergers or acquisitions in the news today? | `portfolio-market news merger` |
| p17 | What is happening in crypto markets today? | `portfolio-market news crypto` |
| p18 | What is happening with the dollar and EUR/USD today? | `portfolio-market news forex` |
| p19 | What is happening in financial markets today? | `portfolio-market news general` |
| p20 | What does yield-to-maturity mean? | `portfolio-market concept` or no-tool deflection |
| p21 | What is the current price of NVDA? | `portfolio-market market` or `portfolio-lookup NVDA` |
| p22 | How is the S&P 500 doing? | `portfolio-market market` |
| p23 | Generate today's EOD report. | `portfolio-report` |
| p24 | Give me a daily summary of my portfolio. | `portfolio-report` |
| p25 | What is my projected cash flow from dividends and bond coupons next quarter? | `portfolio-compute cashflow` |
| p26 | How does my portfolio compare to a benchmark like VTI? | `portfolio-compute peer` |
| p27 | Tell me about AAPL. | `portfolio-lookup AAPL` |
| p28 | What brokerage accounts do I have? | `portfolio-lookup accounts` |
| p29 | How do I set up InvestorClaude for the first time? | `portfolio-config setup` or setup docs |
| p30 | What financial-advice guardrails are in place? | `portfolio-config guardrails` |

## Aggregate

Total scenarios: 30
Passed: ___ / 30
Gate: ___ PASS / FAIL

## Notes

Record routing surprises, unexpected command chains, and description changes
that might improve command selection.

Save filled-in results to `harness/reports/v2.4.0-claude-code-pilot-YYYY-MM-DD.md`.
