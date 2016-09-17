import praw, webbrowser, time, webbrowser, pyimgur, sys
from imgurpython import ImgurClient
from colorama import init
from termcolor import colored
from gfycat.client import GfycatClient
init() #Initialize the color fix
client_id = ''
client_secret = ''
access_token = ''
refresh_token = ''

im = pyimgur.Imgur(client_id)
client = ImgurClient(client_id, client_secret, access_token, refresh_token)
clientt = GfycatClient() #Gfycat client for query_gfy
im = pyimgur.Imgur(client_id)
client = ImgurClient(client_id, client_secret, access_token, refresh_token)
im.change_authentication(client_id=client_id, client_secret=client_secret, access_token=access_token, refresh_token=refresh_token)
r = praw.Reddit(user_agent='imagingB0t') # Note: Be sure to change the user-agent to something unique.

sub = raw_input("Subreddit: ") #Subreddit to pick images from
maxx = int(raw_input("Max images: ")) #Take this input as an int and use it for the limit of images
submissions = r.get_subreddit(sub).get_hot(limit=99999) #Use this as an infinite value and then sys.exit() when count == maxx

fields = {}
fields['title'] = "imagingBot"
fields['description'] = "imagingBot"
fields['privacy'] = 'public'

try: #Create an album using the above fields
    x = client.create_album(fields)
except Exception as e:
    print colored(e, "red")
    sys.exit()

count = 0
print colored(str(x)[45:].strip("'}"), "green")
cleanid = str(x)[45:].strip("'}")

for submission in submissions:
    if "imgur.com" in submission.url: #Check if it's an imgur link
        try:
            clean = submission.url.rsplit("/", 1)[1] #Get imgur image ID
            client.album_add_images(cleanid, clean) #Add the images to the album "cleanid"
            print colored(clean, "cyan")
        except:
            print colored("Timing out", "red")
            time.sleep(15)

    elif "gfycat.com" in submission.url: #Check if it's a gfycat link
        try:
            clean = submission.url.rsplit("/", 1)[1] #Get gfy id
            rr = clientt.query_gfy(clean) #Query the gif "clean"
            url = rr['gfyItem']['max5mbGif'] #Find the url for the 5mb gif (larger files don't get added)
            im.upload_image(url=url, album=cleanid) #Upload to album from url using pyimgur
            print colored(clean, "cyan")
        except:
            print colored("Timing out", "red")
            time.sleep(15)

    for image in client.get_album_images(cleanid): #For every image in this new album, add 1 to count
        count = count + 1

    if int(count) == maxx: #Check if the amount of images from the album is == maxx
        print colored(str(count) + " images were successfully added to album " + cleanid, "green")
        client.album_favorite(cleanid) #Favorite the album (buggy)
        webbrowser.open_new("https://imgur.com/a/" + cleanid) #Open the album
        sys.exit() #Close the program

    elif int(count) != maxx: #We've added count, and if it's not equal we need to reset it for the next loop.
        count = 0
