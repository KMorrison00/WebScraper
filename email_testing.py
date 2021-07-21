import yagmail

yagmail.register('kyle.pyprojects@gmail.com', 'projectG12')
yag = yagmail.SMTP("kyle.pyprojects@gmail.com")
reciever = "kyle.pyprojects@gmail.com"

body = "big test \n " \
       "arbtsdf \n " \
       "askjhajsdha"
yag.send(
    to=reciever,
    subject="Arb alert",
    contents=body
)