import tweepy
import tabula.io #pip install -q tabula-py
#Add your credentials here
import datetime

def writecases(Date, ID):
    
    file_loc="https://drive.google.com/uc?export=download&id="+ID
    tables=tabula.io.read_pdf(file_loc,pages='1,5',lattice=True)
    Districts=tables[7].copy()
    Districts.columns=range(1,28)
    dropColumns=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,21, 22,23,24,25,26,27]
    dropRows=[0,1 ,32,33]
    Districts.drop(index=dropRows,columns=dropColumns,inplace=True)
    Districts.columns=["Date", "District Name",	"Todays Positives",	"Total Positives" ,	"Today’s Discharges" ,	"Total Discharges",  	"Total Active Cases",  	"Today’s Reported Covid Deaths", 	"Total Covid Deaths"]
    Districts['District Name'][12]="Dakshina Kannada"
    Districts['Date']=Date
    Districts.to_csv('districts.csv', index=False, mode='a', header=False)
    
    OverallData=tables[0].loc[[6,7,9,11,13,15,17,19,21,23]][['Unnamed: 6']].transpose()
    OverallData[6]=Date
    OverallData.to_csv('summary.csv', index=False, mode='a', header=False)



twitter_keys = {
        'consumer_key':        ##,
        'consumer_secret':     ##,
        'access_token_key':    ##,
        'access_token_secret': 
    }

#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

API = tweepy.API(auth)

#API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
karnatakaHealthDept=API.user_timeline("DHFWKA",count=30)

for tweets in karnatakaHealthDept:
    if tweets.text.startswith('Today'):
        link=tweets.entities['urls'][0]['expanded_url']
        #Get the PDF ID in google drive
        add=datetime.timedelta(hours=5,minutes=30)
        Date=tweets.created_at+add
        ID=link.split('/',6)[5]
        writecases(Date, ID)
        break
        
        
           
#Use Tabula to read the table
