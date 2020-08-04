import hashlib
import os
import random
import time
from threading import Thread

import requests
from lxml import etree


def downloadFile(session, url, headers, dirPath, fileName):
    if fileName is None:
        fileName = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest() + url[url.rindex("."):]

    if dirPath is None:
        dirPath = os.path.dirname(__file__) + "/file/"

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    filePath = os.path.join(dirPath, fileName)

    if os.path.exists(filePath):
        print("-" * 5 + filePath + " exists" + "-" * 5)
        return

    requests.packages.urllib3.disable_warnings()
    response = session.get(url, headers=headers, verify=False)

    with open(filePath, 'wb') as fp:
        fp.write(response.content)

    print("-" * 5 + filePath + " write finish" + "-" * 5)
    # print(filePath)


def parseHtmlByUrl(session, url, headers, xpath):
    requests.packages.urllib3.disable_warnings()
    response = session.get(url, headers=headers, verify=False)
    html = etree.HTML(response.content)
    results = html.xpath(xpath)
    return results


if __name__ == "__main__":
    session = requests.session()
    basicDirPath = os.path.dirname(__file__) + "/file/"
    doMain = "http://www.quantuwang.co"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/69.0.3497.100 Safari/537.36",
    }
    beginUrl = "http://www.quantuwang.co/meinv/"

    beginHrefs = parseHtmlByUrl(session, beginUrl, headers=headers, xpath="//ul[@class='ul960c']//a/@href")

    for beginHref in beginHrefs:
        titleDir = parseHtmlByUrl(session, doMain + beginHref, headers=headers,
                                  xpath="//div[@class='c_title']//h1/text()")
        titleDir = "".join(titleDir)
        imgSet = set()
        imgSet.add(doMain + beginHref)
        imgHrefs = parseHtmlByUrl(session, doMain + beginHref, headers=headers, xpath="//div[@class='c_page']//a/@href")

    for imgHref in imgHrefs:
        imgSet.add(doMain + imgHref)

    fullDirPath = os.path.join(basicDirPath, titleDir)
    print(fullDirPath)

    for href in imgSet:
        Thread(target=downloadFile(session, href, headers, fullDirPath, None))
        time.sleep(random.randint(0, 3))
        # print(imgSet)
        # print(len(imgSet))
        # break
