import pyttsx3 #pip install pyttsx3==Used for text-to-speech conversion.
import speech_recognition as sr #pip install SpeechRecognition==Used for recognizing speech input
import smtplib # Allows sending emails using the Simple Mail Transfer Protocol (SMTP). 
import pyautogui # pip install pyautogui==Enables taking screenshots and controlling the mouse and keyboard.
import webbrowser as web #Provides a high-level interface for allowing displaying Web-based documents to users.
import wikipedia # pip install wikipedia-api==Used for searching and retrieving information from Wikipedia
import pywhatkit as kit # pip install pywhatkit==for playing youtube
import clipboard #pip install clipboard==for manipulating clipeboard
import os# for using os function
import pyjokes#  pip install pyjokes== generate jokes
import time as tt #time related function
import string
import random# for generating random number
import psutil# pip install psutil== cpu usage and battery
from bs4 import BeautifulSoup#  pip install beautifulsoup4==web scraping
from newsapi import NewsApiClient#  pip install newsapi-python==fetch news articles
from nltk.tokenize import word_tokenize# pip install nltk == tokenized query (natural language processing)
from unidecode import unidecode#  pip install unidecode== unicode data to ascii
from datetime import datetime#for data and time function 
from email.message import EmailMessage# for email message
from secrete import senderemail,epwd#  stored email login info
import json# working with json
import requests# pip install requests == for http request

 #created class for voice assistant function 
 #if mic has problem than use take_command_cmd()
 
