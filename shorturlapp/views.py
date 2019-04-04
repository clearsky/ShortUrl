from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from urllib.parse import unquote
from shorturlapp.url_handle import UrlHandle
from shorturlapp.exception import LongUrlFormatException, CharSetTimeOut, ShortUrlAlreadyExist, InputShortUrlError,\
    LongUrlTooLongError, ShortUrlTooLongError
from shorturlapp.models import Info
from ShortUrl.settings import STATUS_CODE
import qrcode
import logging
import base64
from io import BytesIO
# Create your views here.
logger = logging.getLogger(__name__)
url_handle = UrlHandle()
index_count = 0  # 主页访问的次数
produce_short_url_count = 0  # 生成短链接key成功的次数
redirect_count = 0  # 访问短链接进行跳转的次数


def short_url(request):
    """
    返回主页，GET和POST方法请求都支持
    :param request:
    :return:index.html
    """
    logger.debug('请求index.html')
    global index_count
    index_count += 1  # 主页访问次数增加
    return render(request, 'index.html')


def homepage(request):
    """
    home_page,自动跳转到short_url/
    访问此页面不增加主页访问次数
    :param request:
    :return:跳转到short_url/
    """
    logger.debug('正在跳转到主页')
    return redirect('shorturl/')


def set_short_url(request):
    """
    接受GET请求生成短链接key
    :param request:
    :return: json格式的消息，短链接，长连接，状态码
    """
    msg = 'DEFAULT ERROR'
    code = STATUS_CODE['DEFAULT_ERROR']
    result = None  # 存储短链接key的最终结果
    short_url = None
    long_url = None
    host = request.META['HTTP_HOST']  # 获取当前请求域名，用于和短链接key拼接短链接
    logger.debug('host获取完成')
    global produce_short_url_count
    if request.method == 'POST':  # 只支持POST
        long_url = request.POST['long_url']  # 获取长链接
        try:  # 测试用户是否传入自定义的短链接，如果传入，赋值给short_url
            short_url = request.POST['short_url']
            logger.debug('获取到用户输入的自定义的短链接key:{}'.format(short_url))
        except MultiValueDictKeyError as e:
            logger.debug('用户没有输入自定义的短链接key')
            pass
        try:
            if short_url:  # 如果用户传入了短链接key，抛出长连接已存在异常，进入异常处理，不进行长连接是否已存在的判断
                raise Info.DoesNotExist
            find_obj = Info.objects.get(long_url=long_url)  # 测试长连接是否已存在，如用户未传入自定义的短链接key，则返回已有的短链接key
            result = 'http://{}/{}'.format(host, find_obj.short_url)  # 从数据库返回数据中获取短链接key，并拼接为短链接
            msg = 'ok'
            code = STATUS_CODE['OK']
            produce_short_url_count += 1
            logger.debug('长链接:{}已存在，返回已存在的短链接:{}'.format(long_url, result))
        except Info.DoesNotExist as e:  # 捕获长链接已存在异常
            try:
                short_url = url_handle.run(long_url=long_url, short_url=short_url)  # 获取新的短链接key
                logger.debug('获取到新的短链接key:{}'.format(short_url))
                obj = Info.objects.create(long_url=long_url, short_url=short_url)  # 数据库插入数据
            except LongUrlFormatException as e:  # 捕获长链接格式异常
                logger.error(e)
                msg = str(e)  # 将错误消息赋值给msg，用于返回给用户
                code = e.code  # 状态码设置为ERROR
            except CharSetTimeOut as e:  # 捕获尝试生成短链接key超过最多次数异常
                logger.error(e)
                msg = str(e)
                code = e.code
            except ShortUrlAlreadyExist as e:  # 捕获短链接shukey已存在异常
                logger.error(e)
                msg = str(e)
                code = e.code
            except InputShortUrlError as e:  # 捕获用户输入的自定义的短链接key非法异常
                logger.error(e)
                msg = str(e)
                code = e.code
            except LongUrlTooLongError as e:  # 长链接超出最大长度
                logger.error(e)
                msg = str(e)
                code = e.code
            except ShortUrlTooLongError as e:  # 短链接key超出最大长度
                logger.error(e)
                msg = str(e)
                code = e.code
            else:
                obj.save()  # 提交数据库操作
                result = 'http://{}/{}'.format(host, short_url)  # 设置结果
                logger.debug('生成新的短链接')
                msg = 'ok'
                code = STATUS_CODE['OK']
                produce_short_url_count += 1  # 成功生成短链接key次数增加
    elif request.method == 'GET':  # 不支持GET方式
        msg = '请求方式错误'
        code = STATUS_CODE['DEFAULT_ERROR']
        logger.debug('请求方式错误')
    response = {  # 构造返回数据
        'msg': msg,
        'short_url': result,
        'long_url': long_url,
        'code': code,
    }
    try:  # 生成二维码
        _ = request.POST['qrcode']
        if code == STATUS_CODE['OK']:
            f = BytesIO()
            img = qrcode.make(result)
            img.save(f)
            response['qrcode'] = str(base64.standard_b64encode(f.getvalue()))[2:-1]
    except MultiValueDictKeyError as e:
        response['qrcode'] = False
        logger.debug('用户未请求二维码')
    logger.info('返回数据:{}'.format(response))
    return JsonResponse(data=response, json_dumps_params={"ensure_ascii": False})   # 返回json格式数据


def redirect_to_long_url(request):
    """
    访问短链接时，进行跳转
    :param request:
    :return:
    """
    short_url = request.get_full_path().replace('/', '')  # 获取短链接key
    short_url = unquote(short_url)  # 将获取到的短链接key进行转码
    global redirect_count
    try:
        find_obj = Info.objects.get(short_url=short_url)  # 测试是否存在此短链接key，否则自动触发异常
        long_url = find_obj.long_url  # 从数据库返回的结果获取长链接
        redirect_count += 1  # 访问短链接跳转次数增加
        logger.debug('即将跳转到:{}'.format(long_url))
        return redirect(long_url, permanent=True)  # 跳转到长链接
    except Info.DoesNotExist as e:  # 数据库不存在此短链接key
        data = {  # 构造返回数据
            'msg': '短链接不存在',
            'code': STATUS_CODE['SHOURT_URL_NOT_EXIST'],
            'short_url': short_url,
        }
        logger.error(data)
        return JsonResponse(data=data, json_dumps_params={'ensure_ascii': False})


def get_count(request):
    """
    获取访问统计
    :param request:
    :return:
    """
    data = {  # 构造返回数据
        'index_count': index_count,  # 主页访问次数
        'produce_short_url_count': produce_short_url_count,  # 成功生成短链接次数
        'redirect_count': redirect_count,  # 访问短链接进行跳转的次数
        'sum_count': index_count + produce_short_url_count + redirect_count,  # 以上三个次数相加
    }
    logger.info(data)
    return JsonResponse(data=data, json_dumps_params={'ensure_ascii': False})  # 返回json格式数据
