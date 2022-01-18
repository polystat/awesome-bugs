# CI scripts

This document describes the CI process and each step of it.
NOTE: The working directory for all scripts is the root of the project.

CI process contains such steps:
  1. Source files extraction
  2. Build sources
  3. Clang-tidy analysis
  4. Polystat analysis
  5. Reports analysis

## 1. Source files extractor
Takes 2 arguments:
  - a path to a folder with YAML files (e.g. `tests`);
  - a path to a resulting temp folder with source files (e.g. `temp/sources`),

and:
  - searching for YAML files;
  - process files;
    - check required keys;
    - extract bad and good sources;
    - put extracted sources to resulting folder.

## 2. Build sources
Takes 2 arguments:
  - a path to a folder with source files (e.g. `temp/sources`);
  - a path to a resulting build folder (e.g. `build`),

and:
  - generate CMakeList from CPP source files;
  - build based on the CMakeList file into the resulting folder.

## 3. Clang-tidy analysis
Here parallel clang-tidy runner from LLVM is used. It takes a path to a build folder (e.g. `build`, result from step 2) as an argument and returns a report in a file (output redirection to the file, e.g. `> results/clang-out.txt`).

## 4. Polystat analysis
Takes 4 arguments:
  - a path to polystat.jar file;
  - a path to a folder with EO source files (e.g. `temp/sources/eo`);
  - a path to a temp folder for interim Polystat processes (e.g. `temp/polystat`);
  - a path to a folder where a report will be generated (e.g. `results`),

and form a report based on the analysis results of each `.eo` file in the EO source folder.

## 5. Reports analysis
In this step, the final .tex report generating, based on reports from steps 3-4.
It assumes such a structure of files:
```
awesome-bugs/
  results/
    clang-out.txt
    eo-out.txt
  temp/
    polystat/
    sources/
      cpp/
      eo/
```
