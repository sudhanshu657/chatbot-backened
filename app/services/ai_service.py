import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_email(subject, body):
    try:
        print("OPENAI KEY PRESENT:", bool(os.getenv("OPENAI_API_KEY")))

        prompt = f"""
        Summarize this email in 2-3 lines in simple English.

        Subject:
        {subject}

        Body:
        {body[:3000]}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize emails clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ OPENAI ERROR FULL:", repr(e))
        return "Summary not available"


def generate_reply(subject, body):
    try:
        print("OPENAI KEY PRESENT:", bool(os.getenv("OPENAI_API_KEY")))

        prompt = f"""
        Generate a professional, concise reply to this email.

        Original Subject: {subject}

        Original Body:
        {body[:3000]}

        Reply should be helpful and context-aware.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You generate professional email replies."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ OPENAI REPLY ERROR:", repr(e))
        return "Reply generation failed"




        