import eel
import search

#app_name="html"
#end_point="index.html"
#size=(700,600)

# eel関数の定義(search.pyに定義している鬼滅キャラ検索関数を呼び出す関数)
@eel.expose
def search_item(max,word):
    search.search_item(max,word)

# index.htmlをウィンドウで表示
eel.init("html")
eel.start("index.html")