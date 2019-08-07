from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://passport.yandex.ru/auth/welcome')

assert 'Авторизация' in driver.title

time.sleep(5)
login_input = driver.find_element_by_id('passp-field-login')
login_input.send_keys('lenin.revo@yandex.ru')
login_input.send_keys(Keys.ENTER)
time.sleep(2)
passwd_input = driver.find_element_by_id('passp-field-passwd')
passwd_input.send_keys('bronivichok')
time.sleep(2)
passwd_input.send_keys(Keys.ENTER)
time.sleep(2)
to_mail_link1 = driver.find_element_by_class_name('user-pic__image')
to_mail_link1.click()
time.sleep(1)
to_mail_link2 = driver.find_element_by_xpath('/html/body/div[4]/ul/ul/li[1]/a')
to_mail_link2.click()
time.sleep(2)
#mails = driver.find_elements_by_xpath("//div[contains(@class, 'mail-MessageSnippet-Content')]")
mails = driver.find_elements_by_class_name('mail-MessageSnippet-Content')
for mail in mails:
    from_who = mail.find_element_by_xpath('//span[contains(@class, "mail-MessageSnippet-FromText")]').text
    topic = mail.find_element_by_xpath('//span[contains(@class, "mail-MessageSnippet-Item mail-MessageSnippet-Item_subject")]/span').text
    text = mail.find_element_by_xpath('//span[contains(@class, "mail-MessageSnippet-Item mail-MessageSnippet-Item_firstline js-message-snippet-firstline")]/span').text
    print(f'От кого: {from_who}')
    print(f'Тема: {topic}')
    print(f'Текст письма: {text}')
    print('*'*20)

driver.close()