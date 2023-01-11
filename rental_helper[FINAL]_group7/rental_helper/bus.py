from selenium import webdriver
import pandas as pd

def create_bus_csv():

    # open chromedriver
    PATH = 'driver/chromedriver'
    driver = webdriver.Chrome(PATH)

    # website source
    driver.get("https://www.adelaidemetro.com.au/plan-a-trip/timetables")


    routeNumber_column = []
    name_column = []
    description_column = []
    url_column = []
    # only to display bus detail info
    driver.find_element_by_xpath("""//*[contains(@title, "Show only 'Bus'")]""").click()
    x = 0
    # automatically jump to next page (there are twenty pages in total)
    while (x < 20):
        result_name = driver.find_elements_by_class_name("result-name")
        result_description = driver.find_elements_by_class_name("result-description")
        result_url = driver.find_elements_by_xpath("""//*[contains(@class, "route-link")]""")

        for name in result_name:
            textLine = name.text
            routeNumber_column.append(textLine)


        for description in result_description:
            description_column.append(description.text)


        for l in result_url:
            url_column.append(l.get_attribute('href'))

        # jump to next page
        if x != 19:
            driver.find_element_by_xpath("""//*[contains(@rel, "next")]""").click()

        x += 1


    driver.close()


    # convert lists to a dataframe and store it to a csv file
    data = pd.DataFrame({'route-number' : routeNumber_column, 'description' : description_column, 'url' : url_column },
                    columns=['route-number','description', 'url'])
    data.to_csv("backupcsv\bus_info.csv")









