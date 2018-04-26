from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pause
import datetime
from time import time

MS_DAY = 86400000
MS_WEEK = 604800000
HOURS_4 = 14400000
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# 12 hour format
start = 5

# 24 hour format
end = 21

options = Options()
options.set_headless(headless=True)
browser = webdriver.Chrome(chrome_options=options)

# Loading Image
browser.get('https://i.imgflip.com/28z4h9.jpg')

# Time to start booking a room
bt = datetime.datetime.now()
if bt.hour != 0 or bt.minute != 0 or bt.second != 0 or bt.microsecond != 0:
    bt = bt.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)

# Time of reservation
rt = bt + datetime.timedelta(weeks=1)
rt_epoch = int(rt.timestamp()) * 1000 - HOURS_4
wd = WEEKDAYS[bt.weekday()]

print('Current Time:        {}'.format(datetime.datetime.now()))
print('Booking Time:        {}'.format(bt))
print('Reservation Time:    {}'.format(rt))
print('Reservation Epoch:   {}'.format(rt_epoch))
print('Weekday:             {}'.format(wd))
print('Start    (12-HR):    {}'.format(start))
print('End      (24-HR):    {}'.format(end))

pause.until(bt)

# Start timer
s_time = time()

# Navigate to the study room booking site
browser.get('https://gmu.libcal.com/spaces?lid=1205&gid=2119')

# Go to desired date
browser.find_element_by_class_name('fc-goToDate-button').click()
browser.find_element_by_xpath('//td[@data-date="{}"]'.format(str(rt_epoch))).click()

# Click on the starting block
print('Finding Start Block . . .')
while True:
    try:
        browser.find_element_by_xpath(
            "//*[contains(@title, '{:d}:00pm {}') and contains(@title, '4104')]"
                .format(start, wd)
        ).click()
        break
    except:
        print('.')
        pass

# Click on the ending time
print('Finding End Block . . .')
while True:
    try:
        browser.find_element_by_xpath(
            "//*[contains(@value, '{:d}:00')]"
                .format(end)
        ).click()
        break
    except:
        print('.')
        pass

# Submit study room reservation
print('Submitting Blocks . . .')
browser.find_element_by_name('submit_times').click()

# Accept lost of rights
print('Signing Away Rights . . .')
while True:
    try:
        browser.find_element_by_id('terms_accept').click()
        break
    except:
        print('.')
        pass

# Enter in first name, last name, and email
print('Entering In User Info . . .')
browser.find_element_by_id('fname').send_keys('Albert')
browser.find_element_by_id('lname').send_keys('Lam')
browser.find_element_by_id('email').send_keys('alam12@masonlive.gmu.edu')

# Submit reservation
browser.find_element_by_id('btn-form-submit').click()

# TODO - ADD EMAIL FINDER
# TODO - ADD EMAIL VERIFICATION CLICKER

# End timer
f_time = time()

print('\nDone! ({:g}s)'.format(f_time - s_time))

# Prints out reservation information
table = browser.find_element_by_class_name('s-lc-eq-checkouttb')
row = table.find_elements_by_tag_name('tr')
data = row[1].find_elements_by_tag_name('td')[1:-1]
print('{}, {}\n({}) -> ({})'.format(data[0].text, data[1].text, data[2].text, data[3].text))
