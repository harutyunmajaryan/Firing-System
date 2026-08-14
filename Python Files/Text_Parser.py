

# the function below returns the file content where are written the time code, controller number, channel number and device number
# so by parsing the text, we are going ot have the time in terms of seconds and milliseconds for the first token, then the controller number as second token
# channel number as the 3rd token and finally the device number as 4th token

def text_parser(text_content):
    parsed_text = ""

    new_text_content = text_content.splitlines()
    for line in new_text_content:
        parsed_text += line[:17] + "\n"

    print(parsed_text)
    return parsed_text



# the function below takes the parsed text and tries to tokenize the parsed text into 4 tokens, which are the time, controller number, channel number and device number
# this is for testing mainly, because the tokens are going to be located in the textbox in terms of their order and responsibilities

def tokenized_text(parsed_text_for_tokenization):
    new_text = parsed_text_for_tokenization.splitlines()
    try:
      for line in new_text:
          line = line.split()
          time = line[0]
          controller_number = line[1]
          channel_number = line[2]
          device_number = line[3]
          print(
            "TIME: " + time + " " + "Controller Number: " + controller_number + " " + "Channel Number: " + channel_number + " " + "Device Number: " + device_number + "\n")

    except (IndexError, ValueError):
        print("Cannot tokenize the text!")










