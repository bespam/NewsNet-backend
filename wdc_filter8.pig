-- resort arcs-filtered by target(id2) to merge sort effectively
arcs = load 's3n://wdc-weighted-graph/filter/filter-out/arcs-filtered-split.gz' using PigStorage() as (id1: long, id2:long, id_new: long);
arcs_sorted = order arcs by id2;
store (foreach arcs_sorted generate $1, $0, $2) into 's3://wdc-weighted-graph/filter/filter-out/arcs2-sorted.gz';