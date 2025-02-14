
from pathlib import Path
from tqdm import tqdm
import os
import pickle

from src.recom_search.model.model_output import SearchModelOutput
from src.recom_search.model.model_bfs import  bfs

from src.recom_search.model.baseline import baseline_recomb_sample, recomb_baseline
from src.recom_search.model.generic_search import GenericSearch
from src.recom_search.model.model_bfs_zip import bfs_rcb_any
from src.recom_search.model.exec_setup import tokenizer, model, dataset, dec_prefix, args, dict_io

from src.recom_search.model.util import *


def adjust_batch_size(max_len, task, dataset):
    if task == 'sum':
        bs = max_len * 16 / 25

    elif dataset == 'en-fr':
        bs = 12
    elif dataset == 'zh-en':
        bs = 12
    elif dataset == 'fr-en':
        bs = 12
    # TODO is there a reason why other lpairs wouldn't work?
    elif dataset == 'en-de':
        bs = 12
    elif dataset == 'en-ru':
        bs = 12
    elif task == 'table_to_text':
        bs = 12
    else:
        raise NotImplementedError
    # for dbs, we set ngroup to be 4

    group = 4
    bs = int(bs)
    while bs % group != 0:
        bs -= 1
    return max(bs,1)

def run_bs_recombination(args, model, input_doc, dec_prefix, param_sim_function, adjust=True):
    if args.task == 'table2text':
        input_ids = input_doc['input_ids']
    else:
        input_ids = tokenizer(
            input_doc, return_tensors="pt").input_ids.to(args.device)

    if args.max_len == -1:
        cur_max_len = input_ids.squeeze().size()[0] * 2
    else:
        cur_max_len = args.max_len
    # we already get our processed thing from the get-go
    if args.task == 'table2text':
        input_ids = input_doc 
        for k in input_ids.keys(): 
            input_ids[k] = input_ids[k].to(args.device)
    output = recomb_baseline(doc_input_ids=input_ids, dec_prefix=dec_prefix, param_sim_function=param_sim_function,
                              model=model, debug=False, beam_size=args.beam_size, max_len=cur_max_len, avg_score=args.avg_score)
    mo = SearchModelOutput(ends=output)
    return mo

def run_recom_sample(args, model, input_doc, dec_prefix, param_sim_function) -> SearchModelOutput:
    # for this just use dataloader as is
    if args.task == 'table2text':
        input_ids = input_doc['input_ids']
    else:
        input_ids = tokenizer(
            input_doc, return_tensors="pt").input_ids.to(args.device)

    if args.max_len == -1:
        cur_max_len = input_ids.squeeze().size()[0] * 2
    else:
        cur_max_len = args.max_len
    # we already get our processed thing from the get-go
    if args.task == 'table2text':
        input_ids = input_doc 
        for k in input_ids.keys(): 
            input_ids[k] = input_ids[k].to(args.device)
    output = baseline_recomb_sample(doc_input_ids=input_ids, dec_prefix=dec_prefix, param_sim_function=param_sim_function,
                                     model=model, max_len=cur_max_len, num_return_hypo=args.beam_size, top_p=args.top_p)

    mo = SearchModelOutput(ends=output)
    return mo


def run_bfs(args, model, tokenizer, inp, dec_prefix, param_sim_function, config_search):

    if args.task == 'table2text':
        input_ids = inp['input_ids']
    else:
        input_ids = tokenizer(
            inp, return_tensors="pt").input_ids.to(args.device)

    if args.max_len == -1:
        cur_max_len = input_ids.squeeze().size()[0] * 2
        comp_budget = cur_max_len * args.beam_size
    else:
        comp_budget = args.max_len * args.beam_size
        cur_max_len = args.max_len
    # we already get our processed thing from the get-go
    if args.task == 'table2text':
        input_ids = inp 
        for k in input_ids.keys(): 
            input_ids[k] = input_ids[k].to(args.device)
    output = bfs(doc_input_ids=input_ids, model=model, tokenizer=tokenizer, param_sim_function=param_sim_function, dec_prefix=dec_prefix, avg_score=args.avg_score, max_len=cur_max_len, k_best=args.k_best, comp_budget=comp_budget, config_heu=None, config_search=config_search)

    mo = SearchModelOutput(ends=output)
    return mo


