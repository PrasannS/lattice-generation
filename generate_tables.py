# given a folder with all the graphs given by numerical index, and another with exploded
# paths of corresponding stuff, generate tables for all the respective data (limit of max index)

import pickle 
import pandas as pd
import os
import random
import nltk
from encode_utils.mt_scores import get_scores_auto
import encode_utils.rerank_data as rd

PKLBASE = "outputs/graph_pickles/"
# make n sample test set
def make_sample_test (explode_dir, n=32, lim=-1, seed=1):
    random.seed(seed)
    base = PKLBASE+explode_dir
    pklnames = os.listdir(base)
    if lim>0:
        pklnames = pklnames[:lim]
    res = []
    for p in pklnames:
        with open(base+p, "rb") as input_file:
            explode = pickle.load(input_file)
            
            phoc, cands, ref, src = explode
        # get the sample, construct the data
        if n>0: # negative n just means we're using exploded set
            cands = random.sample(cands, n)
        for ind in range(len(cands)):
            res.append({
                "src":src,
                "ref":ref,
                "hyp":cands[ind]
            })
    return pd.DataFrame(res)

def get_posunique(sentence, noun):
    options = ["VB", "VBP"]
    if noun:
        options = ["NN", "NNP", "NNS"]
    text = nltk.word_tokenize(sentence)
    pos_tagged = nltk.pos_tag(text)
    unwords = set()
    for p in pos_tagged:
        if p[1] in options:
            unwords.add(p[0])
    return len(unwords)

def metrics_mapping (metric, tset):
    hyps, srcs, refs, = list(tset['hyp']), list(tset['src']), list(tset['ref'])
    if metric in tset.keys():
        print("already got it")
        return
    if metric=="utnoun":
        tset[metric] = get_scores_auto(hyps, ["noun"]*len(hyps), [], "utnoun", "comstyle")
    elif metric=="unique_nouns":
        tset[metric] = [get_posunique(s, True) for s in hyps]
    elif metric=="cqe":
        tset[metric] = get_scores_auto(hyps, srcs, refs, "cqe", "")
    elif metric=="comet":
        tset[metric] = get_scores_auto(hyps, srcs, refs, "comet", "")
    elif metric=="posthoc":
        tset[metric] = get_scores_auto(hyps, srcs, refs, "posthoc", "fr-en")
    elif metric=="dupcqe":
        tset[metric] = get_scores_auto(hyps, srcs, refs, "dupcqe", "comstyle")
    # TODO add support for the english->russian table later
    else:
        print("invalid metric")


if __name__=="__main__":
    
    savefile = "frenexplodev1.csv"
    metrics = ['comet', 'cqe', 'posthoc', 'dupcqe']
    #metrics = ['utnoun', 'unique_nouns']

    if os.path.exists("outputs/score_csvs/"+savefile):
        tset = pd.read_csv("outputs/score_csvs/"+savefile, index_col=0)
    else:
        tset = make_sample_test("frenchtest_exploded/", -1, 100)
    
    tset = tset.dropna()
    print("size of dset: ", len(tset))
    # generate necessary scores
    for m in metrics:
        metrics_mapping(m, tset)
        tset.to_csv("outputs/score_csvs/"+savefile)

    print(tset.keys())
    # do re-ranking, save results in a json file

    
