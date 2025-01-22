import os
import shutil

import pandas as pd
import json
from pydub import AudioSegment

clips_from_gold = ["cefc-tcof-Acc_del_07-111", "cefc-tcof-Acc_del_07-118", "cefc-tcof-Acc_del_07-13",
                   "cefc-tcof-Acc_del_07-44", "cefc-tcof-voyage_USA-92", "cefc-tcof-voyage_USA-81",
                   "cefc-tcof-Masc_dom_sd-28", "cefc-tcof-Masc_dom_sd-27", "cefc-tcof-Masc_dom_sd-249",
                   "cefc-tcof-Masc_dom_sd-237", "cefc-tcof-Masc_dom_sd-178", "cefc-tcof-Masc_dom_sd-133",
                   "cefc-tcof-Masc_dom_sd-132", "cefc-tcof-Masc_dom_sd-13", "cefc-tcof-Masc_dom_sd-122",
                   "cefc-tcof-Mar_ferr_sd-923", "cefc-tcof-Mar_ferr_sd-919", "cefc-tcof-Mar_ferr_sd-917",
                   "cefc-tcof-Mar_ferr_sd-897", "cefc-tcof-Mar_ferr_sd-803", "cefc-tcof-Mar_ferr_sd-788",
                   "cefc-tcof-Mar_ferr_sd-755", "cefc-tcof-Lic2012-13_Cohard-23", "cefc-tcof-Lic2012-13_Cohard-151",
                   "cefc-tcof-Lic2012-13_Cohard-132", "cefc-tcof-Lic2012-13_Carrillo-64",
                   "cefc-tcof-Lic2012-13_Carrillo-58", "cefc-tcof-Lic2012-13_Carrillo-55",
                   "cefc-tcof-Lic2012-13_Benmehdi-83", "cefc-tcof-Acc_kom_07-133", "cefc-tcof-Educ_pot_08-138",
                   "cefc-tcof-Educ_pot_08-156", "cefc-tcof-Educ_pot_08-154", "cefc-tcof-Emploi_cha_08-111",
                   "cefc-tcof-Acc_kom_07-81", "cefc-tcof-Ag_ael_08-131", "cefc-tcof-Ag_ael_08-162",
                   "cefc-tcof-Ag_ael_08-25", "cefc-tcof-Ag_ael_08-54", "cefc-tcof-Ag_ael_08-66",
                   "cefc-tcof-Mar_ferr_sd-431", "cefc-tcof-Mar_ferr_sd-485", "cefc-tcof-Acc_del_07-14",
                   "cefc-tcof-Ag_ael_08-65", "cefc-tcof-Lic2012-13_Guerrero-5", "cefc-tcof-Lic2012-13_Guerrero-50",
                   "cefc-tcof-Lic2012-13_Guerrero-51", "cefc-tcof-Lic2012-13_Guerrero-73",
                   "cefc-tcof-Lic2012-13_Guerrero-81", "cefc-tcof-Lic2012-13_Merheb-11", "cefc-tcof-Rae_ash_sd-108",
                   "cefc-tcof-Rae_ash_sd-128", "cefc-tcof-Rae_ash_sd-176", "cefc-tcof-Rae_ash_sd-198",
                   "cefc-tcof-Rae_ash_sd-201", "cefc-tcof-Rae_ash_sd-218", "cefc-tcof-Rae_ash_sd-28",
                   "cefc-tcof-Rae_ash_sd-30", "cefc-tcof-Rae_ash_sd-56", "cefc-tcof-Rae_ash_sd-83",
                   "cefc-tcof-Reunion_hen_09-141", "cefc-tcof-Reunion_hen_09-257", "cefc-tcof-Reunion_jan_09-10",
                   "cefc-tcof-Reunion_jan_09-106", "cefc-tcof-Reunion_jan_09-123", "cefc-tcof-Reunion_jan_09-191",
                   "cefc-tcof-Reunion_jan_09-21", "cefc-tcof-Reunion_jan_09-313", "cefc-tcof-Reunion_jan_09-316",
                   "cefc-tcof-guitariste-285", "cefc-tcof-Reunion_jan_09-296", "cefc-tcof-ordinateur-61",
                   "cefc-tcof-organisation_fetes-149", "cefc-tcof-organisation_fetes-16",
                   "cefc-tcof-petite_discussion_famille-100", "cefc-tcof-petite_discussion_famille-108",
                   "cefc-tcof-petite_discussion_famille-132", "cefc-tcof-petite_discussion_famille-144",
                   "cefc-tcof-pompiers-26", "cefc-tcof-pompiers-267", "cefc-tcof-potins_famille-134",
                   "cefc-tcof-potins_famille-135", "cefc-tcof-preparation_voyage-110",
                   "cefc-tcof-concert_Indochine-152", "cefc-tcof-concert_Indochine-156",
                   "cefc-tcof-concert_Indochine-179", "cefc-tcof-concert_Indochine-76",
                   "cefc-tcof-deux_pipelettes_1-177", "cefc-tcof-dragon-48", "cefc-tcof-espoir_2-107",
                   "cefc-tcof-Tel_maz_07-59", "cefc-tcof-Tel_maz_07-60", "cefc-tcof-Tromboniste-106",
                   "cefc-tcof-Reunion_jan_09-6", "cefc-tcof-Reunion_jan_09-91", "cefc-tcof-Reunion_luc_08-105",
                   "cefc-tcof-Reunion_luc_08-117", "cefc-tcof-Reunion_luc_08-144", "cefc-tcof-Reunion_luc_08-174",
                   "cefc-tcof-Reunion_luc_08-182"]


