from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

start_scrape = time.time()

driver = webdriver.Chrome(r'C:\Users\tdbui\Desktop\chromedriver_win32\chromedriver.exe')
driver.get('https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y=2021&sbd=')

id_city = [str(i).zfill(2) for i in range(1, 65)]
id_default = [str(i).zfill(6) for i in range(1, 100000)]
id_students = []
        
scores = []
early_stoppings = 0
for i in id_city:
    for z in id_default:
        if early_stoppings == 15:
            break
        else:
            id_student = i+z
            id_students.append(id_students)
            url = 'https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y=2021&sbd=' + id_student
            driver.get(url)
            
            student_score = driver.find_elements_by_css_selector('div.search-result-line')
            temp = []
            for j in student_score:
                temp.append(j.text)
            scores.append(temp)
            if len(temp) == 0:
                early_stoppings += 1
            else:
                early_stoppings = 0
driver.close()

end_scrape = time.time()
t = end_scrape-start_scrape
print('Thời gian scrape: {} giờ {} phút {} giây'.format(
    int(t//3600), int((t-t//3600*3600)//60), int((t-t//3600*3600)%60))
)

def get_scores(scores, obj_name):
    obj = []
    for i in scores:
        getted = False
        for j in i:
            if obj_name in j:
                obj.append(j.split('\n')[-1])
                getted = True
        if getted == False:
            obj.append(None)
    return obj

start_xuly = time.time()

toan = get_scores(scores, 'Toán')
van = get_scores(scores, 'Văn')
su = get_scores(scores, 'Sử')
dia = get_scores(scores, 'Địa')
n1 = get_scores(scores, 'Ngoại ngữ (N1)')
n2 = get_scores(scores, 'Ngoại ngữ (N2)')
n3 = get_scores(scores, 'Ngoại ngữ (N3)')
n4 = get_scores(scores, 'Ngoại ngữ (N4)')
n5 = get_scores(scores, 'Ngoại ngữ (N5)')
n6 = get_scores(scores, 'Ngoại ngữ (N6)')
li = get_scores(scores, 'Lí')
hoa = get_scores(scores, 'Hóa')
sinh = get_scores(scores, 'Sinh')
gdcd = get_scores(scores, 'GDCD')

end_xuly = time.time()
t = end_xuly-start_xuly
print('Thời gian xử lý: {} giờ {} phút {} giây'.format(
    int(t//3600), int((t-t//3600*3600)//60), int((t-t//3600*3600)%60))
)

final_scores = pd.DataFrame({'Toán': toan,
	      'Văn': van,
	      'Sử': su,
	      'Địa': dia,
	      'N1': n1,
	      'N2': n2,
	      'N3': n3,
	      'N4': n4,
	      'N5': n5,
	      'N6': n6,
	      'Lí': li,
	      'Hóa': hoa,
	      'Sinh': sinh,
	      'GDCD': gdcd})

final_scores.to_csv('final_score.csv', index=False)
