from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc, options=chrome_options)


def test_website_is_opened():
    # 1. Visit https://useinsider.com/ and check Insider home page is opened or not
    driver.get("https://useinsider.com/")
    assert "Insider" in driver.title, "Title does not contain 'Insider'"


def test_company_careers_exist():
    # 2. Select “Company” menu in navigation bar, select “Careers” and check Career page,
    # its Locations, Teams and Life at Insider blocks are opened or not
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//nav//a[contains(text(),"Company")]'))
    )
    company_menu = driver.find_element(By.XPATH, '//nav//a[contains(text(),"Company")]')
    company_menu.click()
    careers_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Careers")]'))
    )
    careers_link.click()


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'career-our-location'))
    )


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'career-find-our-calling'))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//h2[contains(text(),"Life at Insider")]'))
    )


def test_qa_job_exist():
    # 3. Go to https://useinsider.com/careers/quality-assurance/, click “See all QA jobs”,
    # filter jobs by Location - Istanbul, Turkey and department - Quality Assurance,
    # check presence of jobs list
    driver.get("https://useinsider.com/careers/quality-assurance/")
    cookie_accept = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[contains(@id, "wt-cli-cookie-banner")]//a[contains(@id, "wt-cli-accept-all-btn")]'))
    )
    cookie_accept.click()

    see_all_qa_jobs_button = driver.find_element(By.XPATH, '//a[contains(text(),"See all QA jobs")]')
    see_all_qa_jobs_button.click()
    location_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//select[contains(@name,"location")]/following-sibling::span[1]'))
    )
    time.sleep(5)
    location_filter.click()

    location_filter_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[contains(@class,"select2-dropdown")]//ul//li[contains(text(), "Istanbul, Turkey")]'))
    )
    driver.execute_script("arguments[0].scrollIntoView();", location_filter_value)
    time.sleep(2)
    location_filter_value.click()

    department_filter = driver.find_element(By.XPATH,
                                            '//select[contains(@name,"filter-by-department")]/following-sibling::span[1]')
    time.sleep(2)
    department_filter.click()
    department_filter_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[contains(@class,"select2-dropdown")]//ul//li[contains(text(), "Quality Assurance")]'))
    )
    time.sleep(2)
    department_filter_value.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'career-position-list'))
    )


def test_qa_job_list_is_correct():
    # 4. Check that all jobs’ Position contains “Quality Assurance”, Department
    # contains “Quality Assurance”, Location contains “Istanbul, Turkey”
    time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[contains(@class, "position-list-item")]'))
    )
    job_cards = driver.find_elements(By.XPATH, '//div[contains(@class, "position-list-item")]')
    for job_card in job_cards:
        assert "Quality Assurance" in job_card.find_element(By.XPATH, '//p[contains(@class,"position-title")]').text
        assert "Quality Assurance" in job_card.find_element(By.CSS_SELECTOR, '.position-department').text
        assert "Istanbul, Turkey" in job_card.find_element(By.CSS_SELECTOR, '.position-location').text


def test_roles_exist():
    # 5. Click “View Role” button and check that this action redirects us to Lever
    # Application form page
    # Create an ActionChains object
    action = ActionChains(driver)
    view_role_cards = driver.find_elements(By.XPATH, '//div[contains(@class, "position-list-item")]')
    # Perform the hover action
    action.move_to_element(view_role_cards[0]).perform()

    view_role_button = driver.find_elements(By.XPATH, '//div[contains(@class, "position-list-item")]/a')[0]
    view_role_button.click()

    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 10).until(
        EC.url_contains("jobs.lever.co")
    )