def run_bfs_recombination(args, model, tokenizer, inp, dec_prefix, param_sim_function, config_search) -> SearchModelOutput:        
    config_heu = {
        'heu_seq_score': args.heu_seq_score,
        'heu_seq_score_len_rwd': args.heu_seq_score_len_rwd,
        'heu_pos': args.heu_pos,
        'heu_ent': args.heu_ent,
        'heu_word': args.heu_word
    }
    # for this just use dataloader as is
    if args.task == 'table2text':
        input_ids = inp['input_ids']
    else:
        input_ids = tokenizer(
            inp, return_tensors="pt").input_ids.to(args.device)

    if args.max_len == -1:
        cur_max_len = input_ids.squeeze().size()[0] * 2
        comp_budget = cur_max_len * args.beam_size
    else:
        comp_budget = args.max_len * args.beam_size
        cur_max_len = args.max_len
    # we already get our processed thing from the get-go
    if args.task == 'table2text':
        input_ids = inp 
        for k in input_ids.keys(): 
            input_ids[k] = input_ids[k].to(args.device)
    # TODO k_best of 5 is hard-coded, does that affect anything?
    output = bfs_rcb_any(doc_input_ids=input_ids, model=model, tokenizer=tokenizer, param_sim_function=param_sim_function, dec_prefix=dec_prefix, avg_score=args.avg_score,
                    max_len=cur_max_len, k_best=5, comp_budget=comp_budget, config_heu=config_heu, config_search=config_search)

    mo = SearchModelOutput(ends=output)
    return mo


def run_baseline(args, model, inp, dec_prefix, adjust=True):
    if args.task == 'sum' or args.task == 'table_to_text':
        forced_bos_token_id = None
    else:
        forced_bos_token_id = dec_prefix[-1]
    if args.max_len == -1:
        input_ids = tokenizer(inp, return_tensors="pt").input_ids
        cur_max_len = input_ids.squeeze().size()[0] * 2
    else:
        cur_max_len = args.max_len
    if adjust:
        adj_batch_size = max(adjust_batch_size(
            cur_max_len, args.task, args.dataset),1)
    else:
        adj_batch_size = args.beam_size
    if args.model == 'greedy':
        gs = GenericSearch(model, tokenizer,
                           device=args.device, beam_size=1, do_sample=False, min_len=args.min_len, max_len=cur_max_len, num_beam_hyps_to_keep=1)
    elif args.model == 'bs':
        # TODO changed this up
        gs = GenericSearch(model, tokenizer,
                           device=args.device, beam_size=args.beam_size, do_sample=False,
                           min_len=args.min_len,
                           max_len=cur_max_len,
                           num_beam_hyps_to_keep=args.beam_size
                           )
    elif args.model == 'dbs':
        gs = GenericSearch(model, tokenizer,
                           device=args.device, beam_size=adj_batch_size, do_sample=False,
                           min_len=args.min_len, max_len=cur_max_len,
                           num_beam_groups=4,
                           diversity_penalty=args.hamming_penalty,
                           num_beam_hyps_to_keep=adj_batch_size
                           )
    elif args.model == 'topp':
        gs = GenericSearch(model, tokenizer,
                           device=args.device, beam_size=1, do_sample=True, min_len=args.min_len, max_len=cur_max_len, num_beam_hyps_to_keep=adj_batch_size,
                           top_p=args.top_p)
    elif args.model == 'temp':
        gs = GenericSearch(model, tokenizer,
                           device=args.device, beam_size=1, do_sample=True,
                           min_len=args.min_len, max_len=cur_max_len, num_beam_hyps_to_keep=adj_batch_size,
                           temperature=args.temp
                           )
    else:
        raise NotImplementedError
    output_dict = gs.run(inp, forced_bos_token_id)

    return output_dict

    # output should be a list of str

