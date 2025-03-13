import os
import dotenv
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import db

dotenv.load_dotenv()

def send_whapi_request(endpoint, payload):
    """Send a request to the WhatsApp API."""
    API_URL = 'https://gate.whapi.cloud'
    TOKEN = 'qqzjkILSTfrV3eLZdeiDE5DrRftgk0EB'
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    url = f"{API_URL}/{endpoint}"

    # Check if we're sending an image
    if 'media' in payload:
        # Split the media path and MIME type for image
        image_path, mime_type = payload.pop('media').split(';')
        
        with open(image_path, 'rb') as image_file:
            # Create a MultipartEncoder for the file upload
            m = MultipartEncoder(
                fields={
                    **payload,
                    'media': (image_path, image_file, mime_type)
                }
            )
            headers['Content-Type'] = m.content_type
            response = requests.post(url, data=m, headers=headers)
    else:
        # For text messages, use JSON encoding
        headers['Content-Type'] = 'application/json'
        response = requests.post(url, json=payload, headers=headers)
    
    return response.json()

class Bot:
    
    '''
        handles chats 
    '''

    def __init__(self, user_id, responses, debug=False):
        self.debug = debug
        self.user_id = user_id
        self.memory = []
        self.welcome = True
        self.responses = responses
        self.current_node = responses['Welcome']
        self.next_node_id = None


    def send_response(self, message):
        
        def get_messages(response):
            msgs = []
            print(response)
            responses =  response['response']
            for msg in responses:
                print(msg)
                if msg['type'].strip('\n') == 'text':
                    msgs.append({'payload':{'body': msg['message']}, 'endpoint':f'messages/{msg['type'].strip('\n')}'})
                elif msg['type'].strip('\n') == 'image':
                    msgs.append({'payload':{'caption': msg['caption'], 'media': f'files/images/{msg.filename}'}, 'endpoint':f'messages/{msg['type'].strip('\n')}'})
                elif msg['type'].strip('\n') == 'document':
                    msgs.append({'payload':{'caption': msg['caption'], 'media': f'files/documents/{msg.filename}'}, 'endpoint':f'messages/{msg['type'].strip('\n')}'})
                elif msg['type'].strip('\n') == 'video':
                    msgs.append({'payload':{'caption': msg['caption'], 'media': f'files/videos/{msg.filename}'}, 'endpoint':f'messages/{msg['type'].strip('\n')}'})
            if 'options' in response:
                btn = {'payload':{'body': {'text':'options'}, 
                                    'action':{'buttons': []}, 'type':'button'}, 
                        'endpoint':'messages/interactive'}
                
                for option in response['options']:      
                    btn['payload']['action']['buttons'].append({
                                        'type': 'quick_reply',
                                        'title': option['input'],
                                        'id': option['input']
                                        })
                if len(self.get_memory()) > 1:
                    btn['payload']['action']['buttons'].append({
                                        'type': 'quick_reply',
                                        'title': 'back',
                                        'id': 'back'
                                        })
            msgs.append(btn)
            #self.add_to_memory(message)
            return msgs
        
        def send_message(user_id, msg):
            payload, endpoint = msg.values()
            payload['to'] = user_id
            res = send_whapi_request(endpoint, payload)
            print(f'Response from Whapi: {res}')
            return res
            
        
        #payload = {}
        #payload['to'] = self.user_id
        if message:
            print(self.current_node)
            print(f'Current Node Options:{self.current_node['options']}\n')
            if len(self.get_memory()) == 0:
                msgs = get_messages(self.current_node)
                self.add_to_memory('Welcome')
                self.save_user()
            elif (message == 'back' or message == '0') and len(self.get_memory()) > 1:
                node_name = self.previous_node()
                self.current_node = self.get_response(node_name)
                msgs = get_messages(self.current_node)
            elif self.get_memory()[-1] == 'end':
                msgs = None;
            else:
                options = self.current_node['options']
                if len(options) == 0: # This is a leaf node
                    self.current_node = self.get_response('end')
                    self.add_to_memory(self.current_node)
                    msgs = get_messages(self.current_node)
                # To Do
                # Add a default ending fo leaf nodes
                
                else:
                    option_id = [option for option in options if option['input'] == message]
                    if len(option_id) == 0: #User input incorrect and the current node not welcome
                        msgs = [{'payload':{'body':f'Invalid input {message}. Please select an appropriate option:\n'}, 'endpoint':'messages/text'}]
                        #To Do
                        #Resend the options
                    else:
                        response =  self.get_response(option_id[0]['node_name'])
                        self.add_to_memory(option_id[0]['node_name'])
                        self.current_node = response
                        msgs = get_messages(self.current_node)
        #elif message is None: #default message
        #    response = self.get_response('Welcome')
        #   msgs = get_messages(response)
        
        if self.debug:
            return msgs
        
        print('Memory: ',self.get_memory())
        
        if msgs is not None:
            print(msgs)
            for msg in msgs:
                res = send_message(self.user_id, msg)
                if res['error']:
                    self.current_node = self.previous_node()
            self.save_memory()

                

    def get_response(self, response_id ):
        try:
            return self.responses[response_id]
        except KeyError:
            print(f'{response_id} not in response')
            return None
            

    def add_to_memory(self, option_id):
        self.memory.append(option_id)

    def get_memory(self):
        return self.memory
    
    def previous_node(self):
        if len(self.memory) > 1:
            self.memory.pop()
            return self.memory[-1]
        else:
            return None
    
    def save_memory(self):
       db.save_memory(self.user_id, "/".join(self.memory))
    
    def retrieve_memory(self):
        memory_string = db.get_memory(self.user_id)
        return memory_string.split('/')
    
    def save_user(self):
        db.save_user(self.user_id, "/".join(self.memory))
        
       
        
        
    
