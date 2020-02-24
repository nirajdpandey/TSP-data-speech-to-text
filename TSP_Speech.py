# Importing Dependencies
import glob
import os
import pandas as pd
import subprocess
import soundfile as sf

print("Your process has been initialized. This might takes few seconds to complete.....")
main = './TSP_48k'
wavs = [w for w in glob.glob(os.path.join(main, '*/*.wav')) if os.path.isfile(w)]
print("Total Wav files found:", len(wavs))
# wavs = glob.glob("/home/pandeynj/workspace/data/TTS/TTS/RAW/TSP-Speech/TSP-Speech/*.wav")
with open("wav_files.txt", 'w') as f:
    for i in wavs:
        f.write(i)

corpus = []

def InfoAudio(cmd_argument, save_result_path, wav=wavs):
    """
        Function InfoAudio attempts to extract embedded information out of wav files
        Specifically designed for TSP-Speech DataSet

    cmd_argument: Command line Argument for InfoAudio
    save_result_path: Path of a text file where you want to dump the stdout
    wav: List of wav file path you want to pass to InfoAudio
    """

    f = open(save_result_path, 'w')
    for files in wav:
        out = subprocess.Popen([cmd_argument,
                                files],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
        out.wait()
        stdout, stderr = out.communicate()
        f.write(stdout)

    with open(save_result_path) as f_input:
    	corpus.append(f_input.read())
    data = [i.split("\n") for i in corpus]
	# print(data)
    return data


def get_lines(data):
    """
        This function will extract only the targeted lines from the InfoAudio output

    data: pass the address of the text file which contains all the information of InfoAudio Features
    """

    line = []
    # if/else condition to match the starting string of the sentences to retrieve
    for i in data:
        for l in i:
            if 'Sampling frequency: 48000 Hz' in l:
                line.append(l.replace(" Hz", ""))
            elif 'File name:' in l:
                line.append(l)
            elif 'text:' in l:
                line.append(l)
            elif 'No. channels' in l:
                line.append(l)
            elif 'speaker:' in l:
                line.append(l)
            else:
                pass

    line = [i.strip() for i in line]
    print("Targeted lines has been extracted")
    # print(line)
    return line


def make_dataframe(line):
    """
        Function make_dataframe takes one argument line and tranform all the targeted lines
        into pandas DataFrame

    line: list of lines with (:) seperated
    """

    records = []
    for lines in line:
        key, value = lines.split(":")
        if key == "Sampling frequency":
            records.append({key: value})
        records[-1][key] = value
    data_new = pd.DataFrame.from_records(records)
    print('DataFrame has been build')
    return data_new


subtype = []


def extra_features(wavs=wavs):
    """
        Function extra_features extract more information about passed list of web files.

    :param wavs: The list of wav files you want to extract more information from
    :return: Sampling rate, channels and bit depth.
    """
    for file in wavs:
        ob = sf.SoundFile(file)
        subtype.append(ob.subtype)
    #return ob


extra_features()


def add_columns(df):
    """
        Function add_columns add more features to the existing fataframe.
        These features are coming from either research paper reading or bt mannually extracting
        by using Python Wavfile library

    df: DataFrame
    """

    df["Annotation kind"] = "Text"
    df["Language"] = "en"
    df["Native Speaker"] = "Yes"
    df["Dialects"] = "None"
    df["Reverberant"] = "None"
    df["Noisy"] = "No"
    df["Age"] = "Adult"
    df["File type"] = "wav"
    df["Spontaneous"] = "No"
    df["Subtype/Bit Depth"] = pd.Series(subtype)
    df["Comment"] = "None"
    df['Gender'] = df['speaker']
    print(df)
    # replace certain characters to make another "Gender" Column out of "speaker" column
    pattern = '|'.join(['CA', 'CB', 'FC', 'FB', 'FA', 'FD', 'FE', 'FF',
                        'FG', 'FH', 'FI', 'FJ', 'FK', 'FL', 'MA', 'MB',
                        'MC', 'MD', 'MF', 'MG', 'MH', 'MI', 'MJ', 'MK',
                        'ML'])
    df['Gender'] = df['Gender'].str.replace(pattern, '')
    df['speaker'] = df['speaker'].str.replace(pattern, 'TSP')
    return df


def save_df(data_new, name_of_csv_file):
    # Save pandas DataFrame by providing final data and path to .csv file
    data_new['text'] = data_new['text'].apply(lambda x: x.replace('.', ''))
    data_new['text'] = data_new['text'].apply(lambda x: x.replace('"', ''))
    data_new = data_new.rename(columns={'text': 'Annotation', 'File name': 'Wav_path', 'No. channels': 'Channels',
                                        'Sampling frequency': 'Sample rate'})
    data_new["ID"] = data_new['Wav_path'].apply(lambda x: x.split("/")[1])
    data_new["Speaker_ID"] = data_new["ID"]

    # There are only two child speaker.
    # let's modify age column for them

    data_new.loc[data_new.ID == 'CA', 'Age'] = "Child"
    data_new.loc[data_new.ID == 'CB', 'Age'] = "Child"

    data_new.to_csv(name_of_csv_file, sep='|', encoding='utf-16',
                    columns=['Annotation', 'Wav_path', 'Speaker_ID', 'Annotation kind', 'Language',
                             'Native Speaker', 'Dialects', 'Reverberant', 'Noisy',
                             'Sample rate', 'Channels', 'Age', 'File type',
                             'Spontaneous', 'Subtype/Bit Depth', 'Gender', 'Comment'])
    return data_new


text = InfoAudio('/home/niraj/Documents/work_place/TSP_Speech/AFsp-v10r2/bin/InfoAudio', 'Annotation.txt')

targeted_lines = get_lines(text)
create_dataframe = make_dataframe(targeted_lines)
add_col = add_columns(create_dataframe)
final_data = add_col
print(final_data.info())
save_final_result = save_df(final_data, "TSP-Speech.csv")
print('Your DataFrame has been saved to the current directory')
