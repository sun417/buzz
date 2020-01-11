#-*-coding:utf-8-*-
import csv
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
def makeImg(row):
    print(row)
    img = Image.open("zhengshu.jpg")
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    #编号
    font = ImageFont.truetype("方正黑体简体_2.TTF", 90)
    draw.text((3090, 1235), row[0], font=font, fill = (0, 0, 0, 255))
    #获奖论文
    if len(row[4]) > 30 :
        row[4] = row[4][:26] + "\n" + row[4][26:]
    font = ImageFont.truetype("STSONG.TTF", 108)
    draw.text((1290, 1550), row[4], font=font, fill = (0, 0, 0, 255))
    #作者
    author = row[1]
    if row[5] != '':
        author += ' ' + row[5]
    # if row[6] != '':
    #     author += ' ' + row[6] + '&'
    draw.text((1290, 1820), author, font=font, fill = (0, 0, 0, 255))
    #获奖级别    
    font = ImageFont.truetype("FZDHTJW.TTF", 108)
    draw.text((1290, 2095), row[2], font=font, fill = (29, 32, 136, 255))
    #第一作者单位
    # if len(row[3]) > 30 && row[3].find(' ',15) != -1:
    #     row[3]
    font = ImageFont.truetype("STSONG.TTF", 108)
    draw.text((1290, 2357), row[3], font=font, fill = (0, 0, 0, 255))

    filename = 'images/' + row[1] + ' ' + row[3].replace('/', '').replace('\n', '') + '.jpg'
    img.save(filename, "JPEG", quality = 100)
    #缩略图
    # img.thumbnail((500, 348))
    # filename = 'images/thumbnail/' + row[1] + ' ' + row[3].replace('/', '') + '.jpg'
    # img.save(filename, "JPEG", quality = 100)
    img.close()


def main():
    with open('优秀论文.csv')as f: 
        f_csv = csv.reader(f)
        for row in f_csv:
            for i in range(len(row)):
               row[i] = row[i].replace('\\n', '\n')
            makeImg(row)

if __name__ == '__main__':
    main()