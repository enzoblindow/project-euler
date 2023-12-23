import configparser
from openai import OpenAI


def transform_time_to_string(runtime):
    if runtime < 0.001:
        unit = u'µs'
        runtime *= 1000000
        runtime = int(runtime)
    elif runtime < 1:
        unit = u'ms'
        runtime *= 1000
        runtime = int(runtime)
    elif runtime < 300:
        unit = u's'
        runtime *= 1
        runtime = round(runtime, 1)
    elif runtime < 120 * 60:
        unit = u'm'
        runtime *= 1 / 60
        runtime = round(runtime, 1)
    elif runtime < 120 * 60 * 60:
        unit = u'h'
        runtime *= 1 / 60 * 1 / 60
        runtime = round(runtime, 2)
    else:
        unit = u'd'
        runtime *= 1 / 60 * 1 / 60 * 1 / 24
        runtime = round(runtime, 1)
    return u'{}{}'.format(runtime, unit)


def write_default_config():

    config = configparser.ConfigParser()

    config.add_section("keys.api.openai")
    config["keys.api.openai"]["api_key"] = "FIXME"

    config.add_section("keys.api.gemini")
    config["keys.api.gemini"]["api_key"] = "FIXME"

    with open("config.ini", "w") as f:
        config.write(f)


class OpenAIClient():
    def __init__(self, model:str = "gpt-3.5-turbo-1106"):
        self.model = model

        # open client
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.client = OpenAI(
            api_key=config['keys.api.openai']['api_key'],
        )

        # defaults
        self.responses = list()

    def get_response(self, system_message, user_message):
        return self.client.chat.completions.create(
            model=f"{self.model}",
            messages=[
                {"role": "system", "content": f"{system_message}"},
                {"role": "user", "content": f"{user_message}"}
            ]
        )

    def get_answer_code(self, assignment_text):
        response = self.get_response(
            system_message = """
                I want you to be a mathmatical researcher. I will give you a mathmatical problem statement written in 
                markdown including latex notation. Write me the most efficient solution in python that returns the 
                final answer to the problem in a method called 'solve' that takes no arguments. Only return one code block
                of Python code, nothing else.
            """,
            user_message = f"The problem statement is as follows (in markdown): \'{assignment_text}\'"
        )
        
        # store responses 
        self.responses.append(response)
        
        return response.choices[0].message.content


