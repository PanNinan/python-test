import logging


def logger(filename):
    log = logging.getLogger()
    log.setLevel('DEBUG')

    fh = logging.FileHandler(filename=filename)
    ch = logging.StreamHandler()

    fm = logging.Formatter("%(asctime)s %(message)s")

    fh.setFormatter(fm)
    ch.setFormatter(fm)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


logger = logger('logger.log')
logger.warning('worning message')
