import os

from dotenv import load_dotenv
from tortoise import Tortoise, fields, models

from src import utils
from src.types import SendBy, SettingKey, SettingType

# 加载环境变量
load_dotenv()

# 数据库连接配置
if os.getenv("DB_TYPE") == "mysql":
    db_config = {
        "engine": "tortoise.backends.mysql",
        "credentials": {
            "database": os.getenv("DB_DATABASE"),
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "charset": "utf8mb4",
        },
    }
else:
    db_config = {
        "engine": "tortoise.backends.sqlite",
        "credentials": {
            "file_path": f"data/{os.getenv('DB_DATABASE', 'chii_bot')}.db",
        },
    }

TORTOISE_ORM = {
    "connections": {"default": db_config},
    "apps": {
        "models": {
            "models": ["src.database"],
            "default_connection": "default",
        }
    },
}


# 抽象 BaseModel 定义
class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.BigIntField(default=0)
    updated_at = fields.BigIntField(default=0)

    async def save(self, *args, **kwargs):
        now = utils.now()
        if not self.id:
            self.created_at = now
        self.updated_at = now
        await super().save(*args, **kwargs)

    class Meta:
        abstract = True


class User(BaseModel):
    user_id = fields.IntField(unique=True)  # Telegram User ID, unique
    topic_id = fields.IntField(null=True)  # Topic ID, 可为空
    name = fields.CharField(max_length=255, null=True)  # 非唯一
    username = fields.CharField(
        max_length=255, null=True, unique=True
    )  # Telegram username, unique, 可为空
    blocked = fields.BooleanField(default=False)  # 是否屏蔽
    tutorial_step = fields.IntField(default=0)  # 教程步骤
    message_available_count = fields.IntField(
        default=2
    )  # 剩余可发送消息的次数, -1 为无限制

    class Meta:
        table = os.getenv("DB_PREFIX", "") + "user"


class ForwardMessage(BaseModel):
    user = fields.ForeignKeyField(
        "models.User", related_name="messages", on_delete=fields.CASCADE
    )  # 关联 User 表
    from_chat_id = fields.IntField()  # 原始 Chat
    to_chat_id = fields.IntField(null=True, default=None)  # 转发后的 Chat
    from_message_id = fields.IntField()  # 原始消息
    to_message_id = fields.IntField(null=True, default=None)  # 转发后的消息
    send_by = fields.IntEnumField(SendBy, default=SendBy.HOST)  # 消息发送者

    class Meta:
        table = os.getenv("DB_PREFIX", "") + "forward_message"


class Setting(BaseModel):
    key = fields.CharEnumField(SettingKey, max_length=255, unique=True)
    value = fields.TextField()
    type_ = fields.IntEnumField(SettingType, default=SettingType.STRING)

    class Meta:
        table = os.getenv("DB_PREFIX", "") + "setting"


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
