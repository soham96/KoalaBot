import tweepy
import random

auth = tweepy.OAuthHandler('your Auth', 'token')
auth.set_access_token('your access', 'token')
api=tweepy.API(auth)

def get_fact():
    fact=random.choice(list(open('koala_facts.txt')))
    intro=random.choice(list(open('intro.txt')))

    text=(f"{intro}"
        "\n"
        f"\n{fact}"
        "\nTo save the endangered Koala, do your bit and donate: www.savethekoala.com")
    return text
    
class CustomTwitterStream(tweepy.StreamListener):

    def on_status(self, status):
        #import ipdb; ipdb.set_trace()
        if status.retweeted == False and status.in_reply_to_status_id == None and status.in_reply_to_status_id_str==None and status.in_reply_to_user_id== None and status.in_reply_to_user_id_str ==None and status.in_reply_to_screen_name == None:
            if "RT @" not in status.text:
                api.update_status(status=f'@{status.user.screen_name} {get_fact()}', in_reply_to_status_id=status.id)
                print(status.text)

    def on_error(self, status_code):
        print(status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream
        
stream_api = tweepy.streaming.Stream(auth, CustomTwitterStream(), timeout=60)
print("Starting Stream")
stream_api.filter(track=[" Koalas ", " Koala ", " koalas ", " koala "], is_async=True)
