#importing packages and installing if not available
try:
    import speech_recognition as sr
    import smtplib
    from bs4 import BeautifulSoup
    import email
    import imaplib
    from gtts import gTTS
    import pyglet
    import os, time
    import pyaudio
except:
    import os
    os.system('pip install -r requirements.txt')
finally:
    import speech_recognition as sr
    import smtplib
    from bs4 import BeautifulSoup
    import email
    import imaplib
    from gtts import gTTS
    import pyglet
    import os, time


# default values
calling_word = 'naveen'
emailID = "chennaiprince66@gmail.com"
password = "9092680809@a"


#voice recognition part
r=sr.Recognizer()
r.pause_threshold = 1.0
r.energy_threshold = 4000
r.dynamic_energy_threshold = True

#login from os
login = os.getlogin
print ("You are logging from : "+login())


def speak(text):
    tts = gTTS(text=text, lang='en') #voice out
    tts.save("audio.mp3")
    music = pyglet.media.load("audio.mp3", streaming = False)
    music.play()
    time.sleep(music.duration)
    os.remove("audio.mp3")


def listening():
    text = ''
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio=r.listen(source)
            try:
                print("converting....")
                text=r.recognize_google(audio, language = "en").lower()
                print(text)
                return text
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                break
            print("You are not audible, try again:")


# Acknowlegment function
def ackno(i):
    print("Shall i continue : (Yes/No) : ")
    text = listening().lower()
    if 'no' in text:
        return False
    elif 'yes' in text or 's' in text:
        return True
    else:
        print("Wrong Option!! \nTry Again......")
        if i<3:
            ackno(i+1)
        else:
            main()


# Call function
def call():
     text = listening().lower()
     if calling_word.lower() in text:
         print("Composed a mail.")
         print("Check your inbox")

         speak("Option 1. Composed a mail.")
         speak("Option 2. Check your inbox")
         speak("What do you want to do ?")
         for i in range(0,3):
             x = listening().lower()
             if 'compose' in x:
                 composemail()
                 break
             elif 'read inbox' in x:
                 readmail()
                 break
             elif 'quit' in text or 'exit' in text or 'close' in text:
                 exit(0)
             else:
                 print("Wrong Option!!!!!.....Try Again")
     elif 'quit' in text or 'exit' in text or 'close' in text:
         exit(0)
     else:
         call()

def getVictimMailID():
    mailId = ''
    print("please spell out the mailid letter by letter and say `done` when completed")
    print("And mail will be appended with `@gmail.com` automatically")
    while True:
        char = listening()
        if "done" in char.lower():
            break
        char = char.split(" ")
        if len(char) > 1:
            print("Try Again:")
            continue
        if ackno(2):
            mailId = mailId + char[0].lower()
        else:
                print("Try Again:")
                continue
        print(mailId)
    mailId = mailId + "@gmail.com"
    print(f"\n\nThe MailId is : {mailId}")
    if ackno(2):
        return mailId

    getVictimMailID()


def composemail():

    mail = smtplib.SMTP('smtp.gmail.com',587)    #host and port area
    mail.ehlo()  #Hostname to send for this command defaults to the FQDN of the local host.
    mail.starttls() #security connection
    mail.login(emailID, password) #login part
    msg , subject = '', ''
    while True:
        print ("Your subject :")
        subject = listening()
        print ("You said : "+subject)
        if ackno(0):
            break

    while True:
        print ("Your message :")
        msg = listening()
        print ("You said : "+msg)
        if ackno(0):
            break

    message = f"""Subject: {subject}

        {msg}."""

    reciverid = getVictimMailID()
    mail.sendmail(emailID,reciverid,message) #send part
    print ("Congrates! Your mail has send. ")
    # speak("Congrates! Your mail has send. ")
    mail.close()


def readmail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993) #this is host and port area.... ssl security
    mail.login(emailID, password)  #login
    stat, total = mail.select('Inbox')  #total number of mails in inbox
    # print ("Number of mails in your inbox :"+str(total))


    #unseen mails
    stat, unseen = mail.search(None, '(UNSEEN)') # unseen count
    # print ("Number of UnSeen mails :"+str(unseen))
    print(type(unseen))
    unseen = str(unseen[0]).split(" ")
    print(len(unseen))
    # speak("Your Unseen mail : ")
    #
    # #search mails
    # result, data = mail.uid('search',None, "ALL")
    # inbox_item_list = data[0].split()
    # new = inbox_item_list[-1]
    # old = inbox_item_list[0]
    # result2, email_data = mail.uid('fetch', new, '(RFC822)') #fetch
    # raw_email = email_data[0][1].decode("utf-8") #decode
    # email_message = email.message_from_string(raw_email)
    # print ("From: "+email_message['From'])
    # print ("Subject: "+str(email_message['Subject']))
    # tts = gTTS(text="From: "+email_message['From']+" And Your subject: "+str(email_message['Subject']), lang='en')
    # ttsname=("mail.mp3")
    # tts.save(ttsname)
    # music = pyglet.media.load(ttsname, streaming = False)
    # music.play()
    # os.remove(ttsname)
    #
    # #Body part of mails
    # stat, total1 = mail.select('Inbox')
    # stat, data1 = mail.fetch(total1[0], "(UID BODY[TEXT])")
    # msg = data1[0][1]
    # soup = BeautifulSoup(msg, "html.parser")
    # txt = soup.get_text()
    # print ("Body :"+txt)
    # tts = gTTS(text="Body: "+txt, lang='en')
    # ttsname=("body.mp3")
    # tts.save(ttsname)
    # music = pyglet.media.load(ttsname, streaming = False)
    # music.play()
    # os.remove(ttsname)
    mail.close()
    mail.logout()


def main():
    try:
        #fetch project name
        call()
    except KeyboardInterrupt:
        print("closing program")
        exit(0)


if __name__ == '__main__':
    speak("Project: Voice based Email for blind")
    main()
