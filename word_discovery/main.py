# coding=utf-8
import pandas as pd

from dawndevil.utils.ioutils import read_file_as_string
from dawndevil.word_discovery.word_discovery import WordDiscovery


def print_array(objs):
    for key in objs:
        print(key, objs[key])


def print_object_array(objs):
    for v in objs:
        for key in v:
            print(key, v[key])


w = WordDiscovery()
w.set_dict(
    symbol="../resource/symbol.txt",
    stop_words="../resource/stop_words.txt"
)
w.set_threshold(15, 0.6, 0.6)
w.append(read_file_as_string("article.txt"))
data = w.run()
if len(data) > 0:
    df = pd.DataFrame(data)
    df = df.sort_values(by=["mi", "le", "re"], ascending=False)
    df.to_csv("result.csv", columns=["word", "mi", "le", "re"], encoding="utf8", index=False)
    print(df)