def run_model(args, tokenizer, model, dataset, dec_prefix, wt_dir):

    # logging.info(args)
    nexample = args.nexample
    cnt = 0
    if not isinstance(dataset, zip):
        # TODO turn off shuffling
        print("no shuffle, assume already done")
        #try:
        #    dataset = dataset.shuffle(seed=1000)
        #except:
        #    print('no shuffling')
    else:
        temp = list(dataset)
        random.seed(1000)
        random.shuffle(temp)
        res1, res2 = zip(*temp)
        # res1 and res2 come out as tuples, and so must be converted to lists.
        res1, res2 = list(res1), list(res2)
        dataset = zip(res1, res2)
    logging.info(f"Truncate dataset to {nexample} examples")

    for idx, example in enumerate(tqdm(dataset)):
        try:
            cnt += 1
            if args.task.startswith('mt'):
                document = example[0]
                ref_sum = example[1]
                inp = document
                doc_id = idx
            elif args.dataset == 'cnndm':
                document = example['article']
                doc_id = example['id']
                ref_sum = example['highlights']
            elif args.dataset == 'xsum':
                # TODO switch back, hardcoding here
                document = example['document']
                #document = example[0]
                sents = document.split('\n')
                inp = "\n".join(sents[:10])[:5000]
                #ref_sum = example[1]
                ref_sum = example['summary']
                doc_id = example['id']
                #doc_id = idx
            elif args.dataset == 'custom':
                document = example[0]
                ref_sum = example[1]
                doc_id =  'undefined'
                inp = document
            elif args.task == 'table_to_text':
                document = example[0]
                ref_sum = example[1]
                inp = document
                doc_id = idx
            else:
                raise NotImplementedError("for customized dataset, use custom as the name of dataset and document|ref|uid for fields")
            # if 'Apple' not in document:
            #     continue
            logging.info(f"\n\n===Input Doc/Src: {str(document)[:2000]}\n---Sum/Tgt: {ref_sum}")
            param_sim_function = {
                'ngram_suffix': args.ngram_suffix,
                'len_diff': args.len_diff,
                'merge': args.merge
            }
            config_search = {
                'post': args.post,
                'post_ratio': args.post_ratio,  # ratio of model calls left for post finishing
                'dfs_expand': args.dfs_expand,
                'heu': args.use_heu
            }
            combined_dict = {**config_search, **param_sim_function}
            combined_dict['avgsco'] = args.avg_score
            combined_dict['lenrwd'] = args.heu_seq_score_len_rwd
            combined_dict['topp'] = args.top_p

            config_name, fname = render_name(
                args.task, args.dataset, args.model, doc_id, document[:10], args.beam_size, args.max_len, combined_dict)
            fname += '.pkl'
            Path(os.path.join(wt_dir, config_name)).mkdir(parents=True, exist_ok=True)
            if os.path.exists(os.path.join(wt_dir, config_name, fname)):
                logging.info(f"File exists. Skip.")
                if cnt > nexample:
                    break
                continue
            
            if args.model in ['dbs', 'bs', 'greedy', 'topp', 'temp']:
                output = run_baseline(args, model, inp, dec_prefix)
            elif args.model == 'bs_recom':
                output = run_bs_recombination(
                    args, model, inp, dec_prefix, param_sim_function)
            elif args.model == 'sample_recom':
                output = run_recom_sample(
                    args, model, inp, dec_prefix, param_sim_function)
            elif args.model == 'bfs_recom':
                output = run_bfs_recombination(
                    args, model, tokenizer, inp, dec_prefix, param_sim_function, config_search=config_search)
            elif args.model == 'bfs':
                output = run_bfs(
                    args, model, tokenizer, inp, dec_prefix, param_sim_function, config_search=config_search)
            output.reference = ref_sum
            output.doc_id = doc_id
            output.document = document
            output.args = args

            with open(os.path.join(wt_dir, config_name, fname), 'wb') as fd:
                pickle.dump(output, fd)

            # break
            if cnt > nexample:
                break
        except:
            print("something failed")


if __name__ == "__main__":
    # execute only if run as a script
    run_model(args, tokenizer, model, dataset, dec_prefix, dict_io['data'])
