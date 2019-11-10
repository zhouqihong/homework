# 该文件主要设置file path，统一在这里进行修改
# 使用方法：在其他文件中导入
#
import os
import platform
from pathlib import Path

# 获取系统的信息
sysstr = platform.system()
if (sysstr == "Windows"):
    print("Call Windows tasks")
    # 需要设置windows的配置路径
    sys_path = Path(r'C:/AI-NLP/NewsInfo-Auto-Extration')
    # ltp模型目录的路径
    LTP_DATA_DIR = Path(r'C:/AI-NLP/NewsInfo-Auto-Extration/data/ltp_data_v3.4.0')
elif (sysstr == "Linux"):
    print("Call Linux tasks")
    # 需要设置linux的配置路径
    sys_path = Path(r'/home/student/project/project-01/kill_bug_team/NewsInfo-Auto-Extration')
    # ltp模型目录的路径
    LTP_DATA_DIR = Path(r'/home/student/project/project-01/kill_bug_team/NewsInfo-Auto-Extration/data/ltp_data_v3.4.0')
else:
    print("Other System tasks")

# 读取/保存文本的路径
path_news_sentences_xut_txt = sys_path / r'data/news-sentences-xut.txt'
path_news_txt = sys_path / r'data/news.txt'
path_news_model = sys_path / r'data/news_model'

# said的路径
said_path = sys_path / r'similar_said'

# 初始化路径

# 分词模型路径，模型名称为`cws.model`
cws_model_path = LTP_DATA_DIR / r'cws.model'
# 词性标注模型路径，模型名称为`pos.model`
pos_model_path = LTP_DATA_DIR / r'pos.model'
# 命名实体识别模型路径，模型名称为`pos.model`
ner_model_path = LTP_DATA_DIR / r'ner.model'
# 依存句法分析模型路径，模型名称为`parser.model`
par_model_path = LTP_DATA_DIR / r'parser.model'
# 语义角色标注模型目录路径，模型目录为`srl`
srl_model_path = LTP_DATA_DIR / r'pisrl.model'
