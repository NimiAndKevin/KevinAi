import geocoder
import openai
import cv2
from textblob import TextBlob
from PyDictionary import PyDictionary
from googletrans import Translator
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import requests
import json
import random
import datetime
import pywhatkit
import threading
import subprocess
import os
import psutil
import shutil
# Dictionary to store projects and tasks
projects = {}

# Set up OpenAI API key
openai.api_key = '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'

# Initialize the camera (you may need to adjust the camera index)
cap = cv2.VideoCapture(0)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize the translator
translator = Translator()

# Initialize PyDictionary
dictionary = PyDictionary()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Define a variable to store the current status
user_status = "I'm doing well."

for i in range(3):
    a = input("Enter Password to open Kevin :- ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()
    if (a==pw):
        print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif (i==2 and a!=pw):
        exit()

    elif (a!=pw):
        print("Try Again")

# Function to speak a given text
def speak_properly(text):
    # You can adjust the voice parameters as needed
    voice = engine.getProperty('voices')[0]  
    engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 150)  
    engine.say(text)
    engine.runAndWait()

# Function to sign up a new user
def signup():
    speak_properly("Welcome to the signup process.")
    speak_properly("Please enter your desired username.")
    
    username = listen_for_command().lower()

    # Check if the username already exists
    if username in user_credentials:
        speak_properly("Sorry, this username is already taken. Please choose another username.")
        return

    speak_properly("Please enter your desired password.")
    password = listen_for_command()

    # Store the username and password in the user_credentials dictionary
    user_credentials[username] = password
    speak_properly("Signup successful. You can now log in.")

# Function to log in a user
def login():
    speak_properly("Welcome to the login process.")
    speak_properly("Please enter your username.")
    
    username = listen_for_command().lower()

    if username not in user_credentials:
        speak_properly("Username not found. Please sign up or enter a valid username.")
        return

    speak_properly("Please enter your password.")
    password = listen_for_command()

    if user_credentials[username] == password:
        speak_properly(f"Welcome back, {username}! You are now logged in. Hello {username}! I'm Kevin, How can I assist you today?")
        listen_for_user(username)
    else:
        speak_properly("Password incorrect. Please try again.")

# Function to start video recording
def record_video():
    cap = cv2.VideoCapture(0)  # Open the default camera (usually the built-in webcam)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec (you can change this as needed)
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # Output video file

    while True:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


