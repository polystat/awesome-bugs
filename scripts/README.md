# CI scripts

This document describes lists of steps that each script performs.

## Code samples format checker

1. Identify directories containing code samples (directories without subdirs)
2. Check their content. They should contain
	- `README.md`
	- any source file
	- EO translations (0 or as many as needed)
	- `filters.txt`
3. Parse parameters from `README.md`
4. Validate them
5. Process them if needed
6. Generate `sample_parameters.json`

## Reports analysis

For each analyzer's report:

1. Parse report and extract required data
2. Put this data into the corresponding data structure (`AnalyzerReport`)
3. Filter errors according to error types specified in global and local filters.
4. For each error detected by the analyzer check if their line numbers correspond to ones specified in the parameters of the sample. If they correspond, it is a hit, if not it is a miss.
5. Check if there are samples that were not detected at all. They are considered as not found.

Then `hits.json`, `misses.json`, and `not_found.json` should be generated.


