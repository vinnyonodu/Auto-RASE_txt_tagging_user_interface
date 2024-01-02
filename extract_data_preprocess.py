from bs4 import BeautifulSoup


def find_closest_rasetype(node):
    while node is not None:
        if node.has_attr('data-rasetype'):
            return node['data-rasetype']
        node = node.parent
    return None


count_map = {}


def run(file) -> tuple:
    with open(file) as f:
        soup = BeautifulSoup(f, "html.parser")

    tags = soup.find_all(lambda tag: tag.has_attr('data-rasetype'))
    cleaned_tags = []

    for tag in tags:
        tags_without_current_tag = tags.copy()
        tags_without_current_tag.remove(tag)

        if not any([tag in t for t in tags_without_current_tag]):
            cleaned_tags.append(tag)

    final_data = []

    for i, tag in enumerate(cleaned_tags):
        test_html = str(tag)

        soup = BeautifulSoup(test_html, "html.parser")

        extracted_data = []
        for element in soup.descendants:

            if element.name is None and element.strip():  # this checks for text nodes
                rasetype = find_closest_rasetype(element.parent)
                extracted_data.append((rasetype, element.strip()))
                if count_map.get(rasetype) is None:
                    count_map[rasetype] = 1
                else:
                    count_map[rasetype] += 1
            else:
                if i == 51 and file == "p.html":
                    if str(element).strip().startswith("<span data-raseproperty"):
                        text = str(element).split("data-raseproperty")[1].replace("=\"", "").split("\"")[0]
                        rasetype = str(element).split("data-rasetype")[1].replace("=\"", "").split("\"")[0]
                        extracted_data.append((rasetype, text))
                        if count_map.get(rasetype) is None:
                            count_map[rasetype] = 1
                        else:
                            count_map[rasetype] += 1

        # first = the first element that has Section else it's just the first element
        first = [(i, x) for i, x in enumerate(extracted_data) if "Section" in x[0]]
        first_index = 0
        if len(first) == 0:
            first = extracted_data[0]
        else:
            first_index = first[0][0]
            first = first[0][1]

        if "Section" in first[0]:
            rasetype = first[0]
            only_type = rasetype.split("Section")[0]

            for i in range(0, len(extracted_data)):
                sub_rasetype = extracted_data[i][0]

                if i == first_index:
                    extracted_data[i] = (f"start-{only_type}", extracted_data[i][1])
                elif sub_rasetype != rasetype:
                    extracted_data[i] = (f"{sub_rasetype[0]}-{only_type}", extracted_data[i][1])
                elif i != len(extracted_data) - 1:
                    extracted_data[i] = (f"inside-{only_type}", extracted_data[i][1])
                else:
                    extracted_data[i] = (f"end-{only_type}", extracted_data[i][1])

        final_data.append(extracted_data)

    tokens = []
    labels = []

    for data in final_data:
        for token in data:
            tokens.append(token[1])
            labels.append(token[0])

    return tokens, labels


array = ["a.html", "b.html", "c.html", "d.html", "e.html", "f.html", "g.html", "h.html", "i.html", "j.html", "k.html",
         "l.html", "m.html", "n.html", "o.html", "p.html", "q.html", "r.html", "s.html", "t.html", "u.html", "v.html",
         "w.html", "x.html", "y.html"]

json_output = []
for i, file in enumerate(array):
    tokens, labels = run(file)
    if len(tokens) != 0:
        json_output.append({"tokens": tokens, "labels": labels})

import json

with open('data.json', 'w') as outfile:
    json.dump(json_output, outfile)

all_labels = [label for json in json_output for label in json["labels"]]
cleaned_up_labels = []
for label in all_labels:
    x = label.split("-")
    if len(x) == 2:
        cleaned_up_labels.append(x[1])
    else:
        cleaned_up_labels.append(x[0])

from collections import Counter

x = (Counter(cleaned_up_labels))
for key, value in x.items():
    print(f"{key}: {value}")


# print()
# print(count_map)
# #sum count_map
# print(f" Total Number: {sum(count_map.values())}")

# one hot encode all labels
# set_x = list(set(all_labels))
# one_hot = {}
# for i, x in enumerate(set_x):
#     one_hot[x] = i
#
# print(one_hot)
#
# x = {'Requirement': 0, 'R-Exception': 1, 'Exception': 2, 'start-Requirement': 3, 'S-Selection': 4,
#      'inside-Exception': 5, 'S-Exception': 6, 'inside-Requirement': 7, 'R-Application': 8, 'Selection': 9,
#      'end-Exception': 10, 'Application': 11, 'E-Application': 12, 'start-Exception': 13, 'A-Requirement': 14,
#      'E-Requirement': 15, 'E-Exception': 16, 'S-Requirement': 17, 'end-Requirement': 18, 'E-Selection': 19,
#      'A-Selection': 20, 'inside-Selection': 21, 'A-Exception': 22, 'end-Application': 23, 'R-Selection': 24,
#      'start-Application': 25, 'R-Requirement': 26, 'inside-Application': 27, 'start-Selection': 28, 'S-Application': 29,
#      'end-Selection': 30, 'A-Application': 31}
