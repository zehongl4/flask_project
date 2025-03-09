from flask_mail import Message
from flask import current_app
from .. import mail

def send_verification_email(email, verification_code):
    current_app.logger.info("=== Starting email sending process ===")
    current_app.logger.info(f"Sending to email: {email}")
    
    try:
        # configuration info
        current_app.logger.info(f"Mail server: {current_app.config.get('MAIL_SERVER')}")
        current_app.logger.info(f"Mail port: {current_app.config.get('MAIL_PORT')}")
        current_app.logger.info(f"Mail use TLS: {current_app.config.get('MAIL_USE_TLS')}")
        current_app.logger.info(f"Mail username: {current_app.config.get('MAIL_USERNAME')}")
        
        msg = Message('Your Verification Code',
                     sender=current_app.config['MAIL_USERNAME'],
                     recipients=[email])
        
        current_app.logger.info("Message object created")
        
        msg.body = f'''Your verification code is: {verification_code}
        Please do not share this code with anyone.
        This code will expire in 10 minutes.
        '''
        
        current_app.logger.info("Attempting to send email...")
        mail.send(msg)
        current_app.logger.info("Email sent successfully")
        return True
        
    except Exception as e:
        # details errors
        current_app.logger.error(f"Error type: {type(e).__name__}")
        current_app.logger.error(f"Error message: {str(e)}")
        current_app.logger.error(f"Error details: ", exc_info=True)  
        return False