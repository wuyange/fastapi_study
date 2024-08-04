from fastapi import Depends
from exts.responses.json_response import Success, Fail
from . import userorders
from schemas.useroders.wxauth_login import WxCodeForm
from config.config import get_settings
from wechatpy import WeChatClient, WeChatOAuth, WeChatOAuthException, WeChatException


def getWeChatOAuth(redirect_url):
    """
    获取微信OAuth
    :param redirect_url: 跳转的url
    :return:
    """
    wx_oauth = WeChatOAuth(get_settings().GZX_ID, get_settings().GZX_SECRET, redirect_url, 'snsapi_userinfo')
    print(wx_oauth.get_user_info())
    return wx_oauth


@userorders.get("/login", summary='微信授权登入')
async def callbadk(*, forms: WxCodeForm = Depends(WxCodeForm)):
    wechat_oauth = None
    try:
        CODE = forms.code.strip()
        wechat_oauth = getWeChatOAuth(redirect_url='')
        # 第二步：通过code换取网页授权access_token
        res_openid = wechat_oauth.fetch_access_token(CODE)
    except WeChatOAuthException as wcpayex:
        if not wcpayex.errcode:
            pass
            return Fail(api_code=200, result=None, message='授权处理失败,原因：{}'.format(str(wcpayex.errmsg)))
    except Exception as ex:
        return Fail(api_code=200, result=None, message='授权处理失败,原因：未知异常的错误信息')

    user_info = wechat_oauth.get_user_info()
    # 正常的获取到用户信息
    openid = user_info.get('openid')
    avatar_url = user_info.get('headimgurl')
    city = user_info.get('city')
    coutry = user_info.get('country')
    nick_name = user_info.get('nickname')
    province = user_info.get('province')
    sex = '男' if user_info.get('sex') == 1 else '女'

    data = {
        "openid": openid,
        "nick_name": nick_name,
        "avatar_url": avatar_url,
        "usex": sex
    }
    return Success(api_code=200, result=data, message='获取成功')
