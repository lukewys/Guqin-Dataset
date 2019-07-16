# 古琴数据集

古琴数据集是一个包含古琴曲的符号化音乐数据集。古琴数据集中的古琴谱由我们收集的近年出版的带有简谱的琴谱转录而成。转录的内容为简谱中的旋律与泛音标记，忽略了其他表情记号。

## 文件格式

## 内容

[Guqin_Dataset_v1](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1 "Guqin_Dataset_v1")：古琴数据集

        [xml](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1/xml "xml")：MusicXML格式的古琴曲，每段为单独的一个文件，以“琴曲名-下划线-段落编号”形式的文件名储存。其中泛音记号以跳音记号（实心圆点）表示。
        [xml_no_split](https://github.com/lukewys/Guqin-Dataset/tree/master/Guqin_Dataset_v1/xml_no_split "xml_no_split")：MusicXML格式的古琴曲，每个琴曲为一个文件。其中泛音记号以跳音记号（实心圆点）表示。
        [reference.csv](https://github.com/lukewys/Guqin-Dataset/blob/master/Guqin_Dataset_v1/reference.csv "reference.csv")：琴谱的元信息标注，包含曲谱名称、定弦、琴谱来源、琴曲来源、演奏者与打谱或记谱者的信息。

## 制作

我们使用了一种特殊的快速录入文本标记以录入琴谱，录入一页的时间可缩短至3-5分钟。我们之后使用程序将古琴曲转换至MusicXML格式，并自动生成了拍号。

## 致谢

特别感谢参与古琴数据集建设的同学：张子谦、许阳、苗天辰、张逸嘉。
