def get_webdriver():
    """Simply starts a new Chrome browser instance"""
    #Load .env file contents
    load_dotenv()

    chromedriver = os.environ.get('webdriver_loc')           #  path to the chromedriver executable
    os.environ["webdriver.chrome.driver"] = chromedriver
#   Define optional settings and go to the website
    chrome_options = ChromeOptions()

#     options.add_argument("--headless")
#     options.add_argument("--disable-notifications")
#     driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options, options=options)

    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
    return driver

def login_google(driver):
    """In order to avoid reCAPTCHA's I need to first log in to my google account.
    This function does just that"""
    #Load .env file contents
    load_dotenv()
    google_url = os.environ.get('google_url')

    driver.get(google_url)
    time.sleep(1)

    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "identifierId")))

    username_field = driver.find_element_by_id('identifierId')
    username_field.send_keys(os.environ.get('username'))
    username_field.send_keys(Keys.RETURN)
    time.sleep(1)
    password_field = driver.find_element_by_name('password')
    password_field.send_keys(os.environ.get('secret_g'))
    password_field.send_keys(Keys.RETURN)
    return driver


def solve_recaptcha():
    """Click reCAPTCHA checkbox. If the test with images comes up, I have no solution."""
    frame = driver.find_element_by_xpath('//iframe[contains(@src, "recaptcha")]')
    driver.switch_to.frame(frame)
    driver.find_element_by_xpath("//*[@id='recaptcha-anchor']").click()
    time.sleep(3)
    driver.switch_to.default_content()
    try:
        frame = driver.find_element_by_xpath('//iframe[contains(@src, "recaptcha")]')
        driver.switch_to.frame(frame)
        print('Human intervention needed')
        return 'Human intervention needed'
    except:
        print('ReCAPTHA solved successfully')
        return 'ReCAPTHA solved successfully'


def set_cookies():
    """This function sets the minimal cookie settings and takes us to the filters page"""
    cookie_url = funda_url + '/cookiebeleid/?ReturnUrl=%2f'
    driver.get(cookie_url)

    element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Aangepast')]")))
    element.click()

    cookie_box = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='cookie-preference-aangepast']")))
    save_cookies = cookie_box.find_element_by_xpath(".//button[contains(text(), 'Cookievoorkeuren opslaan')]")
    save_cookies.click()



def open_funda(driver):
    """This function simply starts the chrome driver (from a defined location on the machine)."""
#     Load .env file contents
    load_dotenv()
    funda_url = os.environ.get('funda_url')

    time.sleep(2)
    driver.get(funda_url)

    try:
        set_cookies()
        current_selection = driver.find_element_by_class_name('is-active').text
        # Makes sure that "For Sale" category is selected
        if current_selection == 'For Sale':
            return driver
        else:
            driver.get(funda_url+'koop/')
            return driver
    except:
        recaptcha_msg = solve_recaptcha()
        if recaptcha_msg == 'ReCAPTHA solved successfully':
            set_cookies()
            current_selection = driver.find_element_by_class_name('is-active').text
            # Makes sure that "For Sale" category is selected
            if current_selection == 'For Sale':
                return driver
            else:
                driver.get(funda_url+'koop/')
                return driver
        else:
            print('Could not solve reCAPTCHA :(')
            return driver


def log_in():
    """Uses the credentials defined in the .env file to log in and saves properties matching desired criteria to the favourites"""
    # This is to load environment variables
    load_dotenv()

    login_url = os.environ.get('login_url')
    url = os.environ.get('funda_url')

    driver.get(login_url)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "Username")))

    username_field = driver.find_element_by_id('Username')
    username_field.send_keys(os.environ.get('username'))
    password_field = driver.find_element_by_id('Password')
    password_field.send_keys(os.environ.get('secret_f'))
    driver.find_element_by_xpath("//button[contains(text(), 'Log in')]").click()
    driver.get(url)

def log_out():
    """Logs out once the actions are done"""
    # This is to load environment variables
    load_dotenv()

    logout_url = os.environ.get('logout_url')
    driver.get(logout_url)

def apply_basic_filters(filter_dict={'location': 'Amsterdam', 'radius': '0', 'min_price': '0', 'max_price': 'ignore_filter'}):
    """Takes a dictionary of basic filters, applies them and searches for the properties"""
    # Now apply desired filters (e.g. set location to Amsterdam)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "filter_location")))
    filter_loc = driver.find_element_by_name('filter_location')
    filter_loc.send_keys(filter_dict['location'])

    # Wait for the first dropdown option to appear and select the first option
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".autocomplete-list")))
    filter_loc.send_keys(Keys.ARROW_DOWN)
    filter_loc.send_keys(Keys.ENTER)

    filter_radius = Select(driver.find_element_by_id('Straal'))
    filter_radius.select_by_value(filter_dict['radius'])

    filter_price_from = Select(driver.find_element_by_name('filter_KoopprijsVan'))
    filter_price_from.select_by_value(filter_dict['min_price'])

    filter_price_upto = Select(driver.find_element_by_name('filter_KoopprijsTot'))
    filter_price_upto.select_by_value(filter_dict['max_price'])

    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='button-primary-alternative']")))
    find_search = driver.find_element_by_xpath("//button[contains(text(), 'Search')]")
    find_search.click()

