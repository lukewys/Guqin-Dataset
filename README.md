
# Guqin Dataset
Guqin dataset is a symbolic music dataset containing music from [Guqin](https://en.wikipedia.org/wiki/Guqin), an ancient Chinese pluck instrument. The scores in Guqin dataset are collected from Guqin collection that formated in [reduced notation](https://en.wikipedia.org/wiki/Guqin_notation) with [numbered notation](https://en.wikipedia.org/wiki/Numbered_musical_notation) published in recent years. The numbered notation in the score are then transcripted and converted into MusicXML files (.xml). The content transcripted are melody and overtone notation in numbered notation, with other notation ignored.

## Content
[Guqin_Dataset_v1](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1 "Guqin_Dataset_v1")：Guqin dataset

*[xml](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1/xml "xml")：Guqin music in MusicXML format with each phrase (or paragraph) as an individual file. The file name is format in "score-name_phrase".

*[xml_no_split](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1/xml_no_split "xml_no_split")：Guqin music in MusicXML format with each piece as an individual file.

*[reference.csv](https://github.com/lukewys/Guqin-Dataset/blob/master/Guqin_Dataset_v1/reference.csv "reference.csv")：The metadata of Guqin score in dataset, including score name, tuning, reference, original reference, performer, the recording or organizing person of the score.
        
 ## Format

MusicXML file contains melody in numbered notation and overtone notation. The overtone notation is presented in staccato (in black solid dot).  In MusicXML files, the title of the file is the same as the file name, and the time signature is included.

## Construction

A fast transcription text format is used to transcript Guqin score, reducing the time transcribing a page to 3-5 minutes. A program is then used to automatically convert the text format to MusicXML files, with time signature automatically generated.

## Thanks

Special thanks to students who contribute to Guqin dataset：张子谦、许阳、苗天辰、张逸嘉。

# 古琴数据集

古琴数据集是一个包含古琴曲的符号化音乐数据集。古琴数据集中的古琴谱由我们收集的近年出版的带有简谱的琴谱转录而成。转录的内容为简谱中的旋律与泛音标记，忽略了其他表情记号。古琴数据集中的文件数据格式为MusicXML（.xml）。


## 内容

[Guqin_Dataset_v1](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1 "Guqin_Dataset_v1")：古琴数据集

*[xml](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1/xml "xml")：MusicXML格式的古琴曲，每段为单独的一个文件，以“琴曲名_段落编号”形式的文件名储存。

*[xml_no_split](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1/xml_no_split "xml_no_split")：MusicXML格式的古琴曲，每个琴曲为一个文件。

*[reference.csv](https://github.com/lukewys/Guqin-Dataset/blob/master/Guqin_Dataset_v1/reference.csv "reference.csv")：琴谱的元信息标注，包含曲谱名称、定弦、琴谱来源、琴曲来源、演奏者与打谱或记谱者的信息。

## 文件格式

MusicXML文件包含琴谱的简谱中的旋律与泛音标记。泛音标记使用跳音记号（黑色圆点）表示。MusicXML文件中曲名为文件名，并标明了拍号。

## 制作

我们使用了一种特殊的快速录入文本标记以录入琴谱，录入一页的时间可缩短至3-5分钟。我们之后使用程序将古琴曲转换至MusicXML格式，并自动生成了拍号。

## 致谢

特别感谢参与古琴数据集建设的同学：张子谦、许阳、苗天辰、张逸嘉。

