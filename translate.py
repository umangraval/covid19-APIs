from googletrans import Translator
translator = Translator()
text = "the numbers on the map show the count of affected individuals (both indian and foreign nationalists) dead or alive"
trans = []

t = translator.translate(text, dest='gu')
print(t)
# en - english
# gu - gujarati 
# bn - bengali
# hi - hindi
# kn - kannada
# pa - punjabi
# sd - sindhi
# ta - tamil 
# te - telugu
