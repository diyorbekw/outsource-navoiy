import mailtrap as mt

mail = mt.Mail(
    sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
    to=[mt.Address(email="diyorbek0143@gmail.com")],
    subject="You are awesome!",
    text="Congrats for sending test email with Mailtrap!",
    category="Integration Test",
)

client = mt.MailtrapClient(token="809cb340cce8eb80f63ac91fd5195e50")
response = client.send(mail)

print(response)