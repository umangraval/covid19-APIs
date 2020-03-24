from instabot import Bot
import schedule 
import time
import glob, os

bot=Bot()
bot.login(username="carona_stats",password="CamCann")
def upload_photo():                 
    listofimgs = glob.glob("./Posts/*")
    print(listofimgs)
    img_path = listofimgs[0]
    print(img_path)
    try:
        bot.upload_photo(img_path,caption="#bot #testing loop")
        to_remove_path = img_path+".REMOVE_ME"
        os.remove(to_remove_path)
    except:
        print("err_msg")
    
# # Task scheduling 
schedule.every().day.at("09:00").do(upload_photo) 
schedule.every().day.at("16:00").do(upload_photo) 
schedule.every().day.at("21:00").do(upload_photo) 

# # # Loop so that the scheduling task 
# # # keeps on running all time. 
while True: 
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(1) 
