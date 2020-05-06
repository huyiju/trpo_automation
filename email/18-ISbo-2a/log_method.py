import logging
import configparser

config = configparser.RawConfigParser()
config.read('logging_config.conf')
levels ={
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
logging.basicConfig(
    filename=config['DEFAULT']['file'],
    level=levels[config['DEFAULT']['level']],
    format=config['DEFAULT']['format'])

logger = logging.getLogger(__name__) 

def log_method_info(method):
    def write_logs(*args, **kwargs):
        try:
            logger.info(f'Got into "{method.__name__}" with data {args} and {kwargs}')
            result = method(*args, **kwargs)
            logger.debug(f'Method "{method.__name__}" has returned - {result}')
            logger.info(f'Method "{method.__name__}" has completed')
            return result
        except Exception as ex:
            logger.exception(ex)
            logger.error(f'Method "{method.__name__}" has crashed')
    return write_logs

if __name__ == '__main__':
    @log_method_info
    def ananas(x):
        print ('ananas')
        print(1/0)

    ananas(65)