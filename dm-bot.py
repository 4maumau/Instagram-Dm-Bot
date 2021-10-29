from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, random

browser = webdriver.Chrome('chromedriver')

#username and password of your instagram account:
my_username = open('username.txt', 'r').read()
my_password = open('password.txt', 'r').read()


#Instagram username list to DM:
usernameListFile = 'lista_users.txt'

#Message:
message = 'Opa, tudo bem? Estou passando aqui para avisar que o nosso campeonato está com uma nova data! Nós remarcamos para os dias 06 e 07/11, e a data limite para inscrições é no dia 04/11. A premiação continua a mesma: R$250,00 para o 1º lugar e R$100,00 para o 2º colocado. Vocês tem interesse em participar? Abração'

#Delay time between messages:
message_delay = 50

#Authorization:
def auth(username, password):
    try:
        browser.get('https://www.instagram.com/')
        random_sleep()

        input_username = browser.find_element_by_name("username")
        input_password = browser.find_element_by_name('password')

        #Write username and password + Enter
        input_username.send_keys(username)
        random_sleep()

        input_password.send_keys(password)
        random_sleep()

        input_password.send_keys(Keys.ENTER)
        print('pressed enter')
        random_sleep(4,8)


    except Exception as err:
        print(err)
        browser.quit()

#Send Messages:
def send_message(users, message):
    messagesCounter = 0

    try:
        #click on message button
        browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a').click()
        random_sleep(5,10)
        #turn off notifications
        browser.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[2]').click()
        random_sleep()
        #click send message button
        browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()

        #send message to user in the list
        for user in users:
            #search for user
            random_sleep()
            browser.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input').send_keys(user)
            random_sleep(2,3)
            #click on user
            browser.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div[2]').find_element_by_tag_name('button').click()
            random_sleep(3,4)
            #click next button
            browser.find_element_by_xpath('/html/body/div[6]/div/div/div[1]/div/div[2]/div/button').click()
            random_sleep(4,6)
            
            #write and send message
            text_area = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
            text_area.send_keys(message)
            random_sleep(2,4)
            text_area.send_keys(Keys.ENTER)

            #keeps track of everything
            messagesCounter += 1
            print(f'Message succesfully sent to {user}')
            delete_from_list(usernameListFile, user)
            
            #wait and start new message
            time.sleep(message_delay)
            browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()

    except Exception as err:
        print(err)
        browser.quit()

    print(f'Messaged {messagesCounter} users')

def file_lines_to_list(infile):
    outputList = []
    with open(infile) as input_file:
         outputList = [line.strip() for line in input_file]

    return outputList

def delete_from_list(txtFile ,user):
    #deletes user from list so you can just rerun the script without it sending the message to the same person twice
    with open(txtFile, "r") as f:
        lines = f.readlines()
    with open(txtFile, "w") as f:
        for line in lines:
            if line.strip("\n") != user:
                f.write(line)
    print(f'{user} deleted from {txtFile}')    

def random_sleep(min =1, max = 2):
    time.sleep(random.randrange(min, max))


usernamesList = file_lines_to_list(usernameListFile)

auth(my_username, my_password)
random_sleep(2,4)
send_message(usernamesList, message)
browser.quit()
