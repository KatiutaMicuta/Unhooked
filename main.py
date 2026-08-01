from src.email_analyzer import email_analysis, extract_links
from src.url_analyzer import url_analysis

def main():

    input_type = input("Analyze an URL or an email? ")

    input_type = input_type.strip().lower()

    if input_type == 'email':
        email = input("Enter the sender's email address: ")
        body = input('Paste the email body (HTML) -  (in Gmail: open the email → ⋮ menu → "Show original"')
        result = email_analysis(email, body)

        if result["score"] == 0:
            print("The email is very likely safe!")
            
        else:
            print(f"The email has a phishing score of {result["score"]}.")

            for reason in result['reasons']:
                print(f"The email was flagged for: {reason}")

        if not extract_links(body):
            print("No links found")

    elif input_type == 'url':
        url = input("Enter your link: ")
        result = url_analysis(url)

        if result["score"] == 0:
            print("The link is very likely safe.")
        else:
            print(f"The link has a phishing score of {result["score"]}")

            for reason in result['reasons']:
                print(f"The link was flagged for: {reason}")

    else:
        print(f"Your input, {input_type}, did not match the requested format. Please enter URL or Email")


if __name__ == "__main__":
    main()