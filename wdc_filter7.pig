-- Filter the original arcs dataset by source(id2) column only for news-domains index
arcs = load 's3n://wdc-weighted-graph/arcs' using PigStorage() as (id1: long, id2:long);
index = load 's3n://wdc-weighted-graph/filter/filter-out/index-full-filtered-sorted2' using PigStorage() as (id_old:long, id_new:long);
d = join arcs by id1, index by id_old using 'merge';
arcs_filtered = foreach d generate $0, $1, $3;
-- Save and prepare for second filter for target column
store arcs_filtered into 's3n://wdc-weighted-graph/filter/filter-out/arcs-filtered';