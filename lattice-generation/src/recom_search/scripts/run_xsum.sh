

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dfs_expand -dataset xsum -ngram_suffix 4 -merge zip -device cuda:1

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dfs_expand -dataset xsum -ngram_suffix 4 -merge zip -device cuda:1 -avg_score 0.5

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dfs_expand -dataset xsum -ngram_suffix 4 -merge zip -device cuda:1 -avg_score 1


PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.7  -device cuda:1 -ngram_suffix 4 -merge zip

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.5  -device cuda:1 -ngram_suffix 4 -merge zip

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.3  -device cuda:1 -ngram_suffix 4 -merge zip


PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.7  -device cuda:1 -ngram_suffix 4 -merge zip -avg_score 0.5

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.5  -device cuda:1 -ngram_suffix 4 -merge zip -avg_score 0.5

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.3  -device cuda:1 -ngram_suffix 4 -merge zip -avg_score 0.5


PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.7  -device cuda:1 -ngram_suffix 4 -merge zip -avg_score 1

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.5  -device cuda:1 -ngram_suffix 4 -merge zip -avg_score 1

PYTHONPATH=./ python src/recom_search/scripts/run_pipeline.py -model astar -dataset xsum -post -post_ratio 0.3  -device cuda:1 -ngram_suffix 4 -merge zip -avg_score 1