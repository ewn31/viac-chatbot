import csv

def getResponses(csv_file_path, debug = False):

    responses = {}
    
    errors = []

    try:
        # utf-8-sig removes the \ufeff char added to the start of a line in an 
        #utf encoded file.
        with open(csv_file_path, encoding='utf-8-sig') as responses_csv_file:
            lines = csv.DictReader(responses_csv_file)
            for response_objects in lines:
                response = []
                options = []
                messages = response_objects['response'].split(';')
                if debug:
                    print(f'messages:{messages}\n\n')
                    #print(f'responses: {responses}\n\n')
                for m in messages:
                    if(m != ' ' and m != ''):
                        try:
                            type, message = m.split(':')
                        except ValueError as err:
                            print(f'The was an error parsing this line: {m}')
                            errors.append(f"Error parsing message field in {response_objects['name']} with error:{err}")
                        response.append({'type':type, 'message': message})
                        #print({'type':type, 'message': message})

                nodes = response_objects['options'].split(';')
                for n in nodes:
                    if(n != " " and n != ''):
                        try:
                            input, node_name = n.split(':')
                        except ValueError as err:
                            print(f'An error occured while parsing the options in node: {response_objects['name']}')
                            errors.append(f'Error parsing options field in {response_objects["name"]} with error: {err}')
                        options.append({'input':input, 'node_name': node_name})
                        #print({'input':input, 'node_name': node_name})
                responses[response_objects['name']]={'response':response, 'options':options}
        print(f'Nodes with errors: {errors}')
        return responses
    except FileNotFoundError:
        print(f'Error while processing csv file: {csv_file_path} not found')



if __name__ == '__main__':
    csv_file_path = './files/responses_edited.csv'
    responses =  getResponses(csv_file_path, True)
    #print(responses)


