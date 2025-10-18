#libraries and framework imports
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app_password_instructions = """1. Open your browser and go to https://myaccount.google.com and sign in to the Google account you want to use. 
2. In the left menu click Security (or open the Security section). 
3. Under “Signing in to Google” find 2-Step Verification. If it is not turned on, click it and follow the prompts to enable 2-Step Verification (you’ll set up a phone, authenticator app, or other second step). 
4. After 2-Step Verification is enabled, return to Security → Signing in to Google and click App passwords (or go directly to https://myaccount.google.com/apppasswords). You may be asked to sign in again for security. 
5. In the App passwords page:
6. Click the Select app dropdown and choose the app (Mail, Calendar, Contacts, etc.) — or choose Other (Custom name) and type a name that helps you remember the purpose (e.g., “Thunderbird on Laptop” or “LessonTracker SMTP”).
7. Click Select device and choose a device (or choose Other to name it).
8. Click Generate. 
9. Google will show a 16-character app password in groups of 4 (e.g. abcd efgh ijkl mnop). Copy that password (or write it down) — this is the only time you’ll see it. Use this 16-character string in place of your regular Google password inside the app or device that needs it. 
10.After successful setup in the app/device, you can close the dialog. The app password remains valid until you revoke it or change your Google account password (changing your main Google password revokes app passwords). 

"""

def email_configuration():
    while True: #Ensures that code continues to run until required input is given
        Select_news_type = input('Select news to send:\n1.BBC\n2.GHANAWEB\n:') #asking user to choose the type of news website to scrape
        
    #making a decision based on users' choice on the type of news website to scrape
        if Select_news_type== '1':
            print('Wait while we scrape the content.....') #Reassuring user in case of any delay due to slow network
            Scrape_content = scrape_bbc() #calling the function to scrape the content from bbc.com
            break

        elif Select_news_type== '2':
            print('Wait while we scrape the content.....') #Reassuring user in case of any delay due to slow network
            Scrape_content = scrape_ghanaweb() #calling the function to scrape content from ghanaweb
            break
        else:
            print('Please enter a valid option')
            continue


    while True: #Ensures that code continues to run until required input is given
        Receiver_type = input('Who are you sending to:\n1.SELF\n2.OTHER\n') #asking user to decide who to send the content to.
        
        #making a decision based on users' input
        if Receiver_type == '1':
            Sender_address = input('Enter your email address\n:') #taking sender address
            Title = input('Email subject\n:') #taking subject for mail to be sent
            Password = input('Enter app password\n[NB: Your app password is not\nthe same as your gmail account\npassword.]\nEnter no if you do not know your app password:') #taking email password of sender
        #Email configuration
            message = MIMEMultipart("alternative")
            message["Subject"] = Title
            message["From"] = Sender_address
            message["To"] = Sender_address

            Part = MIMEText(Scrape_content, "plain")
            message.attach(Part)

            if Password == 'no':
                print(app_password_instructions)
            else:
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                    server.login(Sender_address,Password)
                    server.sendmail(Sender_address,Sender_address,message.as_string())
                    print('Email sent!')
                    break

        elif Receiver_type == '2':
            Sender_address = input('Enter your email address\n:')
            Receiver_address = input('Enter receiver email address\n:')
            Title = input('Email subject\n:')
            Password = input('Enter app password\n[Note that your password is safe\nand cannot be viewed by a third party]\n:')
        
        #Email configuration
            message = MIMEMultipart("alternative")
            message["Subject"] = Title
            message["From"] = Sender_address
            message["To"] = Receiver_address

            Part = MIMEText(Scrape_content, "plain")
            message.attach(Part)

            if Password == 'no':
                print(app_password_instructions)
            else:
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                    server.login(Sender_address,Password)
                    server.sendmail(Sender_address,Receiver_address,message.as_string())
                    print('Email sent!')
                    break

        else:
            print('Please enter a valid option')
            continue
    
def scrape_bbc(): #Functions for scraping news from bbc.com
    html_file = requests.get('https://www.bbc.com/').text 
    soup = BeautifulSoup(html_file,'lxml')
    stories = soup.find_all('h2')

    news = ''
    for story in stories:
        news += (f'{story.text}\n')

    return news

def scrape_ghanaweb(): #Functions for scraping news from ghanaweb
    html_file = requests.get('https://www.ghanaweb.com/').text
    soup = BeautifulSoup(html_file,'lxml')
    stories = soup.find_all('div',class_='info')
    news = ''
    for story in stories: 
        news += (f'{story.text}\n')
        
    return news

#scrape_ghanaweb()
#scrape_bbc()
email_configuration()


