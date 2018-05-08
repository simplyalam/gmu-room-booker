from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pause
import datetime
from time import time
import threading

MS_DAY = 86400000
MS_WEEK = 604800000
HOURS_4 = 14400000
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class Booker(threading.Thread):
    def __init__(self, fname: str, lname: str, email: str, start_time: int,
                 end_time: int, room: str, submit: bool = True) -> None:
        threading.Thread.__init__(self)
        self.start_time = start_time
        self.end_time = end_time
        self.fname = fname
        self.lname = lname
        self.email = email
        self.room = room
        self.submit = submit

    def run(self) -> None:
        print('Starting thread {}'.format(self.fname))
        book(self.fname, self.lname, self.email, self.start_time, self.end_time, self.room, self.submit)


# noinspection PyBroadException
def book(fname: str, lname: str, email: str, start: int, end: int, room: str, submit: bool = False) -> None:
    half_s = '00'
    half_e = '00'

    # Check for half values
    if type(start) is float:
        half_s = '30'
        start = int(start - 0.5)
    if type(end) is float:
        half_e = '30'
        end = int(end - 0.5)

    # Parse for AM / PM
    if start >= 12:
        if start != 12:
            start -= 12
        start = f'{start}:{half_s}pm'
    else:
        start = f'{start}:{half_s}am'
    end_time = f'{end}:{half_e}'

    options = Options()
    options.set_headless(headless=True)
    browser = webdriver.Chrome(chrome_options=options)

    # Time to start booking a room
    bt = datetime.datetime.now()
    if bt.hour != 0 or bt.minute != 0 or bt.second != 0 or bt.microsecond != 0:
        bt = bt.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)

    # Time of reservation
    rt = bt + datetime.timedelta(weeks=1)
    rt_epoch = int(rt.timestamp()) * 1000 - HOURS_4
    wd = WEEKDAYS[bt.weekday()]

    print(f'Name:               {fname} {lname}')
    print(f'Current Time:       {datetime.datetime.now()}')
    print(f'Booking Time:       {bt}')
    print(f'Reservation Time:   {rt}, {rt_epoch}')
    print(f'Start-End:          {wd}, {start} - {end_time}')

    pause.until(bt)

    # Start timer
    s_time = time()

    # Navigate to the study room booking site
    browser.get('https://gmu.libcal.com/spaces?lid=1205&gid=2119')

    # Go to desired date
    browser.find_element_by_class_name('fc-goToDate-button').click()
    browser.find_element_by_xpath(f'//td[@data-date="{str(rt_epoch)}"]').click()

    # Click on the starting block
    print('Finding Start Block . . .')
    for i in range(1000):
        try:
            browser.find_element_by_xpath(f"//*[contains(@title, '{start} {wd}') and contains(@title, '{room}')]"
                                          ).click()
            break
        except:
            if i == 1000:
                print('FAILED')
                return

    # Click on the ending time
    print('Finding End Block . . .')
    while True:
        try:
            browser.find_element_by_xpath(
                f"//*[contains(@value, '{end_time}')]"
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
    browser.find_element_by_id('fname').send_keys(fname)
    browser.find_element_by_id('lname').send_keys(lname)
    browser.find_element_by_id('email').send_keys(email)

    # Submit reservation
    if submit:
        browser.find_element_by_id('btn-form-submit').click()

    # TODO - ADD EMAIL FINDER
    # TODO - ADD EMAIL VERIFICATION CLICKER

    # End timer
    f_time = time()

    print(f'{fname} {lname} : {email} : Room {room} ({start}-{end_time})')
    print(f'Done! ({f_time - s_time:g}s)')

    # Prints out reservation information
    if submit:
        table = browser.find_element_by_class_name('s-lc-eq-checkouttb')
        row = table.find_elements_by_tag_name('tr')
        data = row[1].find_elements_by_tag_name('td')[1:-1]
        print(f'{data[0].text}, {data[1].text}\n({data[2].text}) -> ({data[3].text})')
