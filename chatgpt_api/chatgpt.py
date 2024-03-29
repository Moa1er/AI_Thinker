from dotenv import dotenv_values # pip3 instlal python-dotenv
import openai #pip3 install openai
import threading

secrets = dotenv_values(".env")
openai.api_key = secrets['CHATGPT_API_KEY']


MAX_RETRIES = 5
TIMEOUT = 20

def call_api(messages, result_container):
    chat = openai.chat.completions.create(model="gpt-4-0125-preview", messages=messages, temperature=0.9)
    result_container.append(chat.choices[0].message.content)

def call_api_handle_timeout(messages):
    retries = 0
    while retries < MAX_RETRIES:
        result_container = []
        t = threading.Thread(target=call_api, args=(messages, result_container))
        t.start()
        t.join(timeout=TIMEOUT)  # wait for the specified timeout

        if result_container:  # if there's a result, break out of the loop
            response = result_container[0]
            print(f"ChatGPT response: {response}")
            return response
        else:  # if the timeout is reached and there's no result, retry
            retries += 1
            print(f"Request timed out. Retry {retries}/{MAX_RETRIES}")

    raise Exception("Failed to get a response after max retries.")

def ask_for_division(question):
    messages = [{
        "role": "system",
        "content": 
            "You are a gpt that specializes in dividing a question into specialized GPTs."
          + "You should answer with the roles of the specialized GPTs separated by newlines."
          + "The role has to be precise and descriptive. It starts by 'You are a specialized gpt about' and ends by '.'."
    }]

    messages.append({
        "role": "user",
        "content": "The question is: " + question
    })

    print("User request: " + messages[len(messages) - 1]["content"])

    return call_api_handle_timeout(messages)

def ask_specialized_gpt(role, discussion):
    messages = [{
        "role": "system",
        "content": role
    }]

    messages.append({
        "role": "user",
        "content": "Respond to the following discussion:\n\n" + "\n".join(discussion)
    })

    print("User request: " + messages[len(messages) - 1]["content"])

    return call_api_handle_timeout(messages)

def ask_final_response(question, discussion):
    messages = [{
        "role": "system",
        "content": "You are a gpt that specializes in providing a final response out of a discussion and the initial question."
    }]

    messages.append({
        "role": "user",
        "content": "The question was: " + question + "\n\n" + "The final discussion was: \n".join(discussion)
    })

    print("User request: " + messages[len(messages) - 1]["content"])

    return call_api_handle_timeout(messages)