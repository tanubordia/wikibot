#coding:UTF-8
import os
import time
from slackclient import SlackClient
import urllib2
from stripogram import html2text
import requests

BOT_ID = "XXXXXXXXX" #your bot id

AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") #your client id

def handle_command(command, channel):
    command = command.title()
    a = command.split()
    a = '_'.join(a)
    src="https://en.wikipedia.org/wiki/"+str(a)
    try:
        respon=urllib2.urlopen(src)
        page_source=respon.read()
    except urllib2.HTTPError:
        response = "Sorry! We couldn't find the keyword that you tried searching for. Please try again."
    else:
        for item in page_source.split("</p>"):
            if "<p>" in item:
                x=item[item.find("<p>")+len("<p>"):]
                break
    
        txt=html2text(x)
        l=txt.split(" ")
        k=len(l)
        if(k>50):
            response = txt+"\nFor more info:"+src
        else:
            for item in page_source.split("</ul>"):
                if "<ul>" in item:
                    x=item[item.find("<ul>")+len("<ul>"):]
                    break
            text=html2text(x)
            response = txt+text+"\nFor more info:"+src
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect(): #establish connection
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read()) #read user input and send arguement to parse_slack_output() function
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
