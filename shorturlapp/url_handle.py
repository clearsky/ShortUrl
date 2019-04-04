"""
UrlHandle类用于验证传入的长连接和短链接的格式和内容是否正确
如果未传入短链接，就生成短链接
"""
import re
import random
import logging
from shorturlapp.exception import LongUrlFormatException, ShortUrlAlreadyExist, CharSetTimeOut, InputShortUrlError, ShortUrlTooLongError, LongUrlTooLongError
from shorturlapp.models import Info
from ShortUrl.settings import PRODUCE_SHORT_URL_KEY_LENGTH, PRODUCE_SHORT_URL_TRY_TIMES, URLS, SHORT_URL_KEY_CHAR_SETS, \
    BIG_CHAR_SETS_PRODUCE_NUMBER, LONG_URL_MAX_LENGTH, SHORT_URL_MAX_LENGTH, STATUS_CODE

logger = logging.getLogger(__name__)


class UrlHandle:
    def __init__(self):
        self.long_url = None
        self.short_url = None
        self.char_set = []  # 用于生成短链接key的字符集
        self.init_base_char_set()  # 初始化基本字符集
        self.PRODUCE_SHORT_URL_TRY_TIMES = PRODUCE_SHORT_URL_TRY_TIMES  # 生成短链接key的尝试次数
        self.PRODUCE_SHORT_URL_KEY_LENGTH = PRODUCE_SHORT_URL_KEY_LENGTH  # 待生成的短链接的key的长度

    def init_base_char_set(self):
        """
        初始化基本的字符集，因为基本字符集内容较少，所以先初始化并存入一个char_set列表当中
        :return:
        """
        logger.debug('开始初始化基本字符集')
        numbers = SHORT_URL_KEY_CHAR_SETS['NUMBERS']  # 是否开启数字字符集
        uppercase_letters = SHORT_URL_KEY_CHAR_SETS['UPPERCASE_LETTERS']  # 是否开启大写字母字符集
        lowwercase_letters = SHORT_URL_KEY_CHAR_SETS['LOWWERCASE_LETTERS']  # 是否开启小写字符集
        special_symbols = SHORT_URL_KEY_CHAR_SETS['SPECIAL_SYMBOLS']  # 是否开启特殊符号字符集
        if numbers:
            for i in range(10):  # 将数字加入char_set列表
                self.char_set.append(chr(i + 48))
        if uppercase_letters:
            for i in range(26):
                self.char_set.append(chr(i + 65))  # 大写字母加入char_set列表
        if lowwercase_letters:
            for i in range(26):
                self.char_set.append(chr(i + 97))  # 小写字母加入char_set列表
        if special_symbols:  # 特殊符号加入char_set列表
            for i in range(15):
                self.char_set.append(chr(i + 33))
                if i < 7:
                    self.char_set.append(chr(i + 58))
                if i < 6:
                    self.char_set.append(chr(i + 91))
                if i < 4:
                    self.char_set.append(chr(i + 123))
            self.char_set.remove('\\')  # 删除掉不合法的符号
            self.char_set.remove('/')
            self.char_set.remove('?')
            self.char_set.remove('#')
        random.shuffle(self.char_set)  # 打乱char_set列表的顺序
        logger.debug('初始化基本字符集完成')

    def check_long_url(self, long_url):
        """
        通过正则表达式检查长链接是否合法
        只检测长链接的域名部分
        :param long_url: 传入的长链接
        :return: 一个布尔值，表示传入的长链接是否合法
        """
        logger.debug('开始检查长链接:{}'.format(long_url))
        if len(long_url) > LONG_URL_MAX_LENGTH:
            logger.debug('长链接:{}过长'.format(long_url))
            raise LongUrlTooLongError('长链接:{}超出最大长度:{}'.format(long_url, LONG_URL_MAX_LENGTH),
                                      STATUS_CODE['LONG_URL_TOO_LONG_ERROR'])
        self.long_url = long_url
        result = re.search(r'^((http|https)://)([a-zA-Z0-9-]+\.)+([a-zA-Z0-9]+)(/.*)*', self.long_url, re.IGNORECASE)
        if not result or result.group() != self.long_url:
            logger.debug('长链接:{}不合法'.format(long_url))
            return False
        logger.debug('长链接:{}通过检查'.format(long_url))
        return True

    def check_short_url(self):
        """
        检查短链接key是否合法
        短链接key不能和路由系统中的url重合，不能和已有的短链接key重合，不能含有空格和?,/,\
        :return: 返回一个布尔值，表示短链接key是否合法
        """
        logger.debug('开始检查短链接:{}'.format(self.short_url))
        if len(self.short_url) > SHORT_URL_MAX_LENGTH:  # 短链接超出最大长度，抛出异常
            logger.debug('短链接key:{}过长'.format(self.short_url))
            raise ShortUrlTooLongError('短链接key:{}超出最大长度:{}'.format(self.short_url, SHORT_URL_MAX_LENGTH),
                                       STATUS_CODE['SHORT_URL_TOO_LONG_ERROR'])
        for url in URLS.values():  # 判断是否和路由系统中的url重合
            if re.search(url, self.short_url) or re.search(url.replace('/', '') + r'(\?.*)*$', self.short_url):
                logger.debug('短链接key:{}与系统路由重合'.format(self.short_url))
                return STATUS_CODE['SHOURT_URL_EXIST']
        if re.search(r'\?.*', self.short_url) or re.search(r'/.*', self.short_url) or re.search(r'\\.*', self.short_url)\
                or re.search(r'#.*', self.short_url):  # 判断是否含有不合法的符号
            logger.debug('短链接key:{}含有非法符号'.format(self.short_url))
            return STATUS_CODE['INPUT_SHORT_URL_ERROR']
        try:
            Info.objects.get(short_url=self.short_url)  # 判断是否和已有的短链接key重合
            logger.debug('短链接key"{}已存在'.format(self.short_url))
            return STATUS_CODE['SHOURT_URL_EXIST']
        except Info.DoesNotExist as e:
            logger.debug('短链接key:{}通过检查'.format(self.short_url))
            return STATUS_CODE['OK']

    def init_big_char_sets(self):
        """
        初始化大字符集，包括中文和emoji表情
        每次需要使用这部分字符时，随机生成一定数量的字符，追加到char_set中
        :return:
        """
        logger.debug('开始初始化大字符集')
        chinese = SHORT_URL_KEY_CHAR_SETS['CHINESE']  # 是否开启中文字符集
        emoji = SHORT_URL_KEY_CHAR_SETS['EMOJI']  # 是否开启emoji字符集
        chinese_number = BIG_CHAR_SETS_PRODUCE_NUMBER['CHINESE']  # 生成中文字符的数量
        emoji_number = BIG_CHAR_SETS_PRODUCE_NUMBER['EMOJI']  # 生成emoji字符的数量

        if chinese:
            logger.debug('中文字符集已开启')
            for _ in range(chinese_number):  # 生成并追加中文字符
                self.char_set.append(chr(random.randint(0x4e00, 0x9fbf)))
        if emoji:
            logger.debug('emoji字符集已开启')
            for i in range(emoji_number):  # 生成并追加emoji表情，emoji的unicode码不连续
                if i <= emoji_number / 6:
                    self.char_set.append(chr(random.randint(0x1F601, 0x1F64F)))
                elif i <= (emoji_number / 6) * 2:
                    self.char_set.append(chr(random.randint(0x2702, 0x27B0)))
                elif i <= (emoji_number / 6) * 3:
                    self.char_set.append(chr(random.randint(0x1F680, 0x1F6C0)))
                elif i <= (emoji_number / 6) * 4:
                    self.char_set.append(chr(random.randint(0x24C2, 0x1F251)))
                elif i <= (emoji_number / 6) * 5:
                    self.char_set.append(chr(random.randint(0x1F600, 0x1F636)))
                else:
                    self.char_set.append(chr(random.randint(0x1F30D, 0x1F567)))
        random.shuffle(self.char_set)  # 打乱char_set的顺序
        logger.debug('大字符集初始化完成')

    def clear_big_char_sets(self):
        """
        当大字符集使用完后，清除char_set中大字符集中的字符，只保留基本字符集的内容
        :return:
        """
        logger.debug('开始清除大字符集符号')
        self.char_set = list(filter(lambda x: ord(x) < 138, self.char_set))
        logger.debug('大字符集符号清楚完成')

    def get_short_url(self):
        """
        生成短链接的key
        :return:
        """
        logger.debug('开始生成短链接key')
        self.init_big_char_sets()  # 初始化大字符集
        count = 0  # 记录尝试生成短链接key的次数
        # 一次生辰短链接key可能不会成功，所以使用循环生成，直至成功或次数超过限制
        while True:
            result = random.choices(self.char_set, k=self.PRODUCE_SHORT_URL_KEY_LENGTH)  # 从char_set中取出相应个数的字符
            self.clear_big_char_sets()  # 清空char_set中的大字符集的字符
            result = ''.join(result)  # 将获取到的字符连接成字符串
            self.short_url = result
            try:
                if self.check_short_url() == STATUS_CODE['OK']:  # 检查生成的短链接key是否合法，有可能会重复
                    logger.debug('短链接key生成成功:{}'.format(self.short_url))
                    break
            except ShortUrlTooLongError as e:  # 短链接key超过最大长度，上浮异常
                logger.error('生成的短链接key:{}超过最大长度:{}'.format(self.short_url, SHORT_URL_MAX_LENGTH))
                raise e
            count += 1  # 计数器自增
            if count >= self.PRODUCE_SHORT_URL_TRY_TIMES:  # 当尝试次数达到上限，抛自定义出异常
                logger.error('尝试生成短链接key次数超过上限:{}'.format(PRODUCE_SHORT_URL_TRY_TIMES))
                raise CharSetTimeOut('生成短链接key的尝试次数达到上限', STATUS_CODE['CHAR_SET_TIME_OUT'])

    def run(self, long_url, short_url=None):
        """
        完整运行
        :param long_url:传入的长连接
        :param short_url: 当用户传入的自定义的短链接key，如果用户没有传入，默认未None
        :return: 合法的短链接key
        """
        try:
            if not self.check_long_url(long_url=long_url):  # 检查长链接是否合法
                raise LongUrlFormatException('long_url:{}格式错误'.format(long_url), STATUS_CODE['LONG_URL_FORMAT_ERROR'])
        except LongUrlTooLongError as e:  # 长链接超出最大长度，上浮异常
            raise e
        if short_url:  # 判断用户是否传入自定的短链接key
            self.short_url = short_url
            try:
                check = self.check_short_url()  # 检查用户传入的短链接key是否合法
            except ShortUrlTooLongError as e:  # 短链接key超出最大长度，上浮异常
                raise e
            if check == STATUS_CODE['OK']:  # 用户传入的短链接key合法
                return self.short_url
            elif check == STATUS_CODE['SHOURT_URL_EXIST']:  # 用户传入的短链接key和已存在的短链接key重合
                logger.error('输入的短链接key:{}已存在'.format(self.short_url))
                raise ShortUrlAlreadyExist('短链接:{}已被使用'.format(self.short_url), STATUS_CODE['SHOURT_URL_EXIST'])
            elif check == STATUS_CODE['INPUT_SHORT_URL_ERROR']:  # 用户传入的短链接key存在非法符号
                logger.error('输入的短链接key:{}含有非法字符'.format(self.short_url))
                raise InputShortUrlError('输入的短链接key:{}有误'.format(self.short_url), STATUS_CODE['INPUT_SHORT_URL_ERROR'])
        self.get_short_url()  # 用户未传入短链接key，调用函数生成
        logger.info(self.short_url)
        return self.short_url
