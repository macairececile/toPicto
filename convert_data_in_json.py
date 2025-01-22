import pandas as pd
from ast import literal_eval


def read_csv(csv_file):
    return pd.read_csv(csv_file, sep="\t")


def create_json_for_text_to_picto(data, output_json):
    data['pictos'] = data['pictos'].apply(lambda x: literal_eval(x))

    final_data = data.rename({'text': 'src', 'tokens': 'tgt'}, axis='columns')
    final_data = final_data[['id', 'src', 'tgt', 'pictos']]

    final_data.to_json(output_json, orient='records')


def create_json_for_speech_to_picto(data, output_json):
    data['src'] = data['id'].apply(lambda x: x + '.wav')

    final_data = data.rename({'id': 'id', 'tokens': 'tgt'}, axis='columns')
    final_data = final_data[['id', 'src', 'tgt', 'pictos']]

    final_data.to_json(output_json, orient='records')


def create_data_for_ToPicto():
    path = "/data/macairec/PhD/ToPicto2025/datasets/final_splits/"
    outdir_text = "/data/macairec/PhD/ToPicto2025/datasets/final_splits/json/TextToPicto/"
    outdir_speech = "/data/macairec/PhD/ToPicto2025/datasets/final_splits/json/SpeechToPicto/"
    splits = ["train", "valid", "test_general", "test_medical"]
    for i in range(0, 4):
        data = read_csv(path + splits[i] + ".tsv")
        create_json_for_text_to_picto(data, outdir_text + splits[i] + ".json")
        create_json_for_speech_to_picto(data, outdir_speech + splits[i] + ".json")


if __name__ == '__main__':
    create_data_for_ToPicto()
