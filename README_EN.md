<div align="center">
<h1>ChiiBot</h1>
<i>An elegant Telegram PM bot for smarter message management and forwarding.</i>
</div>

EN | <a href="https://github.com/ImYrS/ChiiBot/blob/main/README.md">中文</a>

> [!WARNING]  
> This project is still in a rapid iteration stage and may have bugs or instability issues.
> Breaking changes can occur at any time.

## ✨ Features

- **Forum-Topic in Group**
  > ChiiBot will assign a unique topic for each guest who messages it, allowing for easy reply to different guests.

- **Reply or Not**
  > You can reply to the original message or not.
  > Bot will also perform corresponding reply mapping when forwarding your messages.

- **Blacklist**
  > You can block or unblock users if you don't want to receive their messages.

- **Reaction Feedback**
  > ChiiBot uses reactions to indicate successful forwarding,
  > rather than cumbersome message prompts or no prompt at all.

- **Easy and Simple**
  > No public IP required, can be deployed with proxy, set a Bot Token to start, multi-language supported.

## 🚀 Start to Use

### Preparations

1. Create a bot using [@BotFather](https://t.me/botfather) and get the bot's token.
2. **Create a new group**, add your bot to the group, and **make it an admin**.
3. **Set the group to Forum Mode**.
    - Open the group settings, turn on the "Topic" option.
    - Now your group is in Forum Mode.

### Deploy Bot

#### Docker

> We assume you have Docker installed and running.

1. Prepare a dir for storing the bot's database.
   ```bash
   mkdir -p /path/to/ChiiBotData
   ```
2. Run the bot using Docker.  
   Replace the `{YOUR_BOT_TOKEN}` with your bot's token.
   ```bash
   docker run -d \
     --name ChiiBot \
     -v /path/to/ChiiBotData:/app/data \
     -e CORE_BOT_TOKEN={YOUR_BOT_TOKEN} \
     imyrs/chii-bot:latest
   ```

#### non-Docker

> Not yet written...

### Final Step

Just send `/chii_setup` in your Telegram group created in the previous step.
You should see a success message from the bot.

> ChiiBot will save the group ID and admin ID (you) in the database.

### Done!

Just try to send a message to the bot via another Telegram account.

## How to Update

### Docker

```bash
docker pull imyrs/chii-bot:latest
docker stop ChiiBot
docker rm ChiiBot
docker run -d \
  --name ChiiBot \
  -v /path/to/ChiiBotData:/app/data \
  -e CORE_BOT_TOKEN={YOUR_BOT_TOKEN} \
  imyrs/chii-bot:latest
```

## Q&A

1. How to use proxy?  
   You can add this `-e CORE_PROXY={YOUR_PROXY_URL}` when running Docker. Example:
    ```bash
    docker run -d \
      --name ChiiBot \
      -v /path/to/ChiiBotData:/app/data \
      -e CORE_BOT_TOKEN={YOUR_BOT_TOKEN} \
      -e CORE_PROXY=http://127.0.0.1:6969 \
      imyrs/chii-bot:latest
    ```
   HTTP and SOCKS5 proxy are supported.
