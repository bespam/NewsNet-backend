-- Filter arcs table by target(id2) column only for news-domains index
arcs = load 's3n://wdc-weighted-graph/filter/filter-out/arcs2-sorted.gz' using PigStorage() as (id2: long, id1:long, id_new1:long);
index = load 's3n://wdc-weighted-graph/filter/filter-out/index-full-filtered-sorted2' using PigStorage() as (id_old:long, id_new:long);
d = join arcs by id2, index by id_old using 'merge';
arcs_filtered = foreach d generate $2, $4;
-- keep arcs-filtered in a separate dataset
store arcs_filtered into 's3n://wdc-weighted-graph/filter/filter-out/arcs-filtered2';
-- aggregate and convert to domain1, domain2, weight (to be used in graph)
arcs_filtered_w = foreach (group arcs_filtered by ($0, $1) parallel 1) generate flatten(group), COUNT(arcs_filtered);
store arcs_filtered_w into 's3n://wdc-weighted-graph/filter/filter-out/arcs-filtered2-w';