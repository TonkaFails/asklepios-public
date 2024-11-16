import os
import json
import logging
from tqdm import tqdm
from urllib.parse import urljoin
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
chrome_service = Service('/Users/timon/Downloads/chromedriver-mac-x64/chromedriver')  # Pfad zu deinem Chromedriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.headless = False  # Wenn du die Interaktionen sehen möchtest, setze das auf False

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
wait = WebDriverWait(driver, 30)  # Wait up to 20 seconds
logging.basicConfig(filename='webscrape_errors.log', level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Haupt-URL
main_url = "https://register.awmf.org/de/leitlinien/aktuelle-leitlinien"
driver.get(main_url)

# Schritt 1: Hole alle Elemente mit dem Tag-Namen 'ion-segment-button'
ion_buttons = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ion-segment-button')))

# Schritt 2: Suche unter diesen Elementen nach demjenigen, das ein 'ion-label'-Element enthält, dessen Text genau 'nach Fach' lautet
target_button = None
for button in ion_buttons:
    ion_label = button.find_element(By.TAG_NAME, 'ion-label')
    if ion_label.text.strip().lower() == 'nach fach':
        target_button = button
        break

if target_button:
    target_button.click()
    print("Button 'nach Fach' wurde erfolgreich geklickt.")
else:
    print("Button 'nach Fach' wurde nicht gefunden.")

# Warte, bis die neue Ansicht geladen ist
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'guideline-listing-title')))

guideline_fach_links = []
guideline_elements = driver.find_elements(By.CLASS_NAME, 'guideline-listing-title')

for guideline in guideline_elements:
    a_tag = guideline.find_element(By.TAG_NAME, 'a')
    if a_tag:
        subpage_url = a_tag.get_attribute('href')
        guideline_fach_links.append(subpage_url)

for guideline_fach_link in tqdm(guideline_fach_links[70:], desc="Processing aller Faecher"):
    driver.get(guideline_fach_link)
    
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'guideline-listing-title')))
    
    guideline_subpage_links = []
    main_fach_guidelines = driver.find_elements(By.TAG_NAME, 'ion-grid')[3]
    guideline_fach_subpage = main_fach_guidelines.find_elements(By.CLASS_NAME, 'guideline-listing-title')
    for guideline_subpage in guideline_fach_subpage:
        a_tag = guideline_subpage.find_element(By.TAG_NAME, 'a')
        if a_tag:
            subpage_url = a_tag.get_attribute('href')
            guideline_title = a_tag.text.strip()
            guideline_subpage_links.append(subpage_url)
    
    for guideline_subpage_link in guideline_subpage_links:
        try:
            driver.get(guideline_subpage_link)
            try:
                for i in range(3):
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ion-grid.search_result.search_result_compact.no-bottomline.document-list.md.hydrated')))
                    break
            except:
                logging.error(f'Could not load {guideline_subpage_link}')
            all_rows =  driver.find_elements(By.TAG_NAME, 'ion-row')

            links = {
                'Langfassung': None,
                'Kurzfassung': None,
                'Leitlinienreport': None,
                'Schluesselwoerter': None
            }
            for row in all_rows:
                first_column_text = row.find_element('css selector', 'ion-col:nth-child(1)').text
                second_column = row.find_element('css selector', 'ion-col:nth-child(2)')

                if 'langfassung' in first_column_text.lower():
                    a_tag = second_column.find_element('css selector', 'a')
                    href = a_tag.get_attribute('href')
                    links['Langfassung'] = href
                elif 'kurzfassung' in first_column_text.lower():
                    a_tag = second_column.find_element('css selector', 'a')
                    href = a_tag.get_attribute('href')
                    links['Kurzfassung'] = href
                elif 'leitlinienreport' in first_column_text.lower():
                    a_tag = second_column.find_element('css selector', 'a')
                    href = a_tag.get_attribute('href')
                    links['Leitlinienreport'] = href
                elif 'schl' in first_column_text.lower() and 'sselw' in first_column_text.lower() and 'rter' in first_column_text.lower():
                    links['Schluesselwoerter'] = second_column.text


            guideline_subpage_title = driver.find_elements(By.TAG_NAME, 'h1')
            folder_name = f'Leitlinien/{guideline_subpage_title[0].text.strip()}'

            if not os.path.exists('Leitlinien'):
                os.makedirs('Leitlinien')
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            if links['Langfassung']:
                langfassung_path = os.path.join(folder_name, 'Langfassung.pdf')
                urlretrieve(links['Langfassung'], langfassung_path)
            if links['Kurzfassung']:
                kurzfassung_path = os.path.join(folder_name, 'Kurzfassung.pdf')
                urlretrieve(links['Kurzfassung'], kurzfassung_path)
            if links['Leitlinienreport']:
                leitlinienreport_path = os.path.join(folder_name, 'Leitlinienreport.pdf')
                urlretrieve(links['Leitlinienreport'], leitlinienreport_path)
            if links['Schluesselwoerter']:
                words_list = links['Schluesselwoerter'].split(', ')
                words_dict = {'Schluesselwoerter': words_list}
                schluesselwoerter_path = os.path.join(folder_name, 'schluesselwoerter.json')
                with open(schluesselwoerter_path, 'w') as json_file:
                    json.dump(words_dict, json_file, ensure_ascii=False, indent=4)
        except Exception as ex:
            logging.exception(f'Exception for {guideline_subpage_link}\n {ex}')

# Beende den Browser
driver.quit()
