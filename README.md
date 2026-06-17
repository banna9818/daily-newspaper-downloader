# Daily Gujarat Samachar Newspaper Downloader

Automatically download the daily Gujarat Samachar Rajkot-Saurashtra newspaper and upload it to a Telegram channel using GitHub Actions.

## ✨ Features

✅ **Automatic Daily Download** - Runs every day at 5:00 AM IST via GitHub Actions scheduler
✅ **Dynamic Content Handling** - Uses Playwright to handle JavaScript-rendered content
✅ **Image Collection** - Detects and collects all newspaper pages in correct order
✅ **PDF Merging** - Combines all pages into a single high-quality PDF
✅ **Telegram Integration** - Automatically uploads PDF to your Telegram channel
✅ **Error Handling** - Comprehensive error handling with automatic failure notifications
✅ **Logging** - Detailed logs for debugging and monitoring
✅ **Asia/Kolkata Timezone** - Correctly handles India Standard Time

## 📁 Project Structure

```
newspaper-downloader/
├── .github/
│   └── workflows/
│       └── daily.yml                 # GitHub Actions workflow
├── main.py                           # Main Python script
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 🚀 Setup Instructions

### 1. Configure Telegram Bot

1. Create a bot using [@BotFather](https://t.me/botfather) on Telegram
2. Get your **BOT_TOKEN** from BotFather
3. Create a private Telegram channel for the newspaper
4. Add the bot to your channel as administrator
5. Get your **CHANNEL_USERNAME** (format: `-100123456789` for private channels or `@channelname` for public)

### 2. Set GitHub Secrets

Go to your repository settings and add these secrets:

**Steps:**
1. Go to `Settings` → `Secrets and variables` → `Actions`
2. Click `New repository secret`
3. Add `BOT_TOKEN` with your bot token
4. Add `CHANNEL_USERNAME` with your channel username/ID

### 3. Install Dependencies (Local Testing)

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Run Locally (Optional)

```bash
export BOT_TOKEN="your_bot_token"
export CHANNEL_USERNAME="your_channel_id"
python main.py
```

## ⚙️ How It Works

### 1. Daily Scheduling
The workflow runs automatically via cron scheduler:
- **Time**: 5:00 AM IST (11:30 PM UTC previous day)
- **Trigger**: `30 23 * * *` in UTC

### 2. Newspaper Download Process

```
1. Get today's date in Asia/Kolkata timezone
2. Construct URL: https://sandesh-pages.vercel.app/gujarat-samachar/rajkot-saurashtra?date=YYYY-MM-DD
3. Fetch webpage (with Playwright for dynamic content)
4. Extract all image URLs from the page
5. Download each image in order
6. Validate all images
```

### 3. PDF Creation
- Converts all images to RGB format
- Merges them into a single PDF
- Filename: `Gujarat_Samachar_Rajkot_YYYY-MM-DD.pdf`
- Quality: 95 (high quality)

### 4. Telegram Upload
- Sends PDF with formatted caption in Gujarati
- Format includes date and channel branding
- Automatic retry on failure

### 5. Error Handling
- Network failures are retried up to 3 times
- Missing pages are logged and reported
- Failure notifications sent to Telegram
- Logs uploaded as artifacts for debugging

## 📱 Telegram Caption Format

The PDF is uploaded with this caption:

```
📰 ગુજરાત સમાચાર - રાજકોટ સૌરાષ્ટ્ર

📅 DD-MM-YYYY

📖 આજનું સંપૂર્ણ અખબાર PDF સ્વરૂપે

━━━━━━━━━━━━━━

🔥 KHAKHI NI KHUMARI 🔥

━━━━━━━━━━━━━━
```

## 🔧 Troubleshooting

### Issue: Workflow fails with "Newspaper not available"

**Cause**: The website might not have published the newspaper for that date yet.

**Solution**: 
- Check if the newspaper is available manually at the URL
- Adjust the cron schedule to run later in the morning
- Current: `30 23 * * *` (11:30 PM UTC)
- Try: `10 0 * * *` (12:10 AM UTC = 5:40 AM IST)

### Issue: "Failed to download image" errors

**Cause**: Image URLs might have changed or the website structure changed.

**Solution**:
1. Run workflow manually to see detailed logs
2. Check the artifact logs in GitHub Actions
3. Visit the website to verify the current structure
4. Update the image extraction patterns in `main.py`

### Issue: PDF is empty or has missing pages

**Cause**: Some images failed to download or weren't recognized.

**Solution**:
1. Check the logs for which pages failed
2. Verify network connectivity in GitHub Actions
3. Increase retry attempts in the code
4. Check if image URLs are accessible from GitHub Actions

### Issue: Telegram upload fails

**Cause**: Invalid bot token or channel ID, or file too large.

**Solution**:
1. Verify `BOT_TOKEN` and `CHANNEL_USERNAME` in GitHub Secrets
2. Ensure the bot has admin rights in the channel
3. Check if the PDF file size is reasonable (usually < 50MB)
4. Test the Telegram bot with a simple message:
   ```bash
   curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/sendMessage" \
     -d "chat_id=<CHANNEL_ID>&text=Test"
   ```

### Issue: Workflow doesn't run at scheduled time

**Cause**: GitHub Actions scheduler might be delayed or the repository needs to have commits on the default branch.

**Solution**:
1. Make sure the repository has at least one commit
2. Ensure the workflow file is in the default branch
3. Check GitHub Actions status page
4. Manually trigger workflow using `workflow_dispatch`
5. Note: Scheduled workflows don't run on forks unless explicitly enabled

## 📊 Monitoring

### View Workflow Runs
1. Go to your repository
2. Click `Actions` tab
3. Select `Daily Gujarat Samachar Download`
4. View run details and logs

### Download Error Logs
1. If workflow fails, artifacts are uploaded
2. Go to workflow run details
3. Scroll down to `Artifacts` section
4. Download `error-logs`

### Manual Trigger
```bash
# Using GitHub CLI
gh workflow run daily.yml

# Or via Actions tab in GitHub UI
```

## 🐍 Python Version

- **Minimum**: Python 3.11
- **Tested**: Python 3.11+
- **GitHub Actions**: Uses `ubuntu-latest` with Python 3.11

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| requests | 2.31.0 | HTTP requests |
| beautifulsoup4 | 4.12.2 | HTML parsing |
| Pillow | 10.0.0 | Image processing |
| playwright | 1.40.0 | Browser automation |
| pytz | 2023.3 | Timezone handling |
| aiohttp | 3.9.1 | Async HTTP |
| python-dotenv | 1.0.0 | Environment variables |

## 📜 License

This project is provided as-is for personal use.

---

**Last Updated**: 2026-06-17
**Author**: Banna9818
