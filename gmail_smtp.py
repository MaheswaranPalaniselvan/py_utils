import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    # Create the MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Open the file to be sent
    with open(attachment_path, 'rb') as attachment:
        # Create MIMEBase instance
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode the attachment in base64
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')

    # Attach the file to the message
    msg.attach(part)

    try:
        # Establish a connection with Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {str(e)}")

# Usage Example
sender_email = 'aaaaaaaaa@gmail.com'
sender_password = 'toga uzoz pptr sbpe'
receiver_email = 'aaaaaaaaa@gmail.com'
subject = 'PDF FILE'
body = 'Here we have attached your pdf file'
attachment_path = 'C:\\Users\\aaaaaaaaa\\Downloads\\test.pdf'  # Replace with the path to your file

send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment_path)
