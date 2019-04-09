# -*- coding: utf-8 -*-

# Scrapy settings for kSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'kSpider'

SPIDER_MODULES = ['kSpider.spiders']
NEWSPIDER_MODULE = 'kSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'kSpider.middlewares.KspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'kSpider.middlewares.UserAgentDownloaderMiddleware': 543,
   'scrapy.downloadermiddlewares.retry.RetryMiddleware':100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'kSpider.pipelines.KspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 6
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 重复请求数
RETRY_ENABLED = True
RETRY_TIMES = 1     # default = 2   180s
DOWNLOAD_TIMEOUT = 60


######## scrapy-redis
# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 30
SCHEDULER_PERSIST = True        # 持久化
SCHEDULER_FLUSH_ON_START = False    # del redis:dupefilter key


# for selenium
CHROME_DRIVER='D:/develop/seleniumDrivers/chromedriver.exe'



# 允许error_code
HTTPERROR_ALLOWED_CODES = [302]


# for kafka
# Kafka_HOST='localhost:9092'
# Kafka_TOPIC='kafka_topic'


# for redis
REDIS_HOST = '200.200.200.7'   # 未配置 redis 和 mysql远程连接的 都卡 这儿了
REDIS_PORT='6380'
REDIS_PASSWORD='123456'
REDIS_URL = 'redis://:{}@{}:{}'.format(REDIS_PASSWORD,REDIS_HOST,REDIS_PORT)   # RedisSpider
# for sadd
# REDIS_START_URLS_AS_SET = True


# for splash
SPLASH_URL = 'http://200.200.200.7:8050'


# splash+nginx 负载均衡
NGINX_SPLASH_URL='http://200.200.200.7:8049'



# for image Download
IMAGES_STORE='E:\\IMGS'
# IMAGES_MIN_HEIGHT=100
# IMAGES_MIN_WIDTH=100