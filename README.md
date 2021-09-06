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

Defects are represented by code samples containing them. Each code sample is a single source of file that is containing code which represents a single occurrence of the defect. Those code samples are assumed to be the input for static analyzers. Some metadata is needed and an exact structure of code samples is described below.

## Structure of this repository

├── `code` - Contains code samples
├── `docs` - Documentation
├── `res` - Resources. For now, only analyzers reports
├── `scripts` - Scripts for CI and report analysis
└── `global_filters.txt` - global error filters

## Structure of code samples

A valid code sample is a directory that does not contain any subdirectories and has following files:

- `README.md` - contains description and special header with metadata
- Single file with the source code of the sample
- Any number of files with EO translations
- `fitlers.txt` containing regex filters for static analysis results

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

The way to organize code samples is to put them in directories. For example, a valid path to code sample directory is `./code/error_type_1/error_sub_type_2/sample_1`

The structure of code samples is validated using CI scripts configured in this repository. If pipeline fails due to incorrect `README.md` format or incorrect code sample directory structure, the error message could be found in the pipeline logs on `Format checker` stage.

## Integration with static analyzers

<TODO>