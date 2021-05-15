import eel
import search

@eel.expose
def search_company(word):
    search.search_company(word)

eel.init("html")
eel.start("index.html")