def get_id(html):
    """Given an html this function retrieves the property id from the html link.
    Returns the id"""
    return int(re.findall(r'-\d*-', html)[0].strip('-'))



# Get urls for all the pages and put them into a list
def get_url_list():
    """Records the current url and goes through the website, clicking Next as many times as there are pages.
    Returns a list of urls to be used in the get_htmls function."""
    #Creates a list of urls for all pages
    url_list = []

    #Reads the url of the page the driver is currently in and adds it into the list
    current_page_url = driver.current_url
    url_list.append(current_page_url)

    curr_page_num = 1
    count_exceptions = 0
    while True:
        try:
            curr_page_num += 1
            #Find "Next" button and click it
            find_next = driver.find_element_by_xpath("//a[@rel='next']")
            find_next.click()
            current_page_url = driver.current_url
            url_list.append(current_page_url)
            time.sleep(10)
        except:
            #Count the exceptions
            count_exceptions += 1
            curr_page_num -= 1 #since we are coming back to the same page
            #If the there haven't been 3 exceptions yet, sleep for a bit and then continue
            if count_exceptions < 3:
                time.sleep(10)
            else:
                #If "Next" button isn't there anymore or an error occurs, return the list
                #driver.close()
                print(f'Url list collection - complete. Last page number was {curr_page_num}.')
                return url_list

    print(f'Url list collection - complete. Last page number was {curr_page_num}.')
    return url_list


#Get all the html files for each property ad and put it into a list
def get_htmls():
    """Takes current html list.
    Returns updated html list with all the property ad htmls available on the page."""
    #Find all property ad htmls
    html_list = []
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        html = elem.get_attribute("href")
        if (bool(re.search(r'appartement-\d+', html)) or bool(re.search('huis-\d+', html))) and html not in html_list:
            html_list.append(html)
    return html_list


def get_feat_dict(html):
    """Takes a string with all highlighted features and puts them into a dictionary.
    Returns the dictionary"""

    # Open the html
    driver.get(html)

    # Click to see all the features available (if button doesn't appear, continue)
    try:
        WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".object-kenmerken-open-button")))
        driver.find_element_by_class_name('object-kenmerken-open-button').click()
    except:
        pass

    # Retrieve all the other features now
    time.sleep(5)
    feature_elems = driver.find_elements_by_class_name('object-kenmerken-body')
    feature_string = ''
    for elem in feature_elems:
        if feature_string == '':
            feature_string = elem.text
        else:
            feature_string += '\n' + str(elem.text)

    categories = ['Auction', 'Transfer of ownership', 'Construction', 'Surface areas and volume', 'Areas', 'Layout', 'Energy', 'What does this mean?', 'Cadastral data', 'Exterior space', 'Storage space', 'Parking', 'VVE (Owners Association) checklist', 'Garage', 'Commercial property']
    special_categories = ['Cadastral data', 'Commercial property']
    to_delete = ['Cadastral map']
    features = feature_string.split('\n')
    feat_list = [feat for feat in features if feat not in to_delete]

    feat_dict = {}
    current_index = 0
    current_category = ''

    for feat in feat_list:
        feat = feat_list[current_index]
    #     print(feat, current_index)
        if feat in categories:
            feat_dict[feat] = ''
            current_category = feat
            current_index += 1
        else:
            if current_category in special_categories:
                feat_dict[current_category] += str(feat) + '; '
                if current_index+2 < len(feat_list):
                    current_index += 1
                else:
                    break
            elif feat in feat_dict.keys():
                feat_dict[feat+'_'+current_category] = feat_list[current_index+1]
                if current_index+2 < len(feat_list):
                    current_index += 2
                else:
                    break
            else:
                feat_dict[feat] = feat_list[current_index+1]
                if current_index+2 < len(feat_list):
                    current_index += 2
                else:
                    break
    return feat_dict


