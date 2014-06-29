-- map new page-index ids to new domain-index id
lines = load 's3n://wdc-weighted-graph/index-out/index-full.gz' using PigStorage() as (id_new: chararray, id_old:chararray);
index_filtered = load 's3://wdc-weighted-graph/filter/filter-out/index-new-filtered' using PigStorage() as (id1:chararray, dom:chararray);
d = join lines by id_new, index_filtered by id1 using 'replicated';
index_full_filtered = foreach d generate $0, $1;
store index_full_filtered into 's3://wdc-weighted-graph/filter/filter-out/index-full-filtered';