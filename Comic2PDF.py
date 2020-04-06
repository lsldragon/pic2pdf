import requests
from colorama import *
import time
import os
import fitz
import glob
from pyquery import PyQuery as pq

# 获取当前时间戳,这个值无所谓,加上会更有爬虫的尊严。返回值:当前时间的时间戳long类型
def getmsTime():
    t = time.time()
    mst = int(round(t * 1000))
    return mst

# 获取图片链接地址，批量获取微博头条文章下的所有图片的url链接。返回值：url链接图片列表
def generate_img_urls(id):

    tm = getmsTime()
    url = "https://card.weibo.com/article/m/aj/detail?id=%s&_t=%s" % (
        id, str(tm))

    refervalue = "https://card.weibo.com/article/m/show/id/%s" % id
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0".3809.100 Safari/537.36',
               'Referer': refervalue}

    response = requests.get(url, headers=headers)

    text = response.json()

    print("--------------------------------------")
    print("谨以此软件献给永远的神作----龙珠")
    print("漫画: " + text['data']['title'])
    print("发布时间: " + text['data']['create_at'])
    print("阅读量: " + text['data']['read_count'])
    print(Style.RESET_ALL)

    img_url_all = text['data']['content']
    pic_url = []
    doc = pq(img_url_all)
    lis = doc('p img').items()
    for li in lis:
        pic_url.append(li.attr('src'))
    return pic_url

# 创建下载文件夹，建一个临时缓存文件夹用于储存下载图片的位置，最后会被删掉。返回值：文件夹的路径
def create_down_dir():
    path = "./download/"
    if not os.path.exists(path):
        os.mkdir(path)
    return path

# 下载图片，获得到图片的url链接后就可下载图片。返回值：文件夹的路径。
def download_imgs(img_urls):

    path = create_down_dir()
    count = 1
    for strimg in img_urls:
        response = requests.get(strimg)
        with open(path + str(count).zfill(3) + strimg[-4:], 'wb') as file:
            file.write(response.content)
            print(Fore.GREEN + "已下载 " + strimg)
        count += 1

    return path

# 生成pdf文档，把下载的图片生成一个默认A4大小的PDF文档。PDF文件的路径是和软件的根路径一样的。
def generatePDF(imgpath):
    doc = fitz.open()
    for img in sorted(glob.glob(imgpath + "*")):
        print("插入图片: " + img)
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)

    doc.save(str(getmsTime()) + ".pdf")

# 删除图片文件，只保留pdf。PDF生成成功了，还要缓存的干啥，删掉图片，顺便把缓存的文件夹也删掉。
def delete_imgs(imgpath):
    imgs = glob.glob(imgpath + "*")
    for img in imgs:
        os.remove(img)
        print(Fore.BLUE + "删除缓存 " + img)
    os.removedirs(imgpath)
    print("--------------------------------------")

# 最后不能忘记再写个作者，我 ^_^
def paint_author():
    about = """\n作者: Elliot Lee \n反馈：lsldragon@ouotlook.com"""
    print(Fore.BLACK + Back.WHITE + about)
    print(Style.RESET_ALL)

# 从漫画id获取，即微博头条文章
def get_from_id():
    print()
    value = input(Fore.YELLOW + "输入漫画id(微博网页头条文章): ")
    res = generate_img_urls(value)
    path = download_imgs(res)
    generatePDF(path)
    delete_imgs(path)
    print(Fore.RED + "生成pdf成功")
    paint_author()

# 从长图的url链接获取,url可从浏览器直接复制，省去了解析链接的麻烦
def get_from_longimg_url():
    print()
    value = input(Fore.YELLOW + "输入长图的url链接: ")
    # 因为download_imgs(value) 传入的value是一个列表，而输入的是一个字符串，所以要将字符转为列表
    path = download_imgs([value])
    generatePDF(path)
    delete_imgs(path)
    print(Fore.RED + "生成pdf成功")
    paint_author()

# 入口函数
if __name__ == "__main__":

    options = """选择:
    1. id模式,用将微博头条文章的图片转为PDF
    2. 长图模式,可将微博的长图链接转换为PDF
    -> """
    while True:
        try:
            value = input(options)
            if value == "1":
                get_from_id()
            elif value == "2":
                get_from_longimg_url()
            else:
                print(Fore.RED + "参数错误！")
                print(Style.RESET_ALL)
        except:
            print(Fore.RED + "失败！可是我也不太清楚问题出在哪里，请重试")
            print(Style.RESET_ALL)

print(Style.RESET_ALL)