# Import require dependencies
import os
import base64
import re
import smtplib
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.cloud import language_v1
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] # Gmail API scope for reading emails

# Authenticates and returns the Gmail API service object
def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# Fetches customer feedback emails from the Gmail inbox
def fetch_feedback_emails(service):
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        msg_data = msg['payload']['parts'][0]['body']['data']
        msg_body = base64.urlsafe_b64decode(msg_data.encode('UTF-8')).decode('UTF-8')
        
        print(f"Email Body: {msg_body}")
        yield msg_body

# Analyzes sentiment of the feedback text
def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    
    print(f"Sentiment score: {sentiment.score}, Sentiment magnitude: {sentiment.magnitude}")
    return sentiment.score

# Extracts customer name, order ID, and feedback category from the email body
def extract_data(email_body):
    name = re.search(r'Dear (\w+)', email_body)
    order_id = re.search(r'Order ID: (\d+)', email_body)
    feedback_category = 'Unknown'
    
    if "product" in email_body.lower():
        feedback_category = 'Product'
    elif "service" in email_body.lower():
        feedback_category = 'Service'
    elif "delivery" in email_body.lower():
        feedback_category = 'Delivery'
    
    return {
        'name': name.group(1) if name else 'Unknown',
        'order_id': order_id.group(1) if order_id else 'Unknown',
        'category': feedback_category
    }

# Insert extracted data in a google form
def submit_to_google_form(customer_name, order_id, feedback_category, sentiment_score):
    google_form_url = "https://docs.google.com/forms/d/e/[YOUR_FORM_ID]/formResponse" # Demo URL
    form_data = { # Demo Form Data
        'entry.1234567890': customer_name,
        'entry.0987654321': order_id,
        'entry.1122334455': feedback_category,
        'entry.6677889900': sentiment_score
    }
    
    response = requests.post(google_form_url, data=form_data)
    if response.status_code == 200:
        print("Form submitted successfully!")
    else:
        print("Failed to submit form")

# Sends summary email with feedback details
def send_summary_email(to_email, customer_name, order_id, feedback_category, sentiment_score):
    from_email = "your_email@gmail.com"
    password = "your_password"
    
    subject = f"Customer Feedback Summary for {customer_name}"
    body = f"""
    Customer Name: {customer_name}
    Order ID: {order_id}
    Feedback Category: {feedback_category}
    Sentiment Score: {sentiment_score}
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
    
    print(f"Summary email sent to {to_email}.")

if __name__ == '__main__':

    # Still Working
    '''# 1. Authenticate and fetch emails
    service = get_gmail_service()
    emails = fetch_feedback_emails(service)
    
    for email_body in emails:
        # 2. Analyze sentiment
        sentiment_score = analyze_sentiment(email_body)
        
        # 3. Extract data from email
        extracted_data = extract_data(email_body)
        
        # 4. Submit data to Google Form
        submit_to_google_form(
            customer_name=extracted_data['name'],
            order_id=extracted_data['order_id'],
            feedback_category=extracted_data['category'],
            sentiment_score=sentiment_score
        )
        
        # 5. Send summary email
        send_summary_email(
            to_email="support@company.com",
            customer_name=extracted_data['name'],
            order_id=extracted_data['order_id'],
            feedback_category=extracted_data['category'],
            sentiment_score=sentiment_score
        )'''
