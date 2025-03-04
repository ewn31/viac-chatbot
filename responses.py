import csv

def getResponses(csv_file_path, debug = False):

    responses = {}

    try:
        with open(csv_file_path) as responses_csv_file:
            lines = csv.DictReader(responses_csv_file)
            for response_objects in lines:
                response = []
                options = []
                messages = response_objects['response'].split(';')
                if debug:
                    print(f'messages:{messages}\n')
                    print(f'responses: {responses}\n')
                for m in messages:
                    if(m != ' ' and m != ''):
                        type, message = m.split(':')
                        response.append({'type':type, 'message': message})

                nodes = response_objects['options'].split(';')
                for n in nodes:
                    if(n != " " and n != ''):
                        input, node_name = n.split(':')
                        options.append({'input':input, 'node_name': node_name})
                responses[response_objects['name']]={'response':response, 'options':options}
        return responses
    except(e):
        print(f'Error: {e}')



if __name__ == '__main__':
    csv_file_path = './responses.csv'
    responses =  getResponses(csv_file_path)
    print(responses)


