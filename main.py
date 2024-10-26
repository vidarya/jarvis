import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests


recognizer=sr.Recognizer()
engine = pyttsx3.init()
NEWS_API_KEY = "1f71f9cbea8c4822bb944e65cbe4e67c"

is_playing_music = False
is_reading_news = False


def speak(text):
    engine.say(text)
    engine.runAndWait() 

def get_latest_news():
    global is_reading_news
    is_reading_news = True 
    # Using the 'everything' endpoint with a query for "India"
    url = f"https://newsapi.org/v2/everything?q=india&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        news_data = response.json()
        
        # Check if articles are present in the response
        if "articles" in news_data and news_data["articles"]:
            articles = news_data["articles"][:5]  # Get the top 5 news articles
            news_list = [article["title"] for article in articles]
            
            for i, news in enumerate(news_list, start=1):
                if is_reading_news:  # Check if we should continue reading
                    speak(f"News {i}: {news}")
                else:
                    break  # Stop reading if 'stop' command was given
        else:
            speak("I'm sorry, I couldn't find any news articles.")
    except Exception as e:
        speak("I'm sorry, I couldn't fetch the latest news at this moment.")
    finally:
        is_reading_news = False  # Reset after reading news




def processCommand(c):
    global is_playing_music, is_reading_news
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif(c.lower().startswith("play")):
        global is_playing_music 
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
        is_playing_music = True
    elif "news" in c.lower():
        speak("Fetching the latest news from India...")
        get_latest_news()
    elif "stop" in c.lower():
        # Stop music or news based on what's active
        if is_playing_music:
            is_playing_music = False
            speak("Stopping the music.")
            # Logic to stop the music in the browser can be handled separately
            # (e.g., manually stop or pause in the browser)
        if is_reading_news:
            is_reading_news = False
            speak("Stopping the news.")
        if not is_playing_music and not is_reading_news:
            speak("Nothing is currently playing.")





if __name__=="__main__":
    speak("Initializing Jarvis...")
    while True:

        #Listen for the wake word Jarvis
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("recognizing...")
        

        
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word=r.recognize_google(audio)
            if(word.lower()=='jarvis'):
                speak("Ya")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)

            
        
        except Exception as e:
            print("Error; {0}".format(e))
