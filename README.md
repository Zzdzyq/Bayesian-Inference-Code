# Bayesian-Inference-Code
The code files accompanying the graduate report on Bayesian inference algorithm.

The files in the repository are to be used in the following order:

1. data_resave: directly applied to the raw data from the source page to compile them into monthly subsets.
2. data_load, pcp_map, city_ana: all to be applied to the monthly subsets from data_resave. data_load classifies the data into 1 and -1 for a selected region, and pcp_map and city_ana can be used to generate the global map on percentiles and city precipitation patterns as in the report.
3. edge_num, test_array_size: both to be applied to the classified data from data_load. edge_num generates plot of number of edges being generated compared number of samples selected when using data_load, manual manipultaion of data is required. test_array_size fits the classified data under 100 learning cycles as in the report, and saves the important learned properties and plotting some others.
4. graph_analysis, plot_learn: both to be applied to the saved results of test_array_size. graph_analysis produces a number of plots in the report analyzing the properties of the learned model. plot_learn generates the plots that are based on the map, including the general and the city-specific ones.
