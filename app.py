
import PySimpleGUI as sg
import requests
import json

def get_chat_response(message):
    # Set up the request parameters
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}]
    }


    response = requests.post(url, headers=headers, data=json.dumps(payload))

    data = json.loads(response.text)

    gpt_message = data['choices'][0]['message']['content'].strip()
    if 'choices' not in data or len(gpt_message) == 0:
        print('Response does not contain valid choices')
        return ''
    return gpt_message

# Define a function to save a note to a file
def save_note(note):
    with open('notes.txt', 'a') as f:
        f.write(note + '\n')

# Create a simple GUI with PySimpleGUI
layout = [
    [sg.Text('Enter your message:')],
    [sg.InputText()],
    [sg.Button('Send'), sg.Button('Save and Quit')]
]
window = sg.Window('ChatGPT Notes', layout)

response = 'no message available'
message = ''

# Loop until the user quits
while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Send':
        message = values[0]
        
        response = get_chat_response(message)
        sg.popup(response, title='ChatGPT Response')
    elif event == 'Save and Quit':
        note = sg.popup_get_text('Enter a note:', title='Save Note')
        if note:
            save_note(note)
            save_note(message)
            save_note(response)

window.close()
