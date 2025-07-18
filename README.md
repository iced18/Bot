# Discord Investment Bot

## 🔧 Setup

1. Add a `.env` file with:
```
DISCORD_TOKEN=your_discord_token
SUMMARY_CHANNEL_ID=your_channel_id
```

2. Deploy to [Render](https://render.com):
- Create a **Background Worker**
- Use `render.yaml` for deploy setup
- Set required environment variables

3. Commands you can use:
- !ping
- !price BTC
- !summary
- !breakout
- !plan ETH
- !sentiment NVDA
- !uptime

✅ Bot sends daily breakout summaries at 8:30 AM (UTC).