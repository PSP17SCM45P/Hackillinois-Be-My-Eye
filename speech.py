#Python 2.x program for Speech Recognition
 
import speech_recognition as sr
import wave,struct
 
#enter the name of usb microphone that you found
#using lsusb
#the following name is only used as an example
#mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
#Sample rate is how often values are recorded
sample_rate = 48000
#Chunk is like a buffer. It stores 2048 samples (bytes of data)
#here. 
chunk_size = 2048
#Initialize the recognizer
r = sr.Recognizer()

#generate a list of all audio cards/microphones
#mic_list = sr.Microphone.list_microphone_names()

#the following loop aims to set the device ID of the mic that
#we specifically want to use to avoid ambiguity.
#for i, microphone_name in enumerate(mic_list):
    #device_id = i
    
while(1):
    with sr.Microphone(device_index = 2, sample_rate = 44100, chunk_size = 512) as source:
        #wait for a second to let the recognizer adjust the 
        #energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source)
        print("Say Something")
        #listens for the user's input
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("you said: " + text)
            
            if(text=="stop" or text=="STOP"):
                print("Stop speech to text conversion")
                break
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))