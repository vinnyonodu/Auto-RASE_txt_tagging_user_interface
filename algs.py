import json


def segment(decoded_input_ids: list, predicted_labels: list):
    current_label = None
    current_segment = []

    total_segments = []

    for i, value in enumerate(decoded_input_ids):
        i_p_l = str(predicted_labels[i]).lower().replace("b-", "").replace("i-", "")
        if i_p_l != "o":
            if current_label is None:
                current_label = i_p_l
                current_segment = [value]
            elif current_label == i_p_l:
                current_segment.append(value)
            else:
                total_segments.append((current_label, current_segment))
                current_label = i_p_l
                current_segment = [value]
        else:
            if current_label is not None:
                total_segments.append((current_label, current_segment))
                current_label = None
                current_segment = []

            total_segments.append((i_p_l, [value]))

    if current_label is not None:
        total_segments.append((current_label, current_segment))

    return total_segments


def count_segments(segmented):
    map = {}
    for segment in segmented:
        if segment[0] in map:
            map[segment[0]] += 1
        else:
            map[segment[0]] = 1
    return map


def accuracy_score_for_each_rasetype(segmented, decoded_input_ids, predicted_labels):
    total = 0
    correct = 0

    for i, value in enumerate(decoded_input_ids):
        if predicted_labels[i] != "O":
            total += 1
            if value in segmented[i][1]:
                correct += 1

    return correct / total


# read dataset.json
with open("dataset.json") as f:
    data = json.load(f)

print(len(data))

all_in_one = []

for i, json_object in enumerate(data):
    strrr = str(json_object)


# use_index = 0
# data = data[use_index]
# seg = segment(data["tokens"], data["labels"])
# print(count_segments(seg))
# # chunk segments ino 10

# chunked = [seg[i:i + 10] for i in range(0, len(seg), 10)]
# for chunk in chunked:
#     print(chunk)
#     print()

for json_object in data:
    input_ids = json_object["tokens"]
    predicted_labels = json_object["labels"]

    segmented = segment(input_ids, predicted_labels)
    all_in_one += segmented

all_map = count_segments(all_in_one)
print(all_map)
#
# # express as percentage
#
# for key in all_map:
#     all_map[key] = all_map[key] / len(all_in_one)
#     all_map[key] = "{:.2f}".format(all_map[key] * 100)
#
# print(all_map)
#
# # print total number of segments
# print(len(all_in_one))
