import json
import os
from argparse import ArgumentParser
import google.generativeai as genai  # type: ignore


def load_from_env():
    if not os.path.exists("env.json"):
        return {}
    try:
        with open("env.json", "r") as f:
            content = f.read().strip()
            if not content:  # File is empty
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        print("Warning: env.json file is corrupt or has invalid JSON. Using default empty settings.")
        return {}


def save_to_env(data):
    with open("env.json", "w") as f:
        json.dump(data, f)


def input_api_key():
    api_key = input("Enter your Gemini API key: ")
    env = load_from_env()
    env["api"] = api_key
    save_to_env(env)
    return api_key


def input_model():
    print("Available models: ")
    print("1. gemini-1.0-pro")
    print("2. gemini-1.5-pro")
    print("3. gemini-1.5-flash")

    option = input("Enter the number of the model you want to use: ")
    if option == "1":
        model = "gemini-1.0-pro"
    elif option == "2":
        model = "gemini-1.5-pro"
    elif option == "3":
        model = "gemini-1.5-flash"
    else:
        print("Invalid option. Please enter a number between 1 and 3.")
        return input_model()
    env = load_from_env()
    env["model"] = model
    save_to_env(env)
    return


def first_run():
    print("For setting up this tool you need to enter your API key, base URL, and model\n")
    input_api_key()
    input_model()


def chat(api_key, model):
    try:
        print("You are now chatting. Press Ctrl+C to exit.")

        # Configure the API once, outside the loop
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name=model,  # Use the model parameter here
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])

        while True:
            try:
                message = input("You> ")
                if not message:
                    print("Please enter a message.")
                    continue

                response = chat_session.send_message(message)
                print(f"AI> {response.text}")
            except KeyboardInterrupt:
                print("Exiting chat")
                return
    except EOFError:
        print("Exiting chat")
        return


def normal_run(api_key, model):
    print("1 to start chatting, 2 to change model, 3 to change API key, 4 to exit")
    option = input("Enter your option: ")
    if option == "1":
        chat(api_key, model)
    elif option == "2":
        model = input_model()
    elif option == "3":
        api_key = input_api_key()
    elif option == "4":
        print("Exiting")
        return
    else:
        print("Invalid option. Please enter a number between 1 and 4.")
        return


def main():
    env = load_from_env()
    if not env:
        first_run()
        env = load_from_env()

    api_key = env.get("api", "")
    model = env.get("model", "")

    if not api_key:
        api_key = input_api_key()
    if not model:
        model = input_model()

    normal_run(api_key, model)


if __name__ == "__main__":
    main()
