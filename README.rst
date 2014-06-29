===============
NewsNet backend
===============

-----
Collection of Apache Pig and Python scripts which were used to process
WebDataCommons page-to-page CommonCrawl data set.

To optimize for computational efficiency, time and the cost different tools were used:
1) Processing on 40 m1.small nodes Elastic Map-reduce(EMR) cluster using PIG. 
2) Data download, cleaning and pre-processing on Python on AWS m1.micro(free) or m3.large(memory-intensive) instances.
3) Processing on a Cloudera VM Hadoop Cluster installed locally(testing + small size processing)

  