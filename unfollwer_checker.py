# importing required stuffs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from getpass import getpass
from time import sleep

# inputs for username and password
USERNAME = input('Enter your phone number or username or email: ')
PASSWORD = getpass('Enter your password: ')
PATH = input("Enter the path of your chromedriver")

# final needed lists
notFollowingMe = []
#meNotFollowing = []

# setting chrome driver path
#PATH = r'C:\Users\hp\AppData\Local\Google\Chrome\Application\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get('https://www.instagram.com/')
driver.maximize_window()


def page_found(selector, value):
    # this verifies if the required page is loaded or not
    try:
        useless_variable = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((selector, value))
        )
        return True
    except Exception as e:
        print("ERROR ARRIVED WHEN LOADING THE PAGE ", e)
        return False


def get_names():
    # returns the list of followers and followings
    peoples = []
    lh = 0
    ch = 1
    if page_found(By.CLASS_NAME, 'pbNvD '):
        container = driver.find_element_by_class_name('isgrP')
        peoplesInContainer = container.find_elements_by_tag_name('a[class="FPmhX notranslate  _0imsa "]')

        # scrolls untill we reach the end
        while ch != lh:
            lh = ch
            sleep(1)
            ch = driver.execute_script(
                """arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollTop""", container
            )
            peoplesInContainer = container.find_elements_by_tag_name('a[class="FPmhX notranslate  _0imsa "]')

        for eachPerson in peoplesInContainer:
            peoples.append(eachPerson.text)
        driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()
        return peoples


if page_found(By.NAME, 'username'):
    # initialing the login areas
    usernameInputArea = driver.find_element_by_name('username')
    passwordInputArea = driver.find_element_by_name('password')
    loginButton = driver.find_element_by_tag_name('button[type="submit"]')

    # entering username password and clicking login
    usernameInputArea.send_keys(USERNAME)
    passwordInputArea.send_keys(PASSWORD)
    loginButton.click()

    if page_found(By.CLASS_NAME, 'olLwo'):
        # skipping the save info dialoge
        skip = driver.find_element_by_class_name('yWX7d')
        skip.click()

        if page_found(By.CLASS_NAME, 'HoLwm'):
            # skipping the notifications dialoge
            skip = driver.find_element_by_class_name('HoLwm')
            skip.click()

            if page_found(By.CLASS_NAME, 'gmFkV'):
                # finding and clicking the profile
                myProfile = driver.find_element_by_class_name('gmFkV')
                myProfile.click()

                if page_found(By.CLASS_NAME, 'zwlfE'):
                    # finding the followers tab and clicking it to get the followers
                    postFollowersFollowing = driver.find_elements_by_class_name('-nal3 ')
                    postFollowersFollowing[1].click()
                    followers = get_names()

                    # finding the followings tab and clicking it to get the followingd
                    postFollowersFollowing = driver.find_elements_by_class_name('-nal3 ')
                    postFollowersFollowing[2].click()
                    followings = get_names()

                    # filling the lists of peoples that have not followed me
                    for following in followings:
                        if followers.count(following) == 0:
                            notFollowingMe.append(following)

                    # filling the lists of peoples that I have not followed
                    # for follower in followers:
                    #     if followings.count(follower) == 0:
                    #         meNotFollowing.append(follower)

                    # printing all the values
                    print(f'{len(notFollowingMe)} peoples have not followed you')
                    #print(f'You have not followed {len(meNotFollowing)} peoples')

                    print('---' * 100)
                    print('NOT FOLLOWING ME')
                    for each in notFollowingMe:
                        print(each)

                    # print('---' * 100)
                    # print('I AM NOT FOLLOWING')
                    # for each in meNotFollowing:
                    #    print(each)
# quitting the browser after the work is done
driver.quit()
# a random input statement to stop the commandline from exiting
input()
