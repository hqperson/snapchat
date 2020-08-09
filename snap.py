import requests,time,colorama,json,random,string
from colorama import Fore,init
init()

class report:
    def __init__(self):
        self.session = requests.Session()
        self.site_key = "6Ldt4CkUAAAAAJuBNvKkEcx7OcZFLfrn9cMkrXR8"
        self.url = "https://support.snapchat.com/"
        self.contents = open('config.json', 'r',encoding="latin-1",errors='ignore')
        self.data = json.load(self.contents)
        self.API_KEY = self.data['api_key']
        self.user = self.data['user']
        self.message = self.data['message']


    def captcha(self):
        try:
            captcha_id = self.session.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(self.API_KEY, self.site_key, self.url)).text.split('|')[1]
            recaptcha_answer = self.session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(self.API_KEY, captcha_id)).text
            print(Fore.YELLOW+"[Solving] captcha solving...")
            while 'CAPCHA_NOT_READY' in recaptcha_answer:
                time.sleep(5)
                recaptcha_answer = self.session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(self.API_KEY, captcha_id)).text
            recaptcha_answer = recaptcha_answer.split('|')[1]
            return recaptcha_answer
        except Exception as e:
            print(e)


    def email_gen(self):
        ran = ('').join(random.choices(string.ascii_letters + string.digits, k=8))
        email = ran+"@gmail.com"
        return email
   
    
    def report(self):
        emails = self.email_gen()
        answer1 = self.captcha()
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Host":"support.snapchat.com",
            "Accept-Encoding":"gzip, deflate",
            "Cookie":"sc_at=v2|H4sIAAAAAAAAAE3GyREAIQgEwIiowuUazQY8ojD4/dqvjk/SsJNE6pCWgnKa08qjfaXE5LpNeTRDdw8D7lP+AR74ykdAAAAA",
            "Content-Type":"multipart/form-data; boundary=---------------------------12981267812913132682039128229"
        }
        data ='''-----------------------------12981267812913132682039128229
Content-Disposition: form-data; name="key"

ts-reported-content-3
-----------------------------12981267812913132682039128229
Content-Disposition: form-data; name="field-24335325"

{}
-----------------------------12981267812913132682039128229
Content-Disposition: form-data; name="field-24380626"

{}
-----------------------------12981267812913132682039128229
Content-Disposition: form-data; name="field-22808619"

{}
-----------------------------12981267812913132682039128229
Content-Disposition: form-data; name="g-recaptcha-response"

{}
-----------------------------12981267812913132682039128229
Content-Disposition: form-data; name="answers"

5153567363039232,5763820408537088,5685771749294080
-----------------------------12981267812913132682039128229--'''.format(emails,self.user,self.message,answer1)
        send_report = self.session.post("https://support.snapchat.com/en-US/api/v2/send",data=data,headers=headers)
        if send_report.status_code==200:
            print(Fore.GREEN+"[Success] reported {}".format(self.user))
        else:
            print(Fore.RED+"[Error] Report could not be sent")

if __name__ == "__main__":
    while True:
        start = report()
        start.report()
