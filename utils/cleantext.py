import re

def clean_text(text):
    # Remove multiple newlines (\n)
    text = text.replace('\n', " ")

    # Remove form feed (\f) characters
    text = re.sub(r"\f", "", text)

    # Remove extra spaces at the beginning and end
    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    return text
