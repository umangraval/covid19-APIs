from instabot import Bot
import schedule 
import time
import glob, os

bot=Bot()
langs = ['english','hindi','telugu','marathi','kannada','guj','bengali','urdu','tamil','malayalam']
accounts = {
    'coro.na.tion': 'Statewise covid19 incidences as per ministry of health and welfare government of india.',
    'coro.na.tion_hindi': 'राज्यवार covid19 भारत के स्वास्थ्य और परिवार कल्याण सरकार के मंत्रालय के अनुसार',
    'coro.na.tion_telugu': 'భారతదేశం యొక్క ఆరోగ్య మరియు కుటుంబ సంక్షేమ ప్రభుత్వ మంత్రిత్వ శాఖ ప్రకారం రాష్ట్రవ్యాప్తంగా కోవిడ్ 19 సంఘటనలు',
    'coro.na.tion_marathi': 'भारत सरकारच्या आरोग्य व कुटुंब कल्याण मंत्रालयाच्या अनुसार राज्यस्तरीय कोविड 19 घटना',
    'coro.nat.tion_kannada': 'ಭಾರತದ ಆರೋಗ್ಯ ಮತ್ತು ಕುಟುಂಬ ಕಲ್ಯಾಣ ಸರ್ಕಾರದ ಸಚಿವಾಲಯದ ಪ್ರಕಾರ ರಾಜ್ಯವ್ಯಾಪಿ ಕೋವಿಡ್ 19 ಘಟನೆಗಳು',
    'coro.na.tion_guj': 'ભારત સરકારના આરોગ્ય અને પરિવાર કલ્યાણ મંત્રાલય મુજબ રાજ્યવ્યાપી કોવિડ 19 ઘટનાઓ',
    'coro.na.tion_bengali': 'ভারতের স্বাস্থ্য ও পরিবার কল্যাণ মন্ত্রনালয় অনুসারে রাষ্ট্রীয়ভাবে কোভিড ১৯ টি ঘটনা',
    'coro.na.tion_urdu': 'وزارت صحت اور کنبہ بہبود حکومت ہند کے مطابق اسٹیٹ وائی کوڈ 19 واقعات',
    'coro.na.tion_tamil': 'இந்திய சுகாதார அமைச்சகம் மற்றும் குடும்ப நல அரசாங்கத்தின் படி மாநில அளவிலான கோவிட் 19 சம்பவங்கள்',
    'coro.na.tion_malayalam': 'ആരോഗ്യ മന്ത്രാലയം, ഇന്ത്യയിലെ കുടുംബക്ഷേമ സർക്കാർ എന്നിവ പ്രകാരം സംസ്ഥാനതലത്തിൽ covid19 സംഭവങ്ങൾ'
    }
#bot.login(username="carona_stats",password="CamCann")

def upload_photo():
    os.system("python map_generator.py")                 
    try:
        for key, value in accounts.items():
            print(key,value)
            bot.login(username=key,password="CoronaCann09")
            listofimgs = glob.glob("./Posts/*")
            img_path = listofimgs[0]
            bot.upload_photo(img_path,caption=value)
            to_remove_path = img_path+".REMOVE_ME"
            os.remove(to_remove_path)
            bot.logout(username=key,password="CoronaCann09")
    except:
        print("err_msg")
    
# # Task scheduling 
schedule.every().day.at("10:20").do(upload_photo) 
schedule.every().day.at("16:00").do(upload_photo) 
schedule.every().day.at("21:00").do(upload_photo) 

# # # Loop so that the scheduling task 
# # # keeps on running all time. 
while True: 
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(1) 
