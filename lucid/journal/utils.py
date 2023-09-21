import os
import openai
import re
from dotenv import load_dotenv


load_dotenv()

#OpenAi API Key 
openai.api_key = os.getenv("OPEN_API_KEY")


def analyse_journal_entry(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be given a journal entry, your First task is to clasify its sentiment as positive, neutral or negative. Your second task is to recognise thought distortions, output them and count how many there were in the text. "
            },
            {
                "role": "user", 
                "content": content
            }
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract response from API call
    content_message = response['choices'][0]['message']['content']

    # Split by line breaks
    lines = content_message.split('\n')

    # Extract sentiment
    sentiment = lines[0].split(': ')[1]

    # Extract thought distortions and descriptions
    thought_distortions = {}
    for line in lines[2:-2]:
        if line.strip():  # Check if line is not empty
            split_line = line.split('. ', 1)
            if len(split_line) == 2:  # Make sure there are enough elements to unpack
                _, text_entry = split_line
                distortion_type, description = text_entry.split(': ', 1)
                thought_distortions[distortion_type] = description


    # Extract count of thought distortions and convert to int. Check if str is empty to avoid error
    count_str = lines[-1].split(': ')[1]

    if count_str is not None: 
        count = 0
    else: 
        count = int(count_str)
   

    
    # Now, the 'sentiment', 'thought_distortions', and 'count' variables contain the parsed content.
    print(f'Sentiment: {sentiment}')
    print(f'Thought Distortions: {thought_distortions}')
    print(f'Count: {count}')

    return {
        'sentiment': sentiment,
        'thought-distortions': thought_distortions,
        'count': count
    }
