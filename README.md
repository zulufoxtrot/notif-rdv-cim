# RDV CIM Notification Bot

Automated medical appointment availability monitor that checks for available appointments every 15 minutes and sends Telegram notifications when appointments before a specified date become available.

## Features

- 🔄 **Automatic Monitoring**: Checks appointment availability every 15 minutes
- 📱 **Telegram Notifications**: Instant notifications via Telegram when appointments are available
- 🐳 **Docker Support**: Easy deployment using Docker and Docker Compose
- 🚀 **CI/CD**: Automated Docker image builds with GitHub Actions

## Prerequisites

- Docker and Docker Compose installed
- A Telegram bot token (create one via [@BotFather](https://t.me/botfather))
- Your Telegram chat ID

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/notif-rdv-cim.git
   cd notif-rdv-cim
   ```

2. **Create a `.env` file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` and add your Telegram bot token**:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=8556080794
   ```

4. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

5. **Check logs**:
   ```bash
   docker-compose logs -f
   ```

## Using the Pre-built Docker Image from GHCR

Instead of building locally, you can use the pre-built image:

```yaml
version: '3.8'

services:
  rdv-monitor:
    image: ghcr.io/YOUR_USERNAME/notif-rdv-cim:latest
    container_name: rdv-cim-monitor
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=8556080794
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (required)
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID (default: 8556080794)

### Customization

To change the check interval or limit date, edit `main.py`:

```python
CHECK_INTERVAL = 15 * 60  # 15 minutes in seconds
LIMIT_DATE = datetime(2026, 2, 4)  # Target date
```

## Development

### Local Development

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   ```bash
   export TELEGRAM_BOT_TOKEN=your_token_here
   export TELEGRAM_CHAT_ID=8556080794
   ```

4. **Run the script**:
   ```bash
   python main.py
   ```

## How It Works

1. The script fetches appointment data from the medical portal API
2. It checks if there are available appointments (`firstSchedule` field)
3. If the first available date is before the limit date (2026-02-04), it sends a Telegram notification
4. The process repeats every 15 minutes

## GitHub Actions

The repository includes a GitHub Actions workflow that automatically:
- Builds the Docker image on every push to `main`
- Pushes the image to GitHub Container Registry (GHCR)
- Tags images appropriately (latest, version tags, etc.)

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
