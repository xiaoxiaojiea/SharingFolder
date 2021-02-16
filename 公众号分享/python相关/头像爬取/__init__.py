import requests
import re



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}


def getUrlsToDetail(BASE_URL):

    response = requests.get(BASE_URL,headers = headers)   # 得到 Response 对象
    response = response.text  # 使用 text 方法将 Response 对象解码为 字符串。

    resultTemp =re.findall(' <a href="/nstx/(.*?)" ', response, re.S)


    result = []
    for temp in resultTemp:
        url = BASE_URL + temp

        result.append(url)

    return(result)


def getImagesUrl(detailUrl):

    response = requests.get(detailUrl, headers=headers).text  # 源代码的字符串

    resultTemp = re.findall('src="http://ww1.sinaimg.cn/large(.*?)"', response, re.S)

    result = []
    for urlEnd in resultTemp:
        url = 'http://ww1.sinaimg.cn/large' + urlEnd

        result.append(url)

    return(result)


def saveImages(imgUrl):

    response = requests.get(imgUrl, headers=headers).content  # 解码为 二进制数据，

    # http://ww1.sinaimg.cn/large/005NWMakgy1gnodp163pij30b40b4dh6.jpg

    # [ 'http:' ,'' , 'ww1.sinaimg.cn',  'large', '005NWMakgy1gnodp163pij30b40b4dh6.jpg' ]

    imgName = imgUrl.split("/")[-1]


    with open('./images/'+imgName ,'wb' ) as f:

        f.write(response)




if __name__ == '__main__':

    BASE_URL = 'https://www.bizhizj.com/nstx/'

    detailUrls = getUrlsToDetail(BASE_URL)
    # print(detailUrls)

    imageUrlLists = []
    for detailUrl in detailUrls:
        imageUrlList = getImagesUrl(detailUrl)

        for url in imageUrlList:
            imageUrlLists.append(url)

    # 每个图片真实的地址。
    # print(imageUrlLists)

    print("开始保存...")
    for imgUrl in imageUrlLists:
        saveImages(imgUrl)
    print("保存完成.")



