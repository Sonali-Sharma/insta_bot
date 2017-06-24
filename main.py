import requests      #importing the request library to use get and json method
import urllib  #importing urllib to download media files
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from keys import APP_ACCESS_TOKEN           #importing the access token so that in future changes have  to  be made at one place only

BASE_URL = 'https://api.instagram.com/v1/'



def self_info():            #getting data for the user
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)   #used to contruct the request url...contructing the end point
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()        #this will give us the response object....method chain is implemented
    print  user_info
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_user_id(insta_username):        #function to get the user id of a person
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)     #creating the url to access search endpoint
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()        #issuing get request...getting response object and than calling json method

    if user_info['meta']['code'] == 200:        #checking for the status code
        if len(user_info['data']):
            return user_info['data'][0]['id']       #taking the userid from response
        else:
            print "user does not exist"
            return None

    else:
        print 'Status code is not 200!'
        exit()



def get_user_info(insta_username):      #function to get info of user by user name
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'



def get_own_post():     #function to get our own post
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)      #creating the url and appending the self endpoint...self refers to the owner of access token
    #appending the access token above
    print 'Requesting data from : %s' % (request_url)#REQUESTING DATA FROM REQUEST URL
    own_media = requests.get(request_url).json()        #USING REQUEST LIBRARY TO GET REQUEST..URL IS GIVEN  IN FUNCTION ARGUMENT..IMPROTING IT INTO A JSON FORMAT

    if own_media['meta']['code'] == 200:#CHECKING THE CORRECT RESPONSE CODE
        if len(own_media['data'])>0:      #extracting id of first element
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code 200 is not received'



def get_user_post(insta_username):     # getting the recent post of a user...same as above function..only user id id also extracted here
    user_id = get_user_id(insta_username)       #extracting the user id
    if user_id == None:     #check for id exist or not
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'request url : %s' % (request_url)
    user_media = requests.get(request_url).json()   #using request library..in json format

    if user_media['meta']['code'] == 200:
        if len(user_media['data'])>0:
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']   #accessing keys one by one
            urllib.urlretrieve(image_url, image_name)       #calling function of urllib libraray
            print 'image downloaded!'
        else:
            print 'No Posts!'
    else:
        print 'Status code other than 200 received!'
'''
Function declaration to get the ID of the recent post of a user by username
'''

def get_post_id(insta_username):        # function for gettting ID of the recent post of a user by username
    user_id = get_user_id(insta_username)       #check for valid user id
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)       #to get the media id of various images
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()   #accessing id and converting it to json

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to get the list of people who have like the recent post of a user
'''


def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    likes_info = requests.get(request_url).json()

    if likes_info['meta']['code'] == 200:
        if len(likes_info['data']):
            for x in range(0, len(likes_info['data'])): #accesing index..checking for the length of likes info
                print likes_info['data'][x]['username']
        else:
                print 'No user has liked the post yet!'
    else:
        print 'Status code other than 200 received!'


def like_a_post(insta_username):      #  Function  to like the recent post of a user
    media_id = get_post_id(insta_username)      #extracting media id
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}        #metadata sending to the url..
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()     #  in post issuing a separate payload
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


def get_comment_list(insta_username):  # Function to get the list of comments on the recent post of a user
#samilar to likes functionn
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                print 'Comment: %s || User: %s' % (comment_info['data'][x]['text'], comment_info['data'][x]['from']['username'])
        else:
            print 'There are no comments on this post!'
    else:
        print 'Status code other than 200 received!'

def make_a_comment(insta_username):#Function to make a comment on the recent post of the user
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def delete_negative_comment(insta_username):   # Function to delete negative comments from the recent post

    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])): #naive implementation of how to delete the negative comments
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())#importing textblob..analyser=named parameter
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):#checking for positive and negative sentiment
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Exit"

        choice=raw_input("Enter you choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="c":
            get_own_post()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice=="f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice=="g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice=="h":
            insta_username = raw_input("Enter the username of the user: ")
            make_a_comment(insta_username)
        elif choice=="i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice=="j":
            exit()
        else:
            print "wrong choice"

start_bot()