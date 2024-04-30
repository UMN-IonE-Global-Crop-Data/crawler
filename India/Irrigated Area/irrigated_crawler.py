from selenium import webdriver
from selenium.webdriver.common.by import By
import time




# i-index we don't need the first one(which is "Select State")
i = 2
while i <= 21:
    wb = webdriver.Chrome()
    wb.implicitly_wait(10)

    wb.get("https://aps.dac.gov.in/LUS/Public/Reports.aspx")
    time.sleep(2)
    # select the desired state
    wb.find_element(By.XPATH, f"//select[@name = 'DdlState']/option[{i}]").click()
    time.sleep(2)

    # select format
    wb.find_element(By.XPATH, "//select[@name = 'DdlFormat']/option[2]").click()
    
    # crawl years
    years = wb.find_elements(By.XPATH, "//select[@name = 'DdlYear']/option")
    state = wb.find_element(By.XPATH, f"//select[@name = 'DdlState']/option[{i}]").text
    print(f"{i} {state}")
    j = 2
    while j < len(years):
        # select the desired state
        # wb.find_element(By.XPATH, f"//select[@name = 'DdlState']/option[{i}]").click()
        # time.sleep(3)

        # select the desired year
        wb.find_element(By.XPATH, f"//select[@name = 'DdlYear']/option[{j}]").click()
        
        wb.find_element(By.XPATH, "//*[@id='TreeView1t3']").click()
        # check if there is an alert
        try:
            alert = wb.switch_to.alert
            alert.accept()
            wb.quit()
            time.sleep(2)
            wb = webdriver.Chrome()
            wb.implicitly_wait(10)
            wb.get("https://aps.dac.gov.in/LUS/Public/Reports.aspx")
            time.sleep(2)
            # select the desired state
            wb.find_element(By.XPATH, f"//select[@name = 'DdlState']/option[{i}]").click()
            time.sleep(2)

            # select format
            wb.find_element(By.XPATH, "//select[@name = 'DdlFormat']/option[2]").click()
        except:
            time.sleep(2)
        j += 1
    wb.quit()
    i += 1


