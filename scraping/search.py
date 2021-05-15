import os
from selenium import webdriver
from selenium.webdriver import Chrome,ChromeOptions
import time
import pandas as pd
import csv
import eel
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



def search_company(word):
    
#変数宣言
    search_keyword = word
    LOG_FILE_PATH = './log_file.log'   #ログファイルパス
    CSV_FILE = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\')+'result_{}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

#ログ出力関数
    def log(txt):
        with open(LOG_FILE_PATH,'a',encoding="utf-8-sig") as f:
            f.write(txt)


    def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
        for th_elm,td_elm in zip(th_elms,td_elms):
            if th_elm.text == target:
                return td_elm.text

    
#メイン処理

# クローム起動    
    def main():
        log("処理開始")
        log("キーワード:"+search_keyword+"で検索")
        eel.view_log_js("キーワード:「{}」で検索を開始します。".format(search_keyword))

        #options = Options()
        #options.add_argument('--headless')        
        driver = webdriver.Chrome("C:\\Users\Kanomata\Desktop\chromedriver.exe")#, chrome_options=options
        driver.get("https://tenshoku.mynavi.jp/")
        time.sleep(5)

    #ポップアップを閉じる
        try:
            driver.execute_script('document.querySelector(".karte-close").click()')
            time.sleep(5)
            driver.execute_script('document.querySelector(".karte-close").click()')
        except:
            pass

# キーワード検索
        search_form = driver.find_element_by_class_name("topSearch__text")
        search_form.send_keys(search_keyword)
        search_btn=driver.find_element_by_class_name("topSearch__button")
        search_btn.click()

# 変数宣言
        company_name_null_list = []
        sell_point_null_list = []
        employee_status_null_list = []
        pay_null_list = []
        i=1
        count=1
        success=1
        fail=0

        while True:
    #検索ワードでヒットした募集の会社名、セールスポイント、就業ステータス、給料を抽出
            company_name_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__name")
            sell_point_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__copy")
            employee_status_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .labelEmploymentStatus")
            pay_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")
    
            for company_name, sell_point, employee_status, pay in zip(company_name_list,sell_point_list,employee_status_list,pay_list):        
                try:
                    company_name_null_list.append(company_name.text)
                    sell_point_null_list.append(sell_point.text)
                    employee_status_null_list.append(employee_status.text)
                    first_year_pay = find_table_target_word(pay.find_elements_by_tag_name("th"), pay.find_elements_by_tag_name("td"), "初年度年収")
                    pay_null_list.append(first_year_pay)
                    #log(f"{count}件目成功 : {name.text}")
                    #pay_null_list.append(pay.text)
                    log("抽出成功("+str(success)+"/"+str(count)+"回目)")
                    print("抽出成功("+str(success)+"/"+str(count)+"回目)")
                    success=success+1

                except Exception as e:
                    fail=fail+1
                    log("抽出失敗("+str(fail)+"/"+str(count)+"回目)")
                    log(e)
                    print("抽出失敗("+str(fail)+"/"+str(count)+"回目)")
                    
                finally:
                    count=count+1     
        
            search_next = driver.find_elements_by_class_name("iconFont--arrowLeft")

        #「次のページ」ボタンが一ページに二つあれば次のページへ、なければ終了
            if len(search_next) == 2:
                next_page_link = search_next[0].get_attribute("href")
                driver.get(next_page_link)
                print(i,"ページ目終了")
                i=i+1
                time.sleep(5)
            else:
                print("全ページ終了")
                log("抽出処理終了")
                eel.view_log_js("検索が完了しました")
                eel.view_log_js("-------------------------")
                eel.view_log_js("成功："+str(success)+"/"+str(count))
                eel.view_log_js("失敗："+str(fail)+"/"+str(count))
                eel.view_log_js("CSVファイル：{}".format(CSV_FILE))
                break

#csv出力
        df = pd.DataFrame({
            "企業名":company_name_null_list,
            "セールスポイント":sell_point_null_list,
            "採用ステータス":employee_status_null_list,
            "初年度年収":pay_null_list,
            })
        
        df.to_csv(CSV_FILE,encoding="utf-8-sig")

    main()