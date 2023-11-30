import argparse
import json
from math import log

def compute_pony_lang(pony_counts, num_words):
    #read json file
    with open(pony_counts, 'r') as f:
        pony_counts = json.load(f)
    #sort words by frequency
    pony_counts = {k:sorted(v.items(), key=lambda x: x[1], reverse=True) for k,v in pony_counts.items()}

    #calculate tf-idf
    pony_tfidf = {}
    for pony1 in pony_counts:
        pony_tfidf[pony1] = {}
        #calculate tf-idf for each word
        for word1 in pony_counts[pony1]:
            N = 1 
            #term frequency
            tf = word1[1]
            #number of ponies that mentionned the word
            for pony2 in pony_counts:
                if pony2 != pony1:
                    for word2 in pony_counts[pony2]:
                        if word1[0] == word2[0]:
                            N += 1
            #inverse document frequency
            idf = log(len(pony_counts) / N)
            tfidf = tf * idf
            pony_tfidf[pony1][word1[0]] = tfidf
        #sort words by tf-idf
        pony_tfidf[pony1] = sorted(pony_tfidf[pony1].items(), key=lambda x: x[1], reverse=True)
    top_n = {}
    for pony in pony_tfidf:
        for word in pony_tfidf[pony][:num_words]:
            if pony not in top_n:
                top_n[pony] = [word[0]]
            else:
                top_n[pony].append(word[0])
            json_stdout = json.dumps(top_n, indent=2)
        
    print(json_stdout)
    with open('distinctive_pony_words.json', 'w') as f:
        json.dump(top_n, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Compute Pony Language')
    parser.add_argument('-c',dest='pony_counts', required=True, help='Json file')
    parser.add_argument('-n','--num_words',type=int,required=True, help='Number of words to print')

    args = parser.parse_args()
    compute_pony_lang(args.pony_counts, args.num_words)




if __name__ == '__main__':
    main()