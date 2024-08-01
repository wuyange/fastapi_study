from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # 连接数据库引擎
    ASYNC_DB_DRIVER: str = "mysql+aiomysql"
    # 连接数据库引擎
    SYNC_DB_DRIVER: str = "mysql"
    # 数据库HOST
    DB_HOST: str = "10.182.79.36"
    # 数据库端口号
    DB_PORT: int = 3306
    # 数据库用户名
    DB_USER: str = "root"
    # 数据库密码
    DB_PASSWORD: str = "123456"
    # 需要连接数据库名称
    DB_DATABASE: str = "book_system"
    # 是否输出SQL语句
    DB_ECHO: bool = True
    # 默认的连接池的额大小
    DB_POOL_SIZE: int = 60
    DB_MAX_OVERFLOW: int = 0

    #公众号-开发者ID(AppID)
    GZX_ID: str = 'wxe41915525f7f229f' # 微信公众号ID
    #公众号-开发者密码
    GZX_SECRET:str = '7041d80c5574502e32ef63b2eea14a8e'
    GZX_PAY_KEY: str = '0wmDjLVuk904Ddyj0fLwpX1ymiBMIkXh' # 微信支付秘钥
    MCH_ID: str = '1613748420' # 微信支付ID
    NOTIFY_URL =   'http://hx.wohuayuan.com/hs/api/v1/doctor/subscribe/paycallback' #支付回调

    #  没有值的情况下的默认值--默认情况下读取的环境变量的值
    # 链接用户名
    RABBIT_USERNAME: str = 'admin'
    # 链接密码
    RABBIT_PASSWORD: str = 'admin'
    # 链接的主机
    RABBIT_HOST: str = 'rabbit'
    # 链接端口
    RABBIT_PORT: int = 5672
    # 要链接租户空间名称
    VIRTUAL_HOST: str = 'yuyueguahao'
    # 心跳检测
    RABBIT_HEARTBEAT = 5


@lru_cache()
def get_settings():
    return Settings()
