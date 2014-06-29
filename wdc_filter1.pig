-- filter domains index, which contains all the internet 1st, 2nd level domains for news-domains
lines = load 's3n://wdc-weighted-graph/index-out/index-new.gz' using PigStorage() as (id_new: chararray, dom1:chararray);
dom_filter = load 's3n://wdc-weighted-graph/filter/all-news-domains' using PigStorage() as (dom2:chararray);
d = join lines by dom1, dom_filter by dom2 using 'replicated';
index_filtered = foreach d generate $0, $1;
store index_filtered into 's3://wdc-weighted-graph/filter/filter-out/index-new-filtered';