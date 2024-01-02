import json


def get_reformed_label(previous_label) -> str:
    new = previous_label.split('-')
    if len(new) == 1:
        return previous_label
    new = new[0]
    label_map = {
        'R': 'Requirement',
        'A': 'Application',
        'S': 'Selection',
        'E': 'Exception',
    }
    return label_map[new]


with open('data.json') as f:
    json_data = json.load(f)


cleaned_data = []
for block in json_data:
    tokens = block['tokens']
    labels = block['labels']

    cleaned_tokens = []
    cleaned_labels = []

    for i, token in enumerate(tokens):
        token = token.strip()
        token_split = token.split(' ')

        label = str(labels[i])
        label = label.replace("start-", "")
        label = label.replace("inside-", "")
        label = label.replace("end-", "")

        label = get_reformed_label(label)

        if len(token_split) == 1:
            cleaned_tokens.append(token.replace('\n', '').strip())
            cleaned_labels.append("B-" + label)
            continue

        for j, sub_token in enumerate(token_split):
            cleaned_tokens.append(sub_token.replace('\n', '').strip())
            if j == 0:
                cleaned_labels.append('B-' + label)
            # elif j == len(token_split) - 1:
            #     cleaned_labels.append('E-' + label)
            else:
                cleaned_labels.append('I-' + label)

        cleaned_tokens.append('\n')
        cleaned_labels.append('\n')

    sentences = []
    current_sentence = ""
    for i, token in enumerate(cleaned_tokens):
        if token == '\n':
            sentences.append(current_sentence)
            current_sentence = ""
        else:
            to_add = token + ' ' + cleaned_labels[i] + '\n'
            if len(to_add.strip().split(' ')) <= 1:
                continue
            print(to_add)
            current_sentence += to_add

    cleaned_data += sentences

total = len(cleaned_data)

train = cleaned_data[:int(total * 0.8)]
test = cleaned_data[int(total * 0.8):int(total * 0.9)]
dev = cleaned_data[int(total * 0.9):]

print(len(train))
print(len(test))
print(len(dev))


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        for i, sentence in enumerate(data):
            f.write(sentence)
            if i != len(data) - 1:
                f.write('\n')


# write_to_file('train.txt', train)
# write_to_file('test.txt', test)
# write_to_file('dev.txt', dev)
