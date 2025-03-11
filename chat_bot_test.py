import chat_bot
import responses
import sys



user_response = sys.argv[1]
user_id = 1
res =  responses.getResponses('./files/responses.csv')

bot =  chat_bot.Bot(user_id, res, True)

print(bot.send_response(user_response))

