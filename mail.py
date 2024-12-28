import smtplib

# server = smtplib.SMTP("smtp.gmail.com",587)


# server.starttls()
# server.login("d.avinashkumar22@gamil.com","AMS123ams123")
# server.sendemail("d.avinashkumar22@gamil.com","r190885@rguktrkv.ac.in","Mail receiced from python code")

# print("Mail sent")

email = input("Sender Email: ")
receiver_email = input("Receiver Email: ")

subject = input("Subject: ")
message = input("Message: ")

text = f"Subject {subject}\n\n {message}"

server = smtplib.SMTP("smtp.gmail.com",587)

server.starttls()

server.login(email,"dyls ombd uyfc ncuu")

server.sendmail(email,receiver_email,text)
print("Mail sent")