def read_csv(csv_file):
    return pd.read_csv(csv_file, sep="\t")


def filter_data(data):
    df_filtered = data[data.tokens != 'None']
    df_filtered_2 = df_filtered[df_filtered.tokens.notna()]
    return df_filtered_2[~df_filtered_2['clips'].isin(clips_from_gold)]


def merge_data(data1, data2):
    return pd.concat([data1, data2])


def process_data(file1, file2):
    data1, data2 = read_csv(file1), read_csv(file2)
    all_data = merge_data(data1, data2)
    all_data_filter = filter_data(all_data)
    return all_data_filter


def split_train_dev_test(all_data_filter):
    df_shuffled = all_data_filter.sample(frac=1, random_state=42).reset_index(drop=True)

    # Calculate the sizes for train, dev, and test sets
    total_size = len(df_shuffled)
    train_size = int(0.9 * total_size)
    dev_size = (total_size - train_size) // 2

    # Split the shuffled DataFrame into train, dev, and test sets
    train_df = df_shuffled[:train_size]
    dev_df = df_shuffled[train_size:(train_size + dev_size)]
    test_df = df_shuffled[(train_size + dev_size):]

    return train_df, dev_df, test_df


def create_json_for_text_to_picto(data, output_json):
    data_for_json = data[["clips", "text", 'pictos', 'tokens']]
    data_for_json = data_for_json.sort_values(by=['clips'], ignore_index=True)
    data_for_json['pictos'] = data_for_json['pictos'].apply(lambda x: eval(x))

    final_data = data_for_json.rename({'clips': 'id', 'text': 'src', 'tokens': 'tgt'}, axis='columns')
    final_data = final_data[['id', 'src', 'tgt', 'pictos']]

    final_data.to_json(output_json, orient='records')


def create_json_for_speech_to_picto(data, output_json):
    data_for_json = data[["clips", 'pictos', 'tokens']]
    data_for_json = data_for_json.sort_values(by=['clips'], ignore_index=True)
    data_for_json['pictos'] = data_for_json['pictos'].apply(lambda x: eval(x))
    data_for_json['src'] = data_for_json['clips'].apply(lambda x: x + '.wav')

    final_data = data_for_json.rename({'clips': 'id', 'tokens': 'tgt'}, axis='columns')
    final_data = final_data[['id', 'src', 'tgt', 'pictos']]

    final_data.to_json(output_json, orient='records')


def create_data_for_ToPicto(file_1, file_2):
    outdir_text = "/data/macairec/PhD/CLEFToPicto2024/data/TextToPicto/"
    outdir_speech = "/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/"
    splits = ["train", "valid", "test"]
    all_data = process_data(file_1, file_2)
    for i, el in enumerate(split_train_dev_test(all_data)):
        create_json_for_text_to_picto(el, outdir_text + splits[i] + ".json")
        create_json_for_speech_to_picto(el, outdir_speech + splits[i] + ".json")


def get_lengths(items):
    total_length = sum([len(sentence.split()) for sentence in items])
    average_length = total_length / len(items)

    sentence_lengths = [len(sentence.split()) for sentence in items]
    min_length = min(sentence_lengths)
    max_length = max(sentence_lengths)

    return average_length, min_length, max_length


def get_audio_durations(path, audio_files):
    durations = []

    for file_path in audio_files:
        audio = AudioSegment.from_file(path + file_path)
        duration = len(audio) / 1000  # Convert milliseconds to seconds
        durations.append(duration)

    return durations


def print_duration_info(path, audio_files):
    durations = get_audio_durations(path, audio_files)

    min_duration = min(durations)
    max_duration = max(durations)
    average_duration = sum(durations) / len(durations)

    print("Duration Information:")
    print(f"Min duration: {min_duration:.2f} seconds")
    print(f"Max duration: {max_duration:.2f} seconds")
    print(f"Average duration: {average_duration:.2f} seconds")


