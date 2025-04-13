## Claw Cloud 部署教程

### 注册

使用此链接进入并**使用 GitHub 登录**：[立即注册 Claw Cloud](https://console.run.claw.cloud/signin?link=MJV2T1RZPBM9)

> [!NOTE]
> ✨如果你的 GitHub 账号注册了超过 180 天，Claw Cloud 会每月赠送你 $5 美元的使用额度，足以宽裕的使用本项目。 

### 切换地区

推荐选择德国地区部署七宝，可获得最佳的 Bot 交互速度。  
你可以在 Claw Cloud 左上角切换地区至德国。

<img width="431" alt="image" src="https://github.com/user-attachments/assets/1e2c6e95-9570-4f6e-b264-75e1dd1175d3" />

### 创建容器

1. 打开 App Launchpad
2. 点击右上角 Create App
3. 填写创建参数
  1. Application Name 应用名称：自定义，命名规则和域名要求相同，推荐使用小写英文。
  2. Image 镜像：选择 Public 并填写 `imyrs/chii-bot:latest`
  3. Usage 用量：其实就是配置，建议参考我的配置：选择 Fixed，Replicas: 1, CPU: 0.5, Memory: 1G。这个配置下价格每月刚好不会超过 Claw 送的 $5 用量。
  4. Network 网络：七宝没有对外暴露接口，所以忽略即可
  5. Advanced Configuration 进阶配置：只改 Environment Variables 和 Local Storage。
    - Environment Variables: 添加 `CORE_BOT_TOKEN={YOUR_BOT_TOKEN}`，替换你自己的 Bot token 进去。
    - Local Storage: Capacity 为 1，Mount Path 为 `/app/data` 用于保存数据库。

此时你的配置应如图所示：
<img width="1203" alt="image" src="https://github.com/user-attachments/assets/8d3a3c6e-057c-493e-ae63-5e78f3b2834a" />

确认无误后点击右上角 **Deploy Application** 即可。

### 等待并确认容器启动

等待容器左上角状态从 Waiting 转变为 Running 容器即部署完成。
<img width="584" alt="image" src="https://github.com/user-attachments/assets/8a61b951-2323-4937-b25a-02d919ef5b8c" />

### 提示

使用前请确认 Bot 已经加入 Topic 类型群组内并授予管理员权限，否则无法成功转发哦～



