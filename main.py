import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from mailersend import emails
import time

# Load environment variables from .env file
load_dotenv()

# Get subscribers from environment variable
SUBSCRIBERS = os.getenv('SUBSCRIBERS', '').split(';')

# Initialize the email client
mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))


def get_index_value(url):
    try:
        response = requests.get(url, timeout=10)  # Add a timeout to handle network issues
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        index_values = soup.find_all('p', class_='card-indice-numero')
        if len(index_values) > 1:
            index_value_text = index_values[1].get_text(strip=True)
            return index_value_text
        else:
            return 'Value not found'
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return 'Error fetching data'


def send_email(ipca_value, subscribers=[]):
    subject = "IPCA Hoje"
    html = (
        f"<strong>IPCA</strong>: {ipca_value}<br>"
    )
    my_mail = "financeiro@gtrinvestimentos.com.br"

    for recipient in subscribers:
        try:
            response = mailer.send(
                {
                    "from": {"email": my_mail},
                    "to": [{"email": recipient}],
                    "subject": subject,
                    "html": html,
                }
            )
            print(f"Email sent to {recipient}: {response}")
            time.sleep(1.5)  # Wait for 1.5 seconds before sending the next email to avoid hitting rate limits
        except Exception as e:
            print(f"Error sending email to {recipient}: {e}")


def main():
    ipca_url = 'https://paineldeindices.com.br/indice/ipca/'
    ipca_value = get_index_value(ipca_url)

    # Send the email
    send_email(ipca_value, SUBSCRIBERS)

    print("Process completed.")


if __name__ == "__main__":
    main()