class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.contacts={}
        
    # used for switching male and female voice   
    def get_voices(self, voice):
        voices = self.engine.getProperty('voices')
        if voice == 1:
            self.engine.setProperty('voice', voices[0].id)
            self.speak("this is jarvis")
        elif voice == 2:
            self.engine.setProperty('voice', voices[1].id)
            self.speak("this is friday")
            
    #tts method
    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()
        
    #time and date functions
    def time(self):
        current_time = datetime.now().strftime("%I:%M:%S")
        self.speak("The current time is:")
        self.speak(current_time)
        
    #here we can get last screenshot by our programm by using this function    
    def view_last_screenshot(self, screenshot_directory):
        screenshot_files = [f for f in os.listdir(screenshot_directory) if f.lower().endswith(".png")]
        if screenshot_files:
            latest_screenshot = max(screenshot_files, key=lambda f: os.path.getctime(os.path.join(screenshot_directory, f)))
            screenshot_path = os.path.join(screenshot_directory, latest_screenshot)
            self.speak("Displaying the last captured screenshot.")
            os.startfile(screenshot_path)
        else:
            self.speak("No screenshots found in the directory.")
            
    #this is extra code which save email contact info into json file  
    def add_contact(self):
        self.speak("Sure, please tell me the contact name.")
        name = self.take_command_cmd()
        self.speak(f"Please tell me the email address for {name}.")
        email = self.take_command_cmd()
        self.contacts[name] = email
        self.speak(f"Contact {name} with email {email} has been added.")
        self.save_contacts()  # Save the updated contacts to the file
        
    #show cpu usage    
    def cpu(self):
        usage = str(psutil.cpu_percent())
        self.speak("CPU is at " + usage)
        battery = psutil.sensors_battery()
        self.speak("Battery is at " + str(battery))

    def date(self):
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.speak("The current date is:")
        self.speak(current_date)

    def wish_me(self):
        self.speak("Welcome back, sir!")
        self.time()
        self.date()
        self.greeting()
        self.speak("Jarvis is at your service. Please tell me how I can help you.")

    def greeting(self):
        hour = datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good morning, sir!")
        elif 12 <= hour < 18:
            self.speak("Good afternoon, sir!")
        else:
            self.speak("Good evening, sir")
    #for mic issue i created it
    def take_command_cmd(self):
        query = input("Please tell me how I can help you:\n").lower()
        return query

    def take_command_mic(self):
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                print("Listening...")
                r.energy_threshold = 2000  # for sensitivity
                r.adjust_for_ambient_noise(source)
                try:
                    audio = r.listen(source, timeout=10) 
                except sr.WaitTimeoutError:
                    print("Listening timed out. Please speak again.")
                    continue  # Restart the loop on timeout
    
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language="en-IN")
                #print(query)
                return query
            except sr.UnknownValueError:
                print("Could not understand audio. Please speak again.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Please speak again.")

    #email sending function
    def send_email(self, receiver, subject, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(senderemail, epwd)

        email = EmailMessage()
        email['From'] = senderemail
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(content)

        server.send_message(email)
        server.close()
        self.speak("Email sent!")
        
    #google searching function
    def search_google(self):
        self.speak("What should I search?")
        search = self.take_command_mic()
        web.open('https://www.google.com/search?q=' + search)
        
    #function for weather
    def get_weather_info(self, city):
        url = f"https://www.google.com/search?q=weather+{city}&hl=en"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        temperature = soup.find("div", class_="BNeawe iBp4i AP7Wnd").find("div", class_="BNeawe iBp4i AP7Wnd").get_text()
        weather_condition = soup.find("div", class_="BNeawe tAd8D AP7Wnd").get_text()

        return f"Temperature: {unidecode(temperature)}, Weather: {unidecode(weather_condition)}"

    def news_update(self):
        newsapi = NewsApiClient(api_key="6e9bbb1e4bb54798a0d61bcc8ee95dd1")
        self.speak("What topic do you need news about?")
        topic = self.take_command_cmd()
        data = newsapi.get_top_headlines(q=topic, language='en', page_size=5)
        news_data = data['articles']# need just article of news 

        if not news_data:
            self.speak("I'm sorry, I couldn't find any news related to this.")
        else:
            for index, news in enumerate(news_data):
                description = news.get("description", "No description available")
                print(f'{index + 1}. {description}')
                self.speak(f'{index + 1}. {description}')

        self.speak("That's it for now. I'll update you with more news later.")

    def text_to_speech(self):
        text = clipboard.paste()
        print(text)
        self.speak(text)
        
    #save screenshot
    def screenshot(self):
        name_img = tt.time()
        name_img = f"E:\\python_project\\jarvis\\screenshot\\{name_img}.png"
        img = pyautogui.screenshot(name_img)
        img.show()
        
    #decision making
    def flip(self):
        self.speak("Okay, sir, flipping a coin")
        coin = ["head", "tail"]
        toss = []
        toss.extend(coin)
        random.shuffle(toss)
        toss = "".join(toss[0])
        self.speak("I flipped the coin and you got " + toss)
        
    #for time pass
    def roll(self):
        self.speak("Okay, sir, rolling a dice for you")
        dice = ["1", "2", "3", "4", "5", "6"]
        roll = []
        roll.extend(dice)
        random.shuffle(roll)
        roll = "".join(roll[0])
        self.speak("I rolled a dice and you got " + roll)
        
    #password gen
    def password_gen(self):
        s1 = string.ascii_uppercase
        s2 = string.ascii_lowercase
        s3 = string.digits
        s4 = string.punctuation
        passlen = 8
        s = []
        s.extend(list(s1))
        s.extend(list(s2))
        s.extend(list(s3))
        s.extend(list(s4))

        random.shuffle(s)
        new_pass = "".join(s[0:passlen])
        print(new_pass)
        self.speak(new_pass)
        
    #build this function for saving email info
    def save_contacts(self):
        with open("contacts.json", "w") as f:
            json.dump(self.contacts, f)
            
    #its loads the info
    def load_contacts(self):
        try:
            with open("contacts.json", "r") as f:
                self.contacts = json.load(f)
        except FileNotFoundError:
            self.contacts = {}
    
    def switch_input_method(self):
        self.speak("type or voice")
        response = self.take_command_mic()
        if "type" in response:
            return self.take_command_cmd()
        else:
            return self.take_command_mic()
        
    def whatsapp_message(self, phone_number, message):
        try:     
            kit.sendwhatmsg_instantly(phone_number, message)
        except Exception as e:
            self.speak(f"An error occurred while sending the WhatsApp message. {e}")
    
    def run(self):
        self.load_contacts()
        self.get_voices(1)
        wakeword = "jarvis"
        while True:
            query = self.take_command_mic()
            query = [word.lower() for word in word_tokenize(query)]
            print(query)
            if wakeword in query:
                if 'time' in query:
                    self.time()

                elif "flip" in query:
                    self.flip()
                    
                elif "friday" in query and "mode" in query:
                    self.get_voices(2)
                    
                elif 'date' in query:
                    self.date()

                elif "cpu" in query:
                    self.cpu()

                elif 'last screenshot' in query:
                    self.view_last_screenshot("E:\\python_project\\jarvis\\screenshot")

                elif "roll" in query:
                    self.roll()
                
                elif "add" in query:
                    self.add_contact()

                elif 'email' in query:
                    email_list = {
                        "joy": "tanjimjoy7@gmail.com",
                        "tanjim": "tanjimahmed327@gmail.com",
                        "raya":"rayaanjum0123@gmail.com"
                    }
                    try:
                        self.speak("To whom you want to send the email?")
                        name = self.take_command_mic()
                        receiver = email_list[name]
                        self.speak("What is the subject of the email?")
                        subject = self.take_command_mic()
                        self.speak("What should I say?")
                        content = self.take_command_mic()
                        self.send_email(receiver, subject, content)
                    except Exception:
                        self.speak("Unable to send email")
                        
                elif 'search' in query:
                    self.search_google()

                elif "read" in query:
                    self.text_to_speech()

                elif 'youtube' in query:
                    self.speak("What should I search on YouTube?")
                    topic = self.take_command_cmd()
                    kit.playonyt(topic)

                elif "password" in query:
                    self.password_gen()

                elif 'message' in query:
                    user_name = {
                        'Jarvis': '+8801745583607',
                        'raya':'+8801743207148',
                        'sydney':'+880 1567-910768'
                    }
                    try:
                        self.speak("To whom do you want to send the message?")
                        name = self.take_command_cmd()
                        phone_no = user_name.get(name)
                        if phone_no:
                            self.speak("What is the message?")
                            message = self.switch_input_method()
                            self.whatsapp_message(phone_no, message)
                            self.speak('Message has been sent.')
                        else:
                            self.speak("The recipient name is not in the list.")
                    except Exception:
                        self.speak("Unable to send the message.")

                elif 'joke' in query:
                    self.speak(pyjokes.get_joke())

                elif 'wikipedia' in query:
                    try:
                        self.speak('Searching in Wikipedia...')
                        query = " ".join(query)
                        query = query.replace("jarvis", "") 
                        result = wikipedia.summary(query, sentences=2)
                        print(result)
                        self.speak(result)
                    except wikipedia.exceptions.DisambiguationError as e:
                        self.speak(f"Multiple interpretations found for 'Jarvis'. Please provide more details. {e}")
                    except wikipedia.exceptions.PageError as e:
                        self.speak(f"Couldn't find information on 'Jarvis'. {e}")
                    except Exception as e:
                        self.speak(f"An error occurred during the Wikipedia search. {e}")

                elif "screenshot" in query:
                    self.screenshot()

                elif 'news' in query:
                    self.news_update()

                elif 'vs code' in query:
                    code_path = "C:\\Users\\Tanjim_ahmed\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    os.startfile(code_path)

                elif 'weather' in query:
                    self.speak("Sure, please specify the city for weather information.")
                    city_text = self.take_command_cmd()
                    print(f"City: {city_text}")
                    weather_info = self.get_weather_info(city_text)
                    print(weather_info)
                    self.speak(weather_info)

                elif 'open' in query:
                    os.system(f'explorer C://{query.replace("open", "")}')

                elif 'remember that' in query:
                    self.speak("What should I remember?")
                    data = self.take_command_mic()
                    self.speak("You asked me to remember " + data)
                    remember = open("data.txt", "w")
                    remember.write(data)
                    remember.close()

                elif "tell me tasks" in query:
                    remember = open("data.txt", "r")
                    self.speak("You saved " + remember.read())

                elif "offline" in query:
                    self.speak("Goodbye!")
                    quit()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.wish_me()
    assistant.run()