def scrape_data(ads_list=[], url_list_name='', url_index=0):
    """Reads in the data about each property from a given html files.
    Returns a list of dictionaries of all scraped ads (one dictionary per add)."""

    today_timestamp = str(dt.date.today().year) + str(dt.date.today().month) + str(dt.date.today().day)

    if ads_list != []:
        feat_dict_list = ads_list
    else:
        feat_dict_list = []

    new_ad_count = 0

    if url_list_name != '':
        with open(f'./Cellar/{url_list_name}.pkl', 'rb') as url_pickle:
            url_list = pickle.load(url_pickle)
    else:
        url_list = get_url_list()
        page_count = len(url_list)
        with open(f'./Cellar/url_list_{today_timestamp}.pkl', 'wb') as url_pickle:
            pickle.dump(url_list, url_pickle)

    if url_index != 0:
        original_url_list = url_list
        url_list = url_list[url_index:]

    for url in url_list:
        try:
            driver.get(url)
            html_list = get_htmls()

            for html in html_list:
                new_ad_count += 1
                property_dict = {}

                # To open the property ad
                driver.get(html)

                # To scrape initial data points
                property_dict['property_link'] = html
                property_dict['property_id'] = get_id(html)
                property_dict['title'] = driver.find_element_by_class_name('object-header__title').text
                property_dict['address'] = driver.find_element_by_class_name('object-header__subtitle').text
                property_dict['price'] = driver.find_element_by_class_name('object-header__price').text
                property_dict['neighbourhood'] = driver.find_element_by_class_name('object-buurt__name').text
                property_dict['scraped_date'] = dt.date.today()

                other_features = get_feat_dict(html)
                for key, value in other_features.items():
                    if key not in property_dict.keys():
                        property_dict[key] = value
                if property_dict not in feat_dict_list:
                    feat_dict_list.append(property_dict)
                last_url = url
        except:
            total_ad_count = len(feat_dict_list)
            if url_index != 0:
                print(last_url, f'This URL is number {original_url_list.index(last_url)} in the original url_list.')
            else:
                print(last_url, f'This URL is number {url_list.index(last_url)} in the supplied url_list.')
            print(f'Finished with an error. Number of ads scraped {new_ad_count}, total number of ads in the list is {total_ad_count}.')
            return feat_dict_list
    total_ad_count = len(feat_dict_list)
    print(f'Finished without errors. Number of ads scraped {new_ad_count}, total number of ads in the list is {total_ad_count}.')
    return feat_dict_list



def get_recent_ads(days='1', ads_list=[], url_list_name='', url_index=0):
    """Retrieves only property adverts posted passed in number of days from today (one being today).
    The only options for days are 1, 3, 5, 10 and 30.
    The default is today (1)."""
    apply_ad_filters({'filter_type': 'days', 'filter': days})
    return scrape_data(ads_list=ads_list, url_list_name=url_list_name, url_index=url_index)


def apply_ad_filters(filters_dict={'filter_type': 'days', 'filter': '10'}):
    """Applies specific filters like the size of the property, facilities, etc.
    Available filter types: days, status"""
    filter_type = filters_dict['filter_type']
    type_css_dict = {'days': 'PublicatieDatum-'}

    filters_button_css = ".search-content-header-button-filters.button-tertiary"
    days_on_funda_css = f"label[class='radio-group-item-label label-text'][for='{type_css_dict[filter_type]}{days}']"
    remove_filter_css = "button[class='mobile-filter-reset-button button-tertiary is-enhanced']"

    filters_button = driver.find_element_by_css_selector(filters_button_css)
    filter_dof = driver.find_element_by_css_selector(days_on_funda_css)
    remove_dof_filter = driver.find_element_by_css_selector(remove_filter_css)
    close_filters_pane = driver.find_element_by_css_selector('.button-tertiary.close-search-sidebar')

    # Click on filters button
    try:
        time.sleep(3)
        filters_button.click()
        print('Filters button clicked successfully')
    except:
        print('No filters button available, trying to filter directly.')
        pass

    try:
        time.sleep(4)
        filter_dof.click()
        print('Days on funda set to "days" successfully')
    except:
        print('No "Days on funda" section available, trying to remove existing filter.')
        pass

    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, remove_filter_css)))
        remove_dof_filter.click()
        print('Original filter removed')
    except:
        print('Not able to remove filters.')
        pass

    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, days_on_funda_css)))
        next_section = driver.find_element_by_xpath("//legend[contains(text(), 'Number of rooms')]")
        ActionChains(driver).move_to_element(next_section).perform()
        filter_dof.click()
        print('New filter applied successfully')
        # This is to close the filters pane
        time.sleep(2)
        close_filters_pane.click()
        print('Filters pane closed successfully')
    except:
        print('Could not set the filter.')


def save_to_favourites(html):
    """Saves the given html of the property to favourites"""
    # Goes to the provided html (link)
    driver.get(html)

    # Find the "heart" icon and clicks it once
    driver.find_element_by_class_name('user-save-object').click()
