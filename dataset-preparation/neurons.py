import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

personName = 'Suyash Dixit'
fbData = 'y'
googleData = 'y'
linkedInData = 'n'
whatsAppData = 'y'

def getWhatsAppData():
	responseDictionary = dict()
	fbFile = open('mega.txt', 'r', encoding='utf8') 
	allLines = fbFile.readlines()
	myMessage, otherPersonsMessage, currentSpeaker = "","",""
	for index,lines in enumerate(allLines):
	    rightBracket = lines.find('-') + 2
	    justMessage = lines[rightBracket:]
	    colon = justMessage.find(':')
	    # Find messages that I sent
	    if (justMessage[:colon] == personName or justMessage[:colon] == '91 91492 26865' ):
	        if not myMessage:
	            # Want to find the first message that I send (if I send multiple in a row)
	            startMessageIndex = index - 1
	        myMessage += justMessage[colon+2:]
	        
	    elif myMessage:
	        # Now go and see what message the other person sent by looking at previous messages
	        for counter in range(startMessageIndex, 0, -1):
	            currentLine = allLines[counter]
	            rightBracket = currentLine.find('-') + 2
	            justMessage = currentLine[rightBracket:]
	            colon = justMessage.find(':')
	            if not currentSpeaker:
	                # The first speaker not named me
	                currentSpeaker = justMessage[:colon]
	            elif (currentSpeaker != justMessage[:colon] and otherPersonsMessage):
	                # A different person started speaking, so now I know that the first person's message is done
	                otherPersonsMessage = cleanMessage(otherPersonsMessage)
	                myMessage = cleanMessage(myMessage)
	                responseDictionary[otherPersonsMessage] = myMessage
	                break
	            otherPersonsMessage = justMessage[colon+2:] + otherPersonsMessage
	        myMessage, otherPersonsMessage, currentSpeaker = "","",""    
	return responseDictionary

def getGoogleHangoutsData():
        df = pd.read_csv('messages.csv')
        responseDictionary = dict()
        receivedMessages = df[df['conversation__sender'] != 'suyashofficial']
        sentMessages = df[df['conversation__sender'] == 'suyashofficial']
        combined = pd.concat([sentMessages, receivedMessages])
        print(combined['conversation__sender'])
        otherPersonsMessage, myMessage = "",""
        firstMessage = True
        secondMessage = True
        for index, row in df.iterrows():
                if (row['conversation__sender'] != 'suyashofficial'):
                        if secondMessage:
                                if otherPersonsMessage:
                                        secondMessage = False
                                        # Don't include if I am the person initiating the convo
                                        continue
                        if myMessage and otherPersonsMessage:
                                #print(1)
                                otherPersonsMessage = cleanMessage(otherPersonsMessage)
                                myMessage = cleanMessage(myMessage)
                                responseDictionary[otherPersonsMessage.rstrip()] = myMessage.rstrip()
                                otherPersonsMessage, myMessage = "",""
                        otherPersonsMessage = otherPersonsMessage + str(row['conversation__text']) + " "
                        #print(otherPersonsMessage)
                else:
                        if firstMessage or secondMessage:
                                firstMessage = False
                                # Don't include if I am the person initiating the convo
                                continue
                        myMessage = myMessage + str(row['conversation__text']) + " "
                        #print(myMessage)
        return responseDictionary

def getFacebookData():
        df = pd.read_csv('final.csv')
        df['messages.content'].fillna('.',inplace=True)
        responseDictionary = dict()
        receivedMessages = df[df['messages.sender_name'] != personName]
        sentMessages = df[df['messages.sender_name'] == personName]
        combined = pd.concat([sentMessages, receivedMessages])
        print(combined['messages.sender_name'])
        otherPersonsMessage, myMessage = "",""
        firstMessage = True
        secondMessage = True
        for index, row in df.iterrows():
                if (row['messages.sender_name'] != personName):
                        if secondMessage:
                                if otherPersonsMessage:
                                        secondMessage = False
                                        # Don't include if I am the person initiating the convo
                                        continue
                        if myMessage and otherPersonsMessage:
                                #print(1)
                                otherPersonsMessage = cleanMessage(otherPersonsMessage)
                                myMessage = cleanMessage(myMessage)
                                responseDictionary[otherPersonsMessage.rstrip()] = myMessage.rstrip()
                                otherPersonsMessage, myMessage = "",""
                        otherPersonsMessage = otherPersonsMessage + str(row['messages.content']) + " "
                        #print(otherPersonsMessage)
                else:
                        if firstMessage or secondMessage:
                                firstMessage = False
                                # Don't include if I am the person initiating the convo
                                continue
                        myMessage = myMessage + str(row['messages.content']) + " "
                        #print(myMessage)
        return responseDictionary
##
##def getLinkedInData():
##	df = pd.read_csv('Inbox.csv')
##	dateTimeConverter = lambda x: datetime.strptime(x,'%B %d, %Y, %I:%M %p')
##	responseDictionary = dict()
##	peopleContacted = df['From'].unique().tolist()
##	for person in peopleContacted:
##	    receivedMessages = df[df['From'] == person]
##	    sentMessages = df[df['To'] == person]
##	    if (len(sentMessages) == 0 or len(receivedMessages) == 0):
##	        # There was no actual conversation
##	        continue
##	    combined = pd.concat([sentMessages, receivedMessages])
##	    combined['Date'] = combined['Date'].apply(dateTimeConverter)
##	    combined = combined.sort(['Date'])
##	    otherPersonsMessage, myMessage = "",""
##	    firstMessage = True
##	    for index, row in combined.iterrows():
##	        if (row['From'] != personName):
##	            if myMessage and otherPersonsMessage:
##	                otherPersonsMessage = cleanMessage(otherPersonsMessage)
##	                myMessage = cleanMessage(myMessage)
##	                responseDictionary[otherPersonsMessage.rstrip()] = myMessage.rstrip()
##	                otherPersonsMessage, myMessage = "",""
##	            otherPersonsMessage = otherPersonsMessage + row['Content'] + " "
##	        else:
##	            if (firstMessage):
##	                firstMessage = False
##	                # Don't include if I am the person initiating the convo
##	                continue
##	            myMessage = myMessage + str(row['Content']) + " "
##	return responseDictionary

def cleanMessage(message):
	# Remove new lines within message
	cleanedMessage = message.replace('\n',' ').lower()
	# Deal with some weird tokens
	cleanedMessage = cleanedMessage.replace("\xc2\xa0", "")
	# Remove punctuation
	cleanedMessage = re.sub('([.,!?])','', cleanedMessage)
	# Remove multiple spaces in message
	cleanedMessage = re.sub(' +',' ', cleanedMessage)
	return cleanedMessage

combinedDictionary = {}
if (googleData == 'y'):
	print('Getting Google Hangout Data')
	combinedDictionary.update(getGoogleHangoutsData())
if (fbData == 'y'):
	print('Getting Facebook Data')
	combinedDictionary.update(getFacebookData())
if (linkedInData == 'y'):
	print('Getting LinkedIn Data')
	combinedDictionary.update(getLinkedInData())
if (whatsAppData == 'y'):
        print('Getting whatsApp Data')
        combinedDictionary.update(getWhatsAppData())
print('Total len of dictionary', len(combinedDictionary))

print('Saving conversation data dictionary')
np.save('conversationDictionary.npy', combinedDictionary)

conversationFile = open('conversationData.txt', 'w')
for key,value in combinedDictionary.items():
   	conversationFile.write(str(key.strip().encode("utf-8")) + str(value.strip().encode("utf-8")))
conversationFile.close()