# Function to listen for a voice command
def listen_for_command():
    with sr.Microphone() as source:
        global recognized_command
        print(f"Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak_properly("I didn't catch that. Can you please repeat?")
        return listen_for_command()
    except sr.RequestError:
        speak("I couldn't request results. Please check your internet connection.")
    
# Function to process voice commands
def process_command(command):
    current_time = datetime.datetime.now()
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    if "latest news" in command:
            get_latest_news()
    elif "sign up" in command:
            signup()
    elif "log in" in command:
            login()
    elif "blood" in command:
            vitals = monitor_vitals()
            speak_properly("Here are your vitals:")
            speak_properly(vitals)
    elif "change password" in command:
        speak("What's the new password")
        new_pw = input("Enter the new password\n")
        new_password = open("password.txt","w")
        new_password.write(new_pw)
        new_password.close()
        speak("Done sir")
        speak(f"Your new password is{new_pw}")
    elif "internet speed" in command:
        wifi  = speedtest.Speedtest()
        upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
        download_net = wifi.download()/1048576
        print("Wifi Upload Speed is", upload_net)
        print("Wifi download speed is ",download_net)
        speak(f"Wifi download speed is {download_net}")
        speak(f"Wifi Upload speed is {upload_net}")
    elif "what can you do" in command:
            describe_capabilities()
    elif "kevin" in command:
        speak_properly("Yes")
    elif "where am I" in command:
            user_location = get_user_location()
            speak(f"You are currently in {user_location.city}, {user_location.state}.")
    elif "thanks buddy" in command:
        speak_properly("You are Welcome")
    elif "merry christmas" in command:
        speak_properly("Merry christmas to you and everyone, Christmas is such a happy holiday and im happy to be in it")
    elif "i'm fine" in command:
        speak_properly("Happy to hear that")
    elif "i'm not fine" in command:
        speak_properly("sad to hear about that")
    elif "who are you" in command:
            introduce()
    elif "retrieve data" in command:
        speak("Sure, please specify the data you want to retrieve.")
        data_query = listen_for_command()
        result = retrieve_data_from_internet(data_query)
        speak("Here's the retrieved data:")
        speak(result)
    elif "happy halloween" in command:
        speak_properly("i don't like hallowen its so scary")
    elif "create project" in command:
        project_name = command.split("create project", 1)[1].strip()
        projects[project_name] = []
        speak_properly(f"Project '{project_name}' created.")
    elif "exit" in command:
        speak_properly("Goodbye!")
    elif "add task" in command:
        parts = command.split("add task", 1)
        project_name = parts[0].strip()
        task = parts[1].strip()
        add_task(project_name, task)
        speak_properly(f"Task added to '{project_name}': {task}")

    elif "list tasks" in command:
        project_name = command.split("list tasks", 1)[1].strip()
        list_tasks(project_name)

    elif "complete task" in command:
        parts = command.split("complete task", 1)
        project_name = parts[0].strip()
        task_index = int(parts[1].strip())
        complete_task(project_name, task_index)
    elif "count people" in command:
            people_count = count_people_in_environment()
            speak_people_count(people_count)
    elif "wishme" in command:
        current_time = datetime.datetime.now().time()
        if current_time < datetime.time(12):
            response = "Kevin: Good morning sir! How can I assist you today?"
        elif datetime.time(12) <= current_time < datetime.time(17):
            response = "Kevin: Good afternoon {username}! How can I assist you today?"
        else:
            response = "Kevin: Good evening sir! How can I assist you today?"
    elif "what's the weather" in command:
        speak_properly("Sure, please specify the location.")
        location = listen_for_command()
        weather_data = get_weather(location)
        if weather_data:
            temperature = weather_data['main']['temp']
            speak_properly(f"The current temperature in {location} is {temperature} degrees Celsius.")
        else:
            speak_properly(f"I couldn't fetch the weather data. Please try again later {username}.")
    if "detect emotions" in command:
            speak("Please speak, and I will analyze your emotions.")
            recorded_command = listen_for_command()
            emotion_response = analyze_emotions(recorded_command)
            speak(emotion_response)
    elif"set my status to" in command:
        new_status = command.split("set my status to", 1)[1].strip()
        user_status = new_status
        speak_properly(f"Your status has been updated to: {new_status}")
    elif "open google" in command:
        speak_properly("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak_properly("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open roblox" in command:
        speak_properly("Opening Roblox.")
        webbrowser.open("https://www.roblox.com")
    elif "make a website" in command:
        speak_properly("Creating a website called Nimicodes.com.")
    elif "open prime video" in command:
        speak_properly("Opening Prime Video.")
        webbrowser.open("https://www.amazon.com/Prime-Video")
    elif "open netflix" in command:
        speak_properly("Opening Netflix.")
        webbrowser.open("https://www.netflix.com")
    elif "call" in command:
        speak("Sure, whom do you want to call?")
        recipient_number = listen_for_command()
        call_on_whatsapp(recipient_number)
    elif "what's the time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak_properly(f"The current time is {current_time}.")
    elif "set an alarm" in command:
        speak_properly("Sure, please specify the time for the alarm in 24-hour format.")
        alarm_time = listen_for_command()
        try:
            alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
            current_time = datetime.datetime.now()
            alarm_datetime = current_time.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

            if alarm_datetime < current_time:
                alarm_datetime += datetime.timedelta(days=1)  # Set the alarm for the next day if specified time has already passed today

            time_difference = (alarm_datetime - current_time).total_seconds()
            threading.Timer(time_difference, trigger_alarm).start()
            speak_properly(f"Alarm set for {alarm_time}.")
        except ValueError:
            speak_properly("Sorry, I couldn't set the alarm. Please specify the time in the correct format.")
    elif "order pizza" in command:
        pizza_order = gather_pizza_order_details()
        api_key = ""  # Replace with your actual API key
        place_pizza_order(pizza_order, api_key)
        pizza_order = {}
        speak_properly("What type of pizza would you like to order?")
        pizza_order["type"] = listen_for_command()

        speak_properly("What size would you like (small, medium, large)?")
        pizza_order["size"] = listen_for_command()

        speak_properly("Please provide your delivery address.")
        pizza_order["address"] = listen_for_command()

        speak_properly("What is your preferred payment method?")
        pizza_order["payment"] = listen_for_command()

    elif "calculate" in command:
        speak_properly("Sure, please provide the mathematical expression.")
        math_expression = listen_for_command()
        result = calculate(math_expression)
        speak_properly(f"The result of {math_expression} is {result}.")
    elif "how do I do something" in command:
        speak_properly("Of course! Please specify what you'd like to learn how to do.")
        topic = listen_for_command()
        search_how_to(topic)
    elif "open notepad" in command:
        speak_properly("Opening Notepad.")
        os.system("notepad")  # Open Notepad
    elif "convert" in command:
        conversion_query = command.split("convert", 1)[1].strip()
        conversion_result = convert_units(conversion_query)
        if conversion_result:
            speak_properly(f"The conversion result is: {conversion_result}")
        else:
            speak_properly("Sorry, I couldn't perform the conversion.")
    elif "record a video" in command:
            speak("Starting video recording. To stop recording, say 'stop recording video'.")
            video_thread = threading.Thread(target=record_video)
            video_thread.start()
            video_thread.join()  # Wait for the video recording to finish
            speak("Video recording finished.")
    elif "stop recording" in command:
            cv2.destroyAllWindows()  # Close the video recording window
    elif "remind me" in command:
        speak_properly("Sure, what would you like me to remind you of?")
        reminder_text = listen_for_command()
        speak_properly("When should I remind you of this?")
        reminder_time = listen_for_command()
        set_reminder(reminder_text, reminder_time)
        speak_properly(f"Okay, I will remind you to {reminder_text} at {reminder_time}.")
    elif "take a screenshot" in command:
        take_screenshot()
    elif "tell me a joke" in command:
        joke = get_random_joke()
        speak_properly("Here's a joke for you: " + joke)
    elif "tell me a riddle" in command:
        riddle = get_random_riddle()
        speak_properly("Here's a riddle for you: " + riddle)
    elif "search on youTube" in command:
        speak_properly("What would you like to search for on YouTube?")
        query = listen_for_command()
        search_youtube(query)
    elif "open map" in command:
        speak_properly("Opening maps.")
        os.system("start bingmaps:")
    elif "search on Amazon" in command:
        speak_properly("What product are you looking for on Amazon?")
        product_query = listen_for_command()
        search_amazon(product_query)
    elif "search on Twitter" in command:
        speak_properly("What would you like to search for on Twitter?")
        twitter_query = listen_for_command()
        search_twitter(twitter_query)
    elif "open news" in command:
        speak_properly("Opening the news.")
    elif "what's the date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak_properly(f"Today's date is {current_date}.")
    elif "set a reminder" in command:
        speak_properly("Sure, please specify the reminder message.")
        reminder_message = listen_for_command()
        speak_properly("When should I remind you?")
        reminder_time = listen_for_command()
        set_reminder(reminder_message, reminder_time)
    elif "tell me a fun fact" in command:
        fun_fact = get_random_fun_fact()
        speak_properly("Here's a fun fact: " + fun_fact)
    elif "search on Bing" in command:
        speak_properly("What would you like to search for on Bing?")
        query = listen_for_command()
        search_bing(query)
    elif "play a game" in command:
        speak_properly("Sure, let's play a game. I'll think of a number between 1 and 10, and you try to guess it.")
        play_number_guessing_game()
    elif "open camera" in command:
        speak_properly("Opening the camera.")
        open_camera()
    elif "read a book" in command:
        speak_properly("Sure, let me read you a short story.")
        read_story()
    elif "translate" in command:
        speak_properly("Sure, please specify the text you want to translate.")
        text_to_translate = listen_for_command()
        speak_properly("To which language would you like to translate the text?")
        target_language = listen_for_command()
        translated_text = translate_text(text_to_translate, target_language)
        speak_properly(f"The translated text is: {translated_text}")
    elif "play music on youtube" in command:
        speak_properly("Sure, what music would you like to listen to on YouTube?")
        music_query = listen_for_command()
        play_music_on_youtube(music_query)
    elif "send message on whatsapp" in command:
        speak_properly("Sure, whom do you want to send a message to on WhatsApp?")
        recipient_name = listen_for_command()
        speak_properly(f"What message would you like to send to {recipient_name} on WhatsApp?")
        message = listen_for_command()
        send_whatsapp_message(recipient_name, message)
    elif "tell me a riddle" in command:
        riddle = get_random_riddle()
        speak("Here's a riddle for you: " + riddle)
    elif "open code editor" in command:
        speak_properly("Opening your code editor.")
        os.system("code")  # Opens the default code editor
    elif "play a joke" in command:
        random_joke = get_random_joke()
        speak_properly("Here's a joke for you: " + random_joke)
    elif "change your voice" in command:
        speak_properly("Certainly! What type of voice would you like me to use?")
        new_voice = listen_for_command()
        change_voice(new_voice)
    elif "scan for injuries" in command:
        speak_properly("Initiating body scan for injuries...")
        scan_result = scan_for_injuries()
        speak_properly("The scan is complete. Here are the results:")
        speak_properly(scan_result)
    elif "system information" in command:
        system_info = get_system_info()
        speak_properly("Here's your system information:")
        speak_properly(system_info)
    elif "open safari" in command:
        speak_properly("Opening Safari.")
        open_safari() 
    elif "open app store" in command:
        speak_properly("Opening the App Store.")
        open_app_store()
    elif "open settings" in command:
        speak_properly("Opening Settings.")
        open_settings()
    elif "tell a joke" in command:
        joke = get_random_joke()
        speak_properly("Here's a joke for you: " + joke)
    elif "show how to subscribe to youtube" in command:
        show_subscribe_instructions()
    elif "vitals" in command:
        vitals_info = get_vitals()
        speak(vitals_info)
    elif "search on Wikipedia" in command:
        speak_properly("What would you like to search for on Wikipedia?")
        query = listen_for_command()
        wikipedia_result = search_wikipedia(query)
        if wikipedia_result:
            speak_properly("Here's what I found on Wikipedia:")
            speak_properly(wikipedia_result)
        else:
            speak_properly("I couldn't find information on that topic.")
    elif "play a game" in command:
        speak_properly("Sure, let's play a game. I'll think of a number between 1 and 100, and you can try to guess it.")
        play_number_guessing_game()
    
    elif "i want to ask a question" in command:
        speak_properly("Sure, go ahead and ask your question.")
        user_question = listen_for_command()
        response = answer_question(user_question)
        speak_properly(response)
        
    elif "search" in command:
        speak_properly("What would you like to search for?")
        query = listen_for_command()
        search(query)
    elif "who is" in command:
        person = command.split("who is", 1)[1].strip()
        answer = wikipedia_summary(person)
        speak_properly("Here's what I found about " + person + ": " + answer)
    if "define" in command:
            word_to_define = command.split("define", 1)[1].strip()
            define_word(word_to_define)
    elif "what are" in command:
        query = command.split("what are", 1)[1].strip()
        answer = wikipedia_summary(query)
        speak_properly("Here's what I found about why " + query + ": " + answer)
    elif "why are" in command:
        query = command.split("why are", 1)[1].strip()
        answer = wikipedia_summary(query)
        speak_properly("Here's what I found about why " + query + ": " + answer)
    elif "what's my status" in command:
        speak_properly("Your just the man with the plan and i'm very grateful to have you!")
    elif "what is" in command:
        query = command.split("what is", 1)[1].strip()
        answer = wikipedia_summary(query)
        speak_properly("Here's what I found about " + query + ": " + answer)
    elif "shutdown" in command:
        speak_properly("Shutting down your computer.")
        os.system("shutdown /s /t 0")  # Shuts down the computer immediately
    
    
# Create a thread for listening to voice commands
listen_thread = threading.Thread(target=listen_for_command)

# Create a thread for processing voice commands
process_thread = threading.Thread(target=process_command)

# Start both threads
listen_thread.start()
process_thread.start()
# Function to search the web using the default web browser
def search(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        speak_properly(f"Here are the search results for {query}.")
    except Exception as e:
        print("Error searching:", e)
        speak_properly("I encountered an error while searching. Please try again later.")
 # ...

# Function to play music on YouTube
def play_music_on_youtube(query):
    try:
        # Construct the YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(search_url)
        speak_properly(f"Playing music on youTube for {query}.")
    except Exception as e:
        print("Error playing music on youTube:", e)
        speak_properly("I encountered an error while playing music on youTube. Please try again later.")
# ...

# Function to get the user's location
def get_user_location():
    location = geocoder.ip('me')
    return location

# Function to transcribe and analyze emotions in voice commands
def analyze_emotions(command):
    try:
        text_blob = TextBlob(command)
        sentiment = text_blob.sentiment

        if sentiment.polarity > 0:
            return "You sound happy!"
        elif sentiment.polarity < 0:
            return "You sound sad."
        else:
            return "Your emotion is neutral."

    except Exception as e:
        return "Emotion analysis failed. Please try again."

# Function to retrieve data from the internet
def retrieve_data_from_internet(query):
    try:
        url = f"https://api.example.com/data?query={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return "Failed to retrieve data from the internet."
    except Exception as e:
        return str(e)

# Function to place a pizza order
def order_pizza(pizza_order):
    api_endpoint = "https://api.pizza-ordering-service.com/place-order"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    order_data = {
        "type": order_details["type"],
        "size": order_details["size"],
        "address": order_details["address"],
        "payment": order_details["payment"]
    }

    try:
        response = requests.post(api_endpoint, json=order_data, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            order_confirmation = response_data.get("confirmation")
            speak("Your pizza order has been placed. Here are the details: " + order_confirmation)
        else:
            speak("I'm sorry, there was an issue with your order. Please try again later.")
    except Exception as e:
        print("Error placing pizza order:", e)
        speak("I encountered an error while placing your order. Please try again later.")

# Function to answer questions using ChatGPT
def answer_question(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"I have a question: {question}\nAnswer:",
        max_tokens=100  # Adjust this to control the response length
    )
    return response.choices[0].text

# Function to take a screenshot
def take_screenshot(file_name="screenshot.png"):
    try:
        # Capture the screen
        screenshot = ImageGrab.grab()

        # Save the screenshot
        screenshot.save(file_name)
        print(f"Screenshot saved as {file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to take a screenshot
take_screenshot("my_screenshot.png")

# Function to get and say user's vitals
def get_vitals():
    # In a real implementation, you would retrieve vitals data from a secure source.
    # For demonstration, we'll use fictional data.
    vitals_data = {
        "heart_rate": 75,
        "blood_pressure": "120/80",
        "temperature": 98.6,
        "oxygen_saturation": 98,
    }

    # Construct a response
    response = "Here are your vitals:\n"
    for key, value in vitals_data.items():
        response += f"{key}: {value}\n"

    return response

# Function to open device settings
def open_settings():
    try:
        os.system("control")
        speak_properly("Opening settings.")
    except Exception as e:
        print("Error opening settings:", e)
        speak_properly("I encountered an error while opening settings. Please try again later.")

# Function to count people in the environment
def count_people_in_environment():
    people_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Implement people detection logic here using OpenCV or other computer vision libraries
        # You can use pre-trained models like Haar cascades or deep learning models like YOLO for people detection

        # Update the people_count based on the detection results

        # Display the frame with people count
        cv2.putText(frame, f'People Count: {people_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Environment Monitoring', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    return people_count

# Function to speak the people count
def speak_people_count(people_count):
    engine.say(f"There are {people_count} people in the environment.")
    engine.runAndWait()

# Function to respond to the question "What can you do?"
def describe_capabilities():
    speak("I can perform various tasks, such as opening websites, answering questions, providing information from the web, playing music, and more. You can ask me to do something specific, and I'll do my best to assist you.")

# Function to open Safari
def open_safari():
    try:
        subprocess.run(["open", "-a", "Safari"])
    except Exception as e:
        print("Error:", e)
# Function to open the App Store
def open_app_store():
    try:
        subprocess.run(["open", "-a", "App Store"])
    except Exception as e:
        print("Error:", e)

# Function to fetch the latest news
def get_latest_news():
    news_api_key = "47156559aded4b2ca80bcc2f581b4687"  # Replace with your actual API key
    news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    
    response = requests.get(news_url)
    news_data = json.loads(response.text)

    if news_data.get("status") == "ok":
        articles = news_data.get("articles")
        if articles:
            speak("Here are the latest news headlines:")
            for i, article in enumerate(articles):
                if i < 5:
                    title = article.get("title")
                    speak(f"{i + 1}. {title}")
        else:
            speak("I couldn't find any news articles at the moment.")
    else:
        speak("I encountered an error while fetching news. Please try again later.")

# Function to provide an introduction when asked "Who are you?"
def introduce():
    speak("I am Kevin, your personal voice assistant. I can assist you with various tasks and answer your questions. Some of the things I can do include searching the web, opening websites, providing information, and much more.")


# Function to perform calculations
def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Sorry, I encountered an error while calculating: {str(e)}"

# Function to add a task to a project
def add_task(project_name, task):
    if project_name not in projects:
        projects[project_name] = []
    projects[project_name].append(task)

# Function to list tasks in a project
def list_tasks(project_name):
    if project_name in projects:
        tasks = projects[project_name]
        if not tasks:
            print(f"No tasks found in '{project_name}'.")
        else:
            print(f"Tasks in '{project_name}':")
            for i, task in enumerate(tasks, start=1):
                status = "✔" if task["completed"] else "❌"
                print(f"{i}. [{status}] {task['description']}")
    else:
        print(f"Project '{project_name}' does not exist.")

# Function to mark a task as completed
def complete_task(project_name, task_index):
    if project_name in projects and 1 <= task_index <= len(projects[project_name]):
        task = projects[project_name][task_index - 1]
        print(f"Completed task: {task}")
        projects[project_name].pop(task_index - 1)
    else:
        print("Task not found.")


# Function to define a word
def define_word(word):
    try:
        definition = dictionary.meaning(word)
        if definition:
            speak(f"The definition of {word} is: {', '.join(definition[word])}")
        else:
            speak("I couldn't find a definition for that word.")
    except Exception as e:
        speak("I encountered an error while defining the word. Please try again later.")         

# Function to get weather data from OpenWeatherMap API
def get_weather(location):
    api_key = '5ea46a37aa633eb603bc3459bd08d769'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': location,
        'units': 'metric',  # Use 'imperial' for Fahrenheit
        'appid': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data['cod'] == 200:
            return data
        else:
            return None
    except Exception as e:
        print("Error fetching weather data:", e)
        return None

# Function to get system information
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    system_info = f"CPU Usage: {cpu_percent}%\n"
    system_info += f"Memory Usage: {memory_info.percent}%\n"
    system_info += f"Total Disk Space: {disk_info.total / (1024 ** 3):.2f} GB\n"
    system_info += f"Used Disk Space: {disk_info.used / (1024 ** 3):.2f} GB\n"
    system_info += f"Free Disk Space: {disk_info.free / (1024 ** 3):.2f} GB"

    return system_info

# Function to send a WhatsApp message
def send_whatsapp_message(recipient_name, message):
    try:
        # Use pywhatkit to send the WhatsApp message
        # Replace 'your_country_code' with your country code (e.g., +1 for the USA)
        # and 'your_whatsapp_number' with your WhatsApp number
        pywhatkit.sendwhatmsg(f"+2349070067842", message, 0, 0)
        speak_properly(f"Message sent to {recipient_name} on WhatsApp.")
    except Exception as e:
        print("Error sending WhatsApp message:", e)
        speak_properly("I encountered an error while sending the WhatsApp message. Please try again later.")

# Function to show instructions on how to subscribe to YouTube
def show_subscribe_instructions():
    # You can display instructions on how to subscribe to YouTube.
    # This can be done using a GUI or by opening a web page with instructions.
    # Implement the logic to show instructions here.
    
    # For demonstration purposes, we'll print a message.
    print("To subscribe to a YouTube channel, visit the channel's page and click the 'Subscribe' button.")
    speak("To subscribe to a YouTube channel, visit the channel's page and click the 'Subscribe' button.")

# Function to call someone on WhatsApp
def call_on_whatsapp(recipient_number):
    try:
        # Use pywhatkit to make a WhatsApp call
        # Replace 'your_country_code' with your country code (e.g., +1 for the USA)
        pywhatkit.call_on_whatsapp(f"+2349070067842", recipient_number)
        speak_properly(f"Calling {recipient_number} on WhatsApp.")
    except Exception as e:
        print("Error making WhatsApp call:", e)
        speak_properly("I encountered an error while making the WhatsApp call. Please try again later.")

class VitalsMonitor:
    def __init__(self):
        self.blood_toxicity = 0
        self.heart_rate = 0
        self.blood_pressure = "120/80"

    def update_vitals(self):
        # Simulate random changes in vitals for demonstration purposes
        self.blood_toxicity = random.uniform(0, 1)  # Simulate blood toxicity between 0 and 1
        self.heart_rate = random.randint(60, 100)  # Simulate heart rate between 60 and 100
        self.blood_pressure = f"{random.randint(90, 140)}/{random.randint(60, 90)}"  # Simulate blood pressure

    def get_vitals(self):
        return {
            "blood_toxicity": self.blood_toxicity,
            "heart_rate": self.heart_rate,
            "blood_pressure": self.blood_pressure
        }

# Create a VitalsMonitor instance
vitals_monitor = VitalsMonitor()

# Function to monitor vitals
def monitor_vitals():
    vitals_monitor.update_vitals()
    vitals = vitals_monitor.get_vitals()
    return vitals


# Function to get a random joke from an API
def get_random_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()  # Check for HTTP request errors

        joke_data = response.json()
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        return setup + " " + punchline
    except requests.exceptions.RequestException as req_ex:
        print("Request error:", req_ex)
    except json.JSONDecodeError as json_ex:
        print("JSON decoding error:", json_ex)
    except KeyError as key_error:
        print("Key error:", key_error)
    except Exception as e:
        print("Error fetching joke:", e)
    
    # Return a default joke if an error occurs
    return "Why did the chicken cross the road? To get to the other side!"

# Example usage:
joke = get_random_joke()
speak_properly(joke)


# Function to fetch a summary from Wikipedia
def wikipedia_summary(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple interpretations. Please specify your question."
    except wikipedia.exceptions.PageError as e:
        return "I couldn't find information on that topic."



# Main loop for listening to voice commands
if __name__ == "__main__":
    speak_properly("Would you like to sign up or log in?.If you want to use me say sign up or login")
    while True:
        command = listen_for_command()
        print("You said:", command)
        process_command(command)