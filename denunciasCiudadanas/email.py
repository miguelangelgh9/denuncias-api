#Sacado de: http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
def send_email(recipient, body):
    import smtplib
    user="too115noreply@gmail.com"
    pwd="CONTRASEÑA"
    gmail_user = user
    gmail_pwd = pwd
    FROM = 'GRUPO 13'
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = "Actualizacion sobre el estado de su denuncia!"
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        #print 'successfully sent the mail'
        return "Enviado con exito."
    except:
        return "No se pudo enviar."
