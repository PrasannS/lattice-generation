

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -adhoc -dataset xsum -ngram_suffix 4 -merge zip -device cuda:2

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -adhoc -dataset xsum -ngram_suffix 4 -merge zip -device cuda:2 -avg_score 0.5

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -adhoc -dataset xsum -ngram_suffix 4 -merge zip -device cuda:2 -avg_score 1


PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.7  -device cuda:2 -ngram_suffix 4 -merge zip

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.5  -device cuda:2 -ngram_suffix 4 -merge zip

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.3  -device cuda:2 -ngram_suffix 4 -merge zip


PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.7  -device cuda:2 -ngram_suffix 4 -merge zip -avg_score 0.5

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.5  -device cuda:2 -ngram_suffix 4 -merge zip -avg_score 0.5

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.3  -device cuda:2 -ngram_suffix 4 -merge zip -avg_score 0.5


PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.7  -device cuda:2 -ngram_suffix 4 -merge zip -avg_score 1

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.5  -device cuda:2 -ngram_suffix 4 -merge zip -avg_score 1

PYTHONPATH=./ python src/recom_search/command/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.3  -device cuda:2 -ngram_suffix 4 -merge zip -avg_score 1