## Important Disclaimer

**InvestorClaw is an educational analysis tool.** It is NOT financial advice and NOT provided by a fiduciary advisor. 

**Before acting on any recommendation:**
- Discuss these findings with your qualified financial advisor
- Verify all data and calculations align with your actual holdings
- Consider your full financial situation, not just this portfolio

*No action should be taken based solely on InvestorClaw analysis.*

## Provider Data Flows

- Prompts are sent to Together AI by default for narrative generation.
- Consult-role prompts may optionally be sent to Google AI Studio or to a local
  llama.cpp server when configured by the user.
- Market data requests flow through NewsAPI, Finnhub, Alpha Vantage, FRED, and
  Polygon-via-Massive only when the user supplies the corresponding API keys.
- Portfolio CSV data stays local except when the user's request includes that
  data in a prompt sent to the configured narrative provider.
