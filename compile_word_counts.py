import argparse
import pandas as pd
import re 
import json

def read_stop_words():
    #read from stopwords.txt
    stop_words = []
    with open('stop_words.txt', 'r') as f:
        for line in f:
            stop_words.append(line.strip())
    return stop_words

def clean_dialog(dialog):
    dialog = dialog.lower()
    dialog = re.sub(r'[()\[\],\-.?!:;#&]', ' ', dialog)
    dialog = [re.sub(r',$', '', item) for item in dialog.split()]
    dialog = [re.sub(r'[.,]{2,}', ' ', item) for item in dialog]
    
    return dialog

def compute_word_counts(output_path, dialog_path):
    # Read stop words
    stop_words = read_stop_words()
    # Punctuation characters
    punc = [',', '(', ')', '[', ']', '-', '.', '?', '!', ':', ';', '#', '&']
    # Ponies
    pony_names = ['Twilight Sparkle', 'Applejack', 'Rarity', 'Pinkie Pie', 'Rainbow Dash', 'Fluttershy']
    df = pd.read_csv(dialog_path)
    # Filter rows by pony
    df_filtered = df[df['pony'].isin(pony_names)]
    # Focus on pony and dialog columns
    df_filtered_col = df_filtered[['pony', 'dialog']]
    # Clean dialogues
    df_filtered_col['dialog'] = df_filtered_col['dialog'].apply(clean_dialog)
    # Remove stop words
    df_filtered_col['dialog'] = df_filtered_col['dialog'].apply(lambda x: [item for item in x if item not in stop_words])
    #make sure only alphabetic words are kept
    df_filtered_col['dialog'] = df_filtered_col['dialog'].apply(lambda x: [item for item in x if item.isalpha()])
    # Compute word counts
    word_counts = {}
    for pony in pony_names:
        word_counts[pony] = {}
        #
        pony_dialog = df_filtered_col[df_filtered_col['pony'] == pony]['dialog']
        
        for dialog in pony_dialog:
            for word in dialog:
                if word not in word_counts[pony]:
                    word_counts[pony][word] = 1
                else:
                    word_counts[pony][word] += 1
   
    #keep only words that appear more than 5 times
    for pony in pony_names: 
       
       word_counts[pony] = {k:v for k,v in word_counts[pony].items() if v > 5}
    # Write word counts to json file
    with open(output_path, 'w') as f:
        json.dump(word_counts, f)
    
    return word_counts



def main():
    parser = argparse.ArgumentParser(description='Compute word counts for each pony from all episodes of MLP.')
    parser.add_argument('-o', dest='word_count', required=True, help='The name of the json file to output to')
    parser.add_argument('-d', dest='clean_dialog', required=True,help='The name of the csv file to extract words from')

    args = parser.parse_args()
    #compute_word_counts()
    compute_word_counts(args.word_count, args.clean_dialog)


if __name__ == "__main__":
    main()
