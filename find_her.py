import itertools
from explicit import waiter, XPATH
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import instaloader
import os
import face_recognition
import glob

foundAccounts = []

def login(driver):
    username = "Your username" 
    password = "Your password" 


    driver.get("https://www.instagram.com/accounts/login/")
    sleep(3)

    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    submit = driver.find_element_by_tag_name('form')
    submit.submit()

    WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Not Now')]"))).click()


    WebDriverWait(driver, 15).until999        (
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))
    


def scrape_followers(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    sleep(2)
    driver.find_element_by_partial_link_text("follower").click()
    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)
    allfoll = int(driver.find_element_by_xpath("//li[2]/a/span").text)
    follower_css = "ul div li:nth-child({}) a.notranslate"  
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            if follower_index > allfoll:
                raise StopIteration
            yield waiter.find_element(driver, follower_css.format(follower_index)).text
        last_follower = waiter.find_element(driver, follower_css.format(group+11))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)


def downloadImage(accoutName):
    mod = instaloader.Instaloader()
    mod.download_profile(accoutName,profile_pic_only=True)

def face_identifier(accountName, targetEncoding):
    os.chdir(os.path.join("C:/Users/ashut/Desktop/find_her",accountName))
    for f in glob.glob("*.jpg"):
        imageName = f    
    accountImage = os.path.join(os.getcwd(),imageName)
    image = face_recognition.load_image_file(accountImage)
    face_locations = face_recognition.face_locations(image)

    accountEncoding = get_face_encoding(accountImage,face_locations)
    if(accountEncoding is None):
        return    

    results = face_recognition.compare_faces([targetEncoding], accountEncoding)
    print(results)

def get_face_encoding(fileName,facelocation =None):
    image = face_recognition.load_image_file(fileName)
    try:
        encoding = face_recognition.face_encodings(image,known_face_locations=facelocation)[0]
        return encoding
    except IndexError as e:
        print(e)
    

if __name__ == "__main__":

    fileName = "The face of the person you want to search"
    encoding = get_face_encoding(fileName=fileName)

    account = "The account you want to search In(must be public and this script only looks into the followers)" 
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    try:
        login(driver)
        print('Followers of the "{}" account'.format(account))
        for count, follower in enumerate(scrape_followers(driver, account=account), 1):
            downloadImage(follower)
            face_identifier(follower,encoding)
            os.chdir("C:/Users/ashut/Desktop/find_her")
            print("\t{:>3}: {}".format(count, follower))
        
    finally:
        print(foundAccounts)
        driver.quit()