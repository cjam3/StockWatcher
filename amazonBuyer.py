from selenium import webdriver
import time, logging
import pyinputplus as pyip

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
testing = True


def main():
    username = pyip.inputStr('Amazon Username: ')
    password = pyip.inputPassword('Amazon Password: ', '*')
    passwordCheck = pyip.inputPassword('Re-enter Amazon Password: ', '*')

    if password != passwordCheck:
        print('Passwords did not match. Please try again.')
        exit(0)

    browser = webdriver.Firefox()
    browser.get('https://www.amazon.com/gp/offer-listing/B08HH5WF97/ref=dp_olp_unknown_mbc')

    while True:
        try:
            priceElem = browser.find_element_by_css_selector('span.a-size-large')
            buttonElem = browser.find_element_by_css_selector('.a-button-input')
        except:
            logging.info('No current offers available')

        if convertToNum(priceElem.text) < 800 and isNewCondition(browser):
            buttonElem.click()
            logging.info('Adding to cart')
            if not testing:
                signInandPlaceOrder(browser, username, password)
            browser.quit()
            break

        time.sleep(15)
        logging.info('Refreshing')
        browser.refresh()


def convertToNum(money):
    number = []
    for i in money:
        if i.isdecimal() or i == '.':
            number.append(i)

    return float(''.join(number))


def signInandPlaceOrder(browser, username, password):
    try:
        proceed = browser.find_element_by_css_selector('#hlb-ptc-btn-native')
        proceed.click()
    except:
        print('Could not find proceed to checkout button.')

    try:
        usernameBox = browser.find_element_by_css_selector('#ap_email')
        continueButton = browser.find_element_by_css_selector('.a-button-input')
        usernameBox.send_keys(username)
        continueButton.click()
    except:
        print('Could not find username input or continue button')

    try:
        passwordBox = browser.find_element_by_css_selector('#ap_password')
        signInButton = browser.find_element_by_css_selector('#signInSubmit')
        passwordBox.send_keys(password)
        signInButton.click()
    except:
        print('Could not find password box or sign in button.')

    try:
        placeOrderButton = browser.find_element_by_name('placeYourOrder1')
        placeOrderButton.click()
    except:
        print('Unable to find place order button.')

def isNewCondition(browser):
    try:
        conditionElem = browser.find_element_by_xpath("//span[@class='a-size-medium olpCondition a-text-bold']")
    except:
        logging.error('Unable to locate condition of item!')
        return False
    logging.info(f'Found item with {conditionElem.text} condition')
    if conditionElem.text.lower() == 'new':
        return True
    else:
        return False


if __name__ == '__main__':
    main()
