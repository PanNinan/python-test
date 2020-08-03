# logging日志
import logging

logging.basicConfig(
    level=logging.DEBUG,  # log显示的级别
    filename='log.log',  # 日志存入的文件名
    format='%(asctime)s %(filename)s [%(lineno)d] %(message)s',
)

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')
