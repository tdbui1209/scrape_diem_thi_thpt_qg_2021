from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

start_scrape = time.time()

driver = webdriver.Chrome(r'C:\Users\tdbui\Desktop\chromedriver_win32\chromedriver.exe')
driver.get('https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y=2021&sbd=')

id_city = [str(i).zfill(2) for i in range(1, 65)]
id_default = [str(i).zfill(6) for i in range(1, 999999)]
id_students = []
        
early_stoppings = 0
for i in id_city:
    for j in id_default:
        if early_stoppings == 15:
            early_stoppings = 0
            break
        else:
            id_student = i+j
            id_students.append(id_student)
            url = 'https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y=2021&sbd=' + id_student
            driver.get(url)
            
            student_score = driver.find_elements_by_css_selector('div.search-result-line')
            temp = [''] * 15
            temp[0] = id_student
            for div in student_score:
                z = div.text.split('\n')
                if 'Toán' in z:
                    temp[1] = z[-1]
                elif 'Lí' in z:
                    temp[2] = z[-1]
                elif 'Hóa' in z:
                    temp[3] = z[-1]
                elif 'Sinh' in z:
                    temp[4] = z[-1]
                elif 'Sử' in z:
                    temp[5] = z[-1]
                elif 'Địa' in z:
                    temp[6] = z[-1]
                elif 'Văn' in z:
                    temp[7] = z[-1]
                elif 'GDCD' in z:
                    temp[8] = z[-1]
                elif 'Ngoại ngữ (N1)' in z:
                    temp[9] = z[-1]
                elif 'Ngoại ngữ (N2)' in z:
                    temp[10] = z[-1]
                elif 'Ngoại ngữ (N3)' in z:
                    temp[11] = z[-1]
                elif 'Ngoại ngữ (N4)' in z:
                    temp[12] = z[-1]
                elif 'Ngoại ngữ (N5)' in z:
                    temp[13] = z[-1]
                elif 'Ngoại ngữ (N6)' in z:
                    temp[14] = z[-1]
                else:
                    continue
            score = ','.join(temp)
            if temp[1:] == ['']*14:
                early_stoppings += 1
                continue
            else:
                early_stoppings = 0
            with open('diem_2021.csv', encoding='utf-8', mode='a') as file:
                file.write(score+'\n')
driver.close()

end_scrape = time.time()
t = end_scrape-start_scrape
print('Thời gian scrape: {} giờ {} phút {} giây'.format(
    int(t//3600), int((t-t//3600*3600)//60), int((t-t//3600*3600)%60))
)
