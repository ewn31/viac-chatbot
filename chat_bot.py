

class Chatbot:

    def __init__(self, user_id, responses):
        self.user_id = user_id
        self.memory = []
        self.current_node = responses['root']
        self.next_node_id = None


    def send_response(self, message):
        pass

    def get_user_response(self):
        pass

    def add_to_memory(self, optionId):
        self.memory.append(optionId)

    def get_memory(self):
        return '/'.join(self.memory)

    def save_memory(self):
        pass

