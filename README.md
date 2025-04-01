<div align="center">
<h1>七宝 ChiiBot</h1>
<i>一个优雅的 Telegram 私聊机器人，提供更简单、智能的转发功能。</i>
</div>

<a href="https://github.com/ImYrS/ChiiBot/blob/main/README_EN.md">EN</a> | 中文

> [!WARNING]  
> 此项目目前仍处于快速迭代阶段，可能存在 Bug 或不稳定问题。且随时可能发生破坏性更新。

## ✨ 主要特性

- **群内论坛模式**
  > 七宝会给每位发送消息的访客分配一个独立的话题，用于更清晰、方便的回复不同访客。

- **可选回复消息**
  > 你可以选择在回复对方信息的同时，是否要回复到原消息。七宝会在转发你的消息时，自动进行对应的回复映射。

- **黑名单**
  > 你可以将不想接收消息的用户拉入黑名单，或将其解除拉黑。

- **Reaction 反馈**
  > 七宝使用 Reaction 来提示转发成功，而不是烦人的消息提示或干脆无提示。

- **简单易用**
  > 无需公网 IP、可使用代理部署、只需设置 Bot Token 即可，支持多语言。

## 🚀 开始使用

### 准备工作

1. 通过 [@BotFather](https://t.me/botfather) 创建一个机器人，并保存机器人的 Token。
2. **创建一个新群组**, 将机器人添加到群组中, 并**将其设定为管理员**。
3. **将群组设置为论坛模式**。
    - 在群组设置中打开 "Topic" 选项。
    - 现在你的群组就处于论坛模式了。

### 部署机器人

#### Docker

> 此文假设你已安装并运行了Docker。

1. 准备一个文件夹用于持久化保存机器人的数据库。
   ```bash
   mkdir -p /path/to/ChiiBotData
   ```
2. 使用 Docker 运行机器人.  
   将下文中的 `{YOUR_BOT_TOKEN}` 替换为你自己的 BOT Token。
   ```bash
   docker run -d \
     --name ChiiBot \
     -v /path/to/ChiiBotData:/app/data \
     -e CORE_BOT_TOKEN={YOUR_BOT_TOKEN} \
     imyrs/chii-bot:latest
   ```

#### non-Docker

> 还没写完...

### 最后一步

在你前面创建的群组中发送 `/chii_setup`。如果没问题，你会收到设置成功的提示。

> 七宝会将群组 ID 和管理员 ID （你）保存到数据库中。

### 大功告成！

尝试用另一个 Telegram 账号给机器人发送消息吧。

## 如何更新

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

1. 如何使用代理  
   你可以在运行 Docker 时添加 `-e CORE_PROXY={YOUR_PROXY_URL}` 来使用代理。比如：
    ```bash
    docker run -d \
      --name ChiiBot \
      -v /path/to/ChiiBotData:/app/data \
      -e CORE_BOT_TOKEN={YOUR_BOT_TOKEN} \
      -e CORE_PROXY=http://127.0.0.1:6969 \
      imyrs/chii-bot:latest
    ```
   同时支持 HTTP、SOCKS5 代理。

## 其他

- 如果有 Bug 或者想增加的功能请在 issues 中反馈。
- 欢迎提交 PR。
- 如果你觉得这个项目不错，请给我点个 Star 吧！
- 此项目的 Readme 尚不完整。如果你有兴趣完善它，请提交 PR，非常感谢！