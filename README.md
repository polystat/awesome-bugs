# AwesomeBugs

## Goal

Make a collection of code samples containing various bugs related to OOP together with their description and references. They should be generic and applicable to most object-oriented languages.

## What defects are considered:

Any defects that are:

- related to misuse of OOP techniques
- common for most OOP languages
- lead to any runtime error.

Some defects are not going to be included in this list because they might be ambiguous and dependant on the context.

- Security
- Maintainability
- Performance

## Ideology

Defects are represented by code samples containing them. Each code sample is a single source of file that is containing code that represents a single occurrence of the defect. Those code samples are assumed to be the input for static analyzers. Some metadata is needed and an exact structure of code samples is described below.

## Structure of this repository

```
├── `code` - Contains code samples
├── `docs` - Documentation
├── `res` - Resources. For now, only analyzers reports
├── `scripts` - Scripts for CI and report analysis
└── `global_filters.txt` - global error filters
```

## Structure of code samples

A valid code sample is a directory that does not contain any subdirectories and has the following files:

- `README.md` - contains the description and special header with metadata
- Single file with the source code of the sample
- Any number of files with EO translations
- `fitlers.txt` containing regex filters for static analysis results (more about it in the following sections)

`README.md` file should have a specific "header". It is a block of code with the following content


	```
	# Name        : Name of the code sample
	# FailureType : Type of failure (runtime error type)
	# ErrorType   : Type of error
	# Source      : Source from which this error was taken
	# CodeType    : Type of the code sample. For now only "Artificial" type is valid 
	# Lines       : Comma separated list of lines that contain the error
	```

For a detailed example of `README.md` refer to `code/test/README.md`

*IMPORTANT:* line numbers will be used to find if static analyzers find this error. If they will find an error in ANY of those lines, it will be considered as a hit.

The way to organize code samples is to put them in directories. For example, a valid path to code sample directory is `./code/error_type_1/error_sub_type_2/sample_1`

The structure of code samples is validated using CI scripts configured in this repository. If the pipeline fails due to incorrect `README.md` format or incorrect code sample directory structure, the error message could be found in the pipeline logs on the `Format checker` stage.

## Integration with static analyzers

Static analyzers can be integrated into CI or can be run separately. Reports that they produce can be used as input for the report analyzer. The output is a summary containing hits, misses, and not found samples for each of the static analyzers. The report analyzer is integrated into CI and its results can be found in the corresponding stage of the pipeline. It generates a small summary in logs (just plain numbers) and several artifacts which can be used for deeper analytics.

For now, only Coverity reports are supported. They cannot be generated in CI, so they have to be added manually to the `res` directory. The exact path of the report is `res/coverity.xlsx`.

The error found by the analyzer is considered as a hit (detected by the analyzer) if the analyzer will find an error in any of the lines specified in the code sample's `README.md`.

## Handling false positives

To handle false positives results produced by analyzers, some types of errors can be ignored. They can be defined in:

- `/global_filters.txt` - global filters for all code samples
- `<code_sample_path>/filters.txt` - filters local to specific code sample

Each line of those files contains a REGEX pattern which will be used to filter error types.

We assume that type error + line number combination will be too much.


## CI pipeline

CI pipeline checks that all code samples are formatted correctly and analyses report from static analyzers. The description of the output is described in the next section. For implementation details, refer to `docs/ci_scripts.md`

CI pipeline is using 2 scripts. 
- `scripts/format_checker.py` - checks the format of code samples
- `scripts/analyzer_report_checker.py` - analyzes static analyzers' reports

The scripts used for CI can be run locally. To do that, you need Python 3 and `scripts/requirements.txt` installed. Both of them should be run from the root directory of the repository. Commands are:

- `python scripts/format_checker.py`
- `python scripts/analyzer_report_checker.py`

## Output

The pipeline consists of two main stages: format checker and reports analysis. It generates several artifacts and logs.

### Logs

- Format checker logs will help you to see whether your code sample was found and what formatting issues it may have. Example output:

```
// Example of a successful run
processing code/A1 ... OK
processing code/A2 ... OK
processing code/A3 ... OK
processing code/A4 ... OK
Done!

// Example of an error
ERROR:root:Path 'code/faulty' should contain code sample, but there is no README.md (it is case sensitive)
```
	

- Report analysis logs to provide a small summary that tells what analyzers were able to find. Example output:

```
'coverity' analyzer produced: 
4 hits (0.6666666666666666 of max 6)
16 (0.2962962962962963 of all results)
2 samples were not found. They are:

code/tricky1
code/tricky2

Done!
```

### Artifacts

Report analysis produces several artifacts that can be used for deeper analysis.

- .csv reports containing the output of static analyzers converted to a single format. Example output of `coverity.csv`

| code sample path | file path | line | error type | report reference line number |
| ---------------- | --------- | ---- | ---------- | ---------------------------- |
| code/Infer/NullPointerExceptions/Nullable | code/Infer/NullPointerExceptions/Nullable/InferNullableTests.java | 21 | cov:USELESS_CALL:Useless call:Incorrect expression | 1 |
| code/Infer/NullPointerExceptions/Trivial | code/Infer/NullPointerExceptions/Trivial/InferTrivialNPETests.java | 130 | cov:NULL_RETURNS:Dereference null return value:Null pointer dereferences | 2 |
| code/Infer/NullPointerExceptions/Trivial | code/Infer/NullPointerExceptions/Trivial/InferTrivialNPETests.java | 164 | cov:USELESS_CALL:Useless call:Incorrect expression | 3 |

- `hits.json` - contains lists of references to errors sorted by analyzer name that are considered as hits (they correspond to lines described in the readme of code samples)

```
{"coverity": [2, 17, 21, 33]}
```

- `misses.json` - contains lists of references to errors sorted by analyzer name that is considered as misses (they do not correspond to lines described in the readme of code samples)

```
{"coverity": [12, 19, 20, 22, 26, 29, 31, 32, 41, 42, 43, 48, 49, 52, 53, 54]}
```

- `not_found.json` - contains lists of code samples that were not found by analyzers

```
{"coverity": ["code/tricky1", "code/tricky2"]}
```

Also, the format checker generates `samples_parameters.json` that contains parameters parsed from READMEs of each sample. Example:

```
{
    "code/Infer/NullPointerExceptions/Nullable": {
        "Name": "Very tricky error",
        "FailureType": "Null Pointer Exceptions",
        "ErrorType": "Programming error",
        "Source": "Creadible source",
        "CodeType": "Artificial",
        "Lines": [
            1,
            2,
            3
        ]
    },
    ...
}
```


