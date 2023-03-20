# ChatGPT Flask App by ChatGPT-3.5-turbo

This is a web application that allows users to chat with GPT-3.5-turbo. This project was designed by [your name] and mostly written by GPT-3.5-turbo.

## Features

A simple flask app that will allow you to converse with chatgpt-3.5-turbo. 
- Automatically include up to the last 1024 tokens worth of history
- Logs your conversations with a unique id
- Log viewer page

## Installation

### Requirements
- Ubuntu 22.04.2 (this version has been tested and confirmed to work)
- Python 3.8
- pip

**Note:** You´ll need an [OpenAI API key](https://beta.openai.com/signup/) to use this app. You will require a paid account with OpenAI.


### Steps to install
1. Install Python 3.8 and pip as per your system requirements.
2. Install the OpenAI library by running:

   ```
   pip install openai=0.27.0
   ```

3. Clone this repository by running:

   ```
   git clone https://github.com/dustinandrews/gptFlaskByGpt-3.5-turbo.git
   ``` 

4. Navigate to the directory of the project:

   ```
   cd gptFlaskByGpt-3.5-turbo.git
   ```

5. Create a new file named "openai.api_key.txt" and add your [OpenAI API key](https://beta.openai.com/docs/authentication/api-keys) in the file using a text editor of your choice:

   ```
   nano openai.api_key.txt
   ```

6. Start the app by running the following command:

   ```
   flask run
   ```

7. Access the application by navigating to the URL displayed in the terminal window on your web browser.

## License

This project is licensed under the MIT License

## Motivation

I was looking for a simple ChatGpt client I could use with gtp-3.5-turbo. I prefered flask because it's simple to use and run for experimental purposes.

I also wanted to test out chat-gpt. It wrote 90% of the code in response to my questions.

## Known Issues

After around 20-30 messages OpenApi will timeout. This seems to be due to the openai library doing something odd. Use the reset button to start over.

## Wishlist
