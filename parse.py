import os, re, json, binascii

def parseMeta(root):
    with open(filename,'r',encoding='utf-8',errors='ignore') as f:
        content = f.read()
        topic_id = readMetaAttr("topic_id", content)
        word_level_id = readMetaAttr("word_level_id", content)
        tag_id = readMetaAttr("tag_id", content)
        word = readMetaAttrWord("word", content)
        word_audio = readMetaAttr("word_audio", content)
        image_file = readMetaAttr("image_file", content)
        accent = readMetaAttr("accent", content)
        mean_cn = readMetaAttr("mean_cn", content)
        mean_en = readMetaAttr("mean_en", content)
        sentence_phrase = readMetaAttr("sentence_phrase", content)
        deformation_img = readMetaAttr("deformation_img", content)
        sentence = readMetaAttr("sentence", content)
        sentence_trans = readMetaAttr("sentence_trans", content)
        sentence_audio = readMetaAttr("sentence_audio", content)
        cloze_data = readMetaAttr("cloze_data", content)
        cloze = readMetaAttr("cloze", content)
        options = readMetaAttr("options", content)
        tips = readMetaAttr("tips", content)
        word_etyma = readMetaAttr("word_etyma", content)
        d = {"topic_id":topic_id, "word_level_id":word_level_id, "tag_id": tag_id, "word": word, "word_audio": word_audio, "image_file":image_file, "accent":accent, "mean_cn":mean_cn, "mean_en":mean_en, "sentence_phrase":sentence_phrase, "deformation_img":deformation_img, "sentence":sentence, "sentence_trans":sentence_trans, "sentence_audio":sentence_audio, "cloze_data": cloze_data, "cloze":cloze, "options":options, "tips":tips, "word_etyma":word_etyma}
        word = word.replace('"', '')
        print(filename)
        os.makedirs(root + 'project_output/' + word + '/', exist_ok=True)
        with open(root + 'project_output/' + word + '/data.txt', 'w', encoding = 'utf-8') as f:
            f.write(content)
        with open(root + 'project_output/' + word + '/word.json', 'w', encoding = 'utf-8') as f:
            json.dump(d, f, ensure_ascii = False)
        return word

def parseMP3(data):
    try:
        # res = re.findall("ff e3 20 c4.*aa aa", data)
        res = re.findall("49 44 33.*aa aa", data)
        with open(savePath + "audio.mp3", 'wb') as bmp_file:
            bmp_file.write(bytearray.fromhex(res))
    except:
        print("未解析出mp3")
        return "Error"

def parseAAC(data):
    try:
        res = re.findall("ff f1 5c 40.*00 07", data)[0]
        with open(savePath + "audio.aac", 'wb') as bmp_file:
            bmp_file.write(bytearray.fromhex(res)) 
    except:
        print("未解析出aac")
        return "Error"

def parseJPG(data, name):
    try:
        res = re.findall("ff d8 ff.*ff d9",data)[0]
        with open(savePath + name, 'wb') as bmp_file:
            bmp_file.write(bytearray.fromhex(res))
    except:
        print("未解析出jpg")
        return "Error"

def parsePNG(data, name):
    try:
        res = re.findall("89 50 4e 47.*ae 42 60 82",data)[0]
        with open(savePath + name, 'wb') as bmp_file:
            bmp_file.write(bytearray.fromhex(res))
    except:
        print("未解析出png")
        return "Error"

def parseFileList(data):
    reverseData = data[::-1]
    res = re.findall('a0 (.*?) 00 00 00 00 00 00', reverseData)
    if len(res)>0:
        res = res[0][::-1]
        filelist = hex2chr(res)
        print('文件列表处理完成')
        return {"list": filelist, "data": data.replace(res, '')}
    else:
        return False

def hex2chr(data):
    res = ''.join(list(map(chr, map(int16, data.split(' ')))))
    return res

def int16(num):
    return int(num, 16)

def readZpk():
    with open(filename, 'rb') as f:
        a=f.read()
        b2a_hex = binascii.b2a_hex(a)
        b2a_hex_str = str(b2a_hex, encoding = "utf-8")
        alist = []
        for i in range(0, len(b2a_hex_str), 2):
            alist.append(b2a_hex_str[i:i+2])
        b2a_hex_str = ' '.join(alist)
        return b2a_hex_str

def readMetaAttr(name, content):
    res = re.findall('\"' + name + '\":(.*?),', content)
    if len(res) > 0:
        attr = res[0]
        if attr[0] == '"' and attr[-1] == '"':
            attr = attr[1:-1]
        return attr
    else:
        return ''

def readMetaAttrWord(name, content):
    res = re.findall('\"' + name + '\":(.*?)}', content)
    if len(res) > 0:
        attr = res[0]
        if attr[0] == '"' and attr[-1] == '"':
            attr = attr[1:-1]
        return attr
    else:
        return ''

def write():
    data = ''
    with open("img.mp3", 'wb') as bmp_file:
        bmp_file.write(bytearray.fromhex(data))

if __name__ == "__main__":
    for root, dirs, files in os.walk('./'):
        if root != './':
            root += '/'
            os.makedirs(root + 'project_output/', exist_ok=True)
            for file in os.listdir(root):
                if ".zpk" in file:
                    filename = root + file
                    data = readZpk()
                    word = parseMeta(root)
                    savePath = root + 'project_output/' + word + '/'
                    fileList = parseFileList(data)
                    newFileList = []
                    for i in fileList['list'].split('\n'):
                        info =  i.split('.')
                        name =info[0]
                        ext = str.lower(info[1] if len(info) > 1 else "")
                        if ext == 'jpg' or ext == 'jpeg':
                            parseJPG(data, i)
                        elif ext == 'png':
                            parsePNG(data, i)
                        else:
                            continue
                # parseAAC(data)
                # parseMP3(data)
                # parseJPG(data)
                # parsePNG(data)