# def compute_stats(file_json_train, file_json_test, type):
#     with open(file_json_train, 'r') as f:
#         data = json.load(f)
#     src_train = [d['src'] for d in data]
#     tgt_train = [d['tgt'] for d in data]
#     with open(file_json_test, 'r') as f:
#         data = json.load(f)
#     src_valid = [d['src'] for d in data]
#     tgt_valid = [d['tgt'] for d in data]
#
#     if type == "text":
#         print(f"{'':<30}{'Train':<30}{'Valid':<30}")
#         print("-" * 75)
#
#         print(f"{'Number of utterances:':<30}{len(src_train):<30}{len(src_valid):<30}")
#
#         average_length_train, min_length_train, max_length_train = get_lengths(src_train)
#         average_length_val, min_length_val, max_length_val = get_lengths(src_valid)
#         print(f"{'Min length:':<30}{min_length_train:<30}{min_length_val:<30}")
#         print(f"{'Max length:':<30}{max_length_train:<30}{max_length_val:<30}")
#         print(f"{'Average length:':<30}{average_length_train:<30}{average_length_val:<30}")
#
#         print(f"{'':<30}{'Train':<30}{'Valid':<30}")
#         print("-" * 75)
#
#         print(f"{'Number of utterances:':<30}{len(tgt_train):<30}{len(tgt_valid):<30}")
#
#         average_length_train, min_length_train, max_length_train = get_lengths(tgt_train)
#         average_length_val, min_length_val, max_length_val = get_lengths(tgt_valid)
#         print(f"{'Min length:':<30}{min_length_train:<30}{min_length_val:<30}")
#         print(f"{'Max length:':<30}{max_length_train:<30}{max_length_val:<30}")
#         print(f"{'Average length:':<30}{average_length_train:<30}{average_length_val:<30}")
#
#     if type == "speech":
#         print('TRAIN')
#         print_duration_info("/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/clips/", src_train)
#         print("VALID")
#         print_duration_info("/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/clips/", src_valid)

def load_data_from_json(file_json):
    with open(file_json, 'r') as f:
        data = json.load(f)
    return [d['src'] for d in data], [d['tgt'] for d in data]

def print_text_stats(src_train, src_valid, tgt_train, tgt_valid):
    print(f"{'':<30}{'Train':<30}{'Valid':<30}")
    print("-" * 75)

    print_stats("Number of utterances:", len(src_train), len(src_valid))
    print_lengths_info("Text Lengths", get_lengths(src_train), get_lengths(src_valid))
    print_stats("Number of utterances:", len(tgt_train), len(tgt_valid))
    print_lengths_info("Text Lengths", get_lengths(tgt_train), get_lengths(tgt_valid))

def print_speech_stats(src_train, src_valid):
    print("_____________________________")
    print('TRAIN')
    print_duration_info("/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/clips/", src_train)
    print("_____________________________")
    print("VALID")
    print_duration_info("/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/clips/", src_valid)

def print_stats(title, train_value, valid_value):
    print(f"{title:<30}{train_value:<30}{valid_value:<30}")

def print_lengths_info(title, train_lengths, valid_lengths):
    print(f"{title:<30}{'Train':<30}{'Valid':<30}")
    print("-" * 75)

    print_stats("Min length:", train_lengths[1], valid_lengths[1])
    print_stats("Max length:", train_lengths[2], valid_lengths[2])
    print_stats("Average length:", train_lengths[0], valid_lengths[0])

def compute_stats(file_json_train, file_json_test, type):
    src_train, tgt_train = load_data_from_json(file_json_train)
    src_valid, tgt_valid = load_data_from_json(file_json_test)

    if type == "text":
        print_text_stats(src_train, src_valid, tgt_train, tgt_valid)
    elif type == "speech":
        print_speech_stats(src_train, src_valid)


def read_clips(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return [d['src'] for d in data]


def select_clips_for_speech_to_picto(json_file_train, json_file_valid):
    clips_train, clips_valid = read_clips(json_file_train), read_clips(json_file_valid)
    source_directory = '/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/clips_tcof/clips/'
    destination_directory = '/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/clips/'
    for c in clips_train + clips_valid:
        try:
            source_path = os.path.join(source_directory, c)
            destination_path = os.path.join(destination_directory, c)

            # Copy the file from source to destination
            shutil.copy(source_path, destination_path)
        except:
            print("No file : ", c)


if __name__ == '__main__':
    # create_data_for_ToPicto("/data/macairec/PhD/CLEFToPicto2024/data/tcof_grammar_v2_final_1.csv",
    #                         "/data/macairec/PhD/CLEFToPicto2024/data/tcof_grammar_v2_final_2.csv")
    # select_clips_for_speech_to_picto("/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/train.json",
    #                                  "/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/valid.json")

    compute_stats("/data/macairec/PhD/CLEFToPicto2024/data/TextToPicto/train.json",
                  "/data/macairec/PhD/CLEFToPicto2024/data/TextToPicto/valid.json",
                  "text")

    compute_stats("/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/train.json",
                  "/data/macairec/PhD/CLEFToPicto2024/data/SpeechToPicto/valid.json",
                  "speech")
