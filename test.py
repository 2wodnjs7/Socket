from datetime import datetime, timezone

msgDATE = 'Date: ' + str(datetime.now().strftime('%a, %d %b %Y %X %Z'))
print(datetime.now().astimezone("Asia/Seoul").strftime('%a, %d %b %Y %X %Z'))
print(msgDATE)