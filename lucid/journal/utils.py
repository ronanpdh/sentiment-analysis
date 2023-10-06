import os
import openai
import re
import nltk
from dotenv import load_dotenv

load_dotenv()

# OpenAi API Key
openai.api_key = os.getenv("OPEN_API_KEY")


def analyse_journal_entry(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be given a journal entry, your First task is to clasify its sentiment as positive, neutral or negative. Your second task is to recognise thought distortions, output them and count how many there were in the text.",
            },
            {"role": "user", "content": content},
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response


# Function to format API response
def format_content(analysed_text):
    # Extract response from API call
    content_message = analysed_text["choices"][0]["message"]["content"]

    # Split by line breaks
    lines = content_message.split("\n")

    # Extract sentiment - Use IF statement to handle the index error if the journal entry isn't long enough
    # sentiment = lines[0].split(": ")[1]
    if len(lines) > 1:
        sentiment = lines[0].split(": ")[1]
    else:
        sentiment = "N/A"
        pass

    # Extract thought distortions and descriptions
    thought_distortions = {}
    for line in lines[2:-2]:
        if line.strip():  # Check if line is not empty
            split_line = line.split(". ", 1)
            if len(split_line) == 2:  # Make sure there are enough elements to unpack
                _, text_entry = split_line
                distortion_type, description = text_entry.split(": ", 1)
                thought_distortions[distortion_type] = description

    # Convert thought_distortions into a string and seperate into sentences for better front end output
    formatted_distortions = "\n".join(
        f"{key}: {value}" for key, value in thought_distortions.items()
    )
    
    sentences = nltk.sent_tokenize(formatted_distortions)
    print(sentences)
    print(type(sentences))


    #  Store Thought Distortion types in a list to output into journal Entry detail view
    thought_distortions_keys = thought_distortions.keys()
    keys_list = list(thought_distortions_keys)
    keys_formatted = ", ".join(keys_list)

    # Extract count of thought distortions and convert to int. Check if str is empty to avoid error
    count_str = lines[-1].split(": ")[1]
    if count_str is not None:
        count = 0
    else:
        count = int(count_str)

    # Now, the 'sentiment', 'thought_distortions', and 'count' variables contain the parsed content. Use for checking outcome
    # print(f"Sentiment: {sentiment}")
    # print(f"Thought Distortions: {formatted_distortions}")
    # print(f"keys: {keys_formatted}")

    return {
        "sentiment": sentiment,
        "thought-distortions": sentences,
        "distortion-types": keys_formatted,
        "count": count,
    }

# #    Use NLTK sentence tokenizer to seperate sentences in thought disortions - This will improve flexibiliyy and output on front end
# def distortion_sentence_tokenizer(thought_distortions):
#     sentences = nltk.sent_tokenize(thought_distortions)
#     return sentences