#This program uses Reddit's JSON storage to find a user's most recent comment.
#Honestly, this could have been done easier using PRAW, or some similar library, but I was looking for something new and different.

import json
import urllib2

from Tkinter import *

root = Tk()

screenW = root.winfo_screenwidth()
screenH = root.winfo_screenheight()

#Create the window.
root.title("Recent Reddit Comment")
root.iconbitmap("speech.ico")
root.configure(background="white")
app = Frame(root,bg="white")
app.grid()

lblEnterName = Label(app,text="Enter a Username: ",bg="white",padx=100)
txtUser = Entry(app,bd=4,bg="white",relief="sunken")

lblMostRecentComment = Label(app,text="",wraplength=screenW/2,font=('Comic Sans MS',10),bg="white")

def getData():
    txtInput = txtUser.get()
    url = "http://www.reddit.com/u/" + txtInput + ".json"
    try:
        #User exists
        data = json.load(urllib2.urlopen(url)) #Stores the info from the JSON file.
        data = str(data) #Makes it a String so we can actually do stuff to it.
        lblEnterName.configure(text="Enter a Username: ",fg="black")
        if "body" in data: #"body" is used to hold the value of the comment. This finds the most recent one.
            #If true, then a comment exists on the account! Yay!
            bodyindex = data.index("body")
            recentComment = data[bodyindex+9] #We start at 9 because there are some miscellaneous characters in the way of our comment.
            count = 10
            while True:
                if data[bodyindex+count:bodyindex+count+18] == '", u\'link_title\': ' or data[bodyindex+count:bodyindex+count+18] == "', u\'link_title\': ":
                    break #"u\'link_title\':" is shown after the comment, so if we find it, then we finished getting the comment.
                elif data[bodyindex+count:bodyindex+count+2] == "\\n": #This just takes care of the newline escape character.
                    recentComment = recentComment + "\n"
                    count = count + 1
                else:
                    recentComment = recentComment + data[bodyindex+count] #Parses each individual character from the comment to a String.
                count = count + 1
            lblMostRecentComment.configure(text=recentComment) #Displays the comment in our Label.
    except urllib2.HTTPError as e:
        #User does not exist, or we can't connect to the server.
        lblEnterName.configure(text="Invalid! (User doesn't exist, or can't connect to server.) Try again.",fg="red")

btnGo = Button(app,text="Get Comment",command=getData)

lblEnterName.grid()
txtUser.grid()
btnGo.grid()
lblMostRecentComment.grid()

root.mainloop()
