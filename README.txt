作者：宋军帅
时间：2016-01-11

数据集：DBpedia 2014
描述：Unknown action "a"Extended Abstracts，ttl格式
网址：http://oldwiki.dbpedia.org/Downloads2014

1. Ubuntu服务器67
    建立solr索引，版本6.3.0
    参考解压目录/example/README.txt(techproducts)

2. 处理文件
（1）原始数据量太大，减少数据量
    entity_link.py
    由long_abstracts_en.ttl获得data.in，共33361条数据
（2）处理数据data.in，正则，获取data.seg（LDA输入训练主题文件）
    seg.py
（3）使用C++处理data.in，获得title + link文件，共33361条数据（这里只运行main中第一个函数）
    entity_link_title.cpp
    获得title_link.dat文件，例如：Graph http://.......
（4）整理LDA输入文件data.seg
    remove_others.py
    去掉那些不是[a~zA~Z0-9_]的文件字符
    check_content.py
    检查是否有某一行为空行（LDA训练前排错）
（5）统一取data.seg文件与title_link.dat文件的前2W行，作为小样本，进行Demo演示(split -l 20000 data.in)
    data.seg -> data_2W.seg
    title_link.dat -> title_link_2W.dat

3. 使用LDA进行主题提取: 使用data_2W.seg进行主题训练（2W样本，1000轮迭代训练时间为80min左右）
    src/lda -est -alpha 0.5 -beta 0.1 -ntopics 50 -niters 1000 -savestep 500 -twords 20 -dfile models/entity/data_2W.seg
    主题50个，a=0.5,b=0.1，采样1000轮，获得如下两个文件：
    （1）model-final.tassign & wordmap.txt（每个单词与id映射关系）
        每个单词采样的主题，用此文件统计每个单词的主题分布
    （2）model-final.theta
        每个entity主题分布
   注意：上述data_2W.set文件路径

4. 合并2.(3)的数据文件 & 3的两个结果文件，运行entity_final() & word_final()函数
    Xcode中C++项目：entity_link_title
    （1）对于entity，生成entity.final
        生成entity link topic格式文件，例如： Graph http://.../Graph 0.2 0.01 0.1 ...
    （2）对于word，生成word.final
        生成word topic格式文件，例如 play 0 0 4 0 2 ...
        （后面记录的是在50个主题上的分别出现的次数，较为稀疏，也可以换编码格式）
    结果：生成entiity.final & word.final

5. 将生成的的entity.final & word.final文件在solr上构建索引    
    程序文件：solr_build.py
    数据：entity.final & word.final
    将程序文件 & 数据文件（entity.final & word.final）传到服务器上，进行传输
    
    测试索引是否构建成功：solr_test.py

6. 搭建前端Chrome插件
    （1）67服务器上搭建CGI服务器
    （2）前端插件发送GET请求到67，67请求93上的solr索引返回数据处理后给前端
        发送数据：查询文本
        67上处理：计算到文本主题分布（访问每个单词的主题分布）
                设计一种不重不漏地解决冲突的策略，来获取不同entity的主题分布
                （没有冲突就算了，有冲突需要使用主题分布来确定一个）
		CGI文件：search.pl
        返回数据：返回确定下来的每一个entity + 对应超链接link
    （3）前端插件：speak_selection

    补充：Chrome插件：speak_selection
        核心js代码在 popup.js 与 send_links.js 中。发送与接收消息，以及界面显示

