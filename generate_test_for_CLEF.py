import json

def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
        ids = [d['id'] for d in data]
        srcs = [d['src'] for d in data]
        refs = [d['tgt'] for d in data]

    return ids, srcs, refs


def create_test_file_for_participants(ids, srcs):
    data = [{"id": id_val, "src": src_val} for id_val, src_val in zip(ids, srcs)]
    file_path = "test.json"

    # Write the data to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def create_test_file_ground_truth(ids, refs):
    data = [{"id": id_val, "ref": src_val} for id_val, src_val in zip(ids, refs)]
    file_path = "test_GT.json"

    # Write the data to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def main(json_file):
    ids, srcs, refs = read_json(json_file)
    create_test_file_for_participants(ids, srcs)
    create_test_file_ground_truth(ids, refs)


if __name__ == '__main__':
    main("/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/test_Speech2Picto.json")