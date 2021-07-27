# AwesomeBugs

## Goal

Make a collection of code samples containing various bugs related to OOP together with their description and references. They should be generic and applicable to most object-oriented languages.

## Taxonomy of defects:

Type of defects given below are supposed to either produce runtime errors or to make a program hang.

> The taxonomy is not complete yet and soon to be moved to the separate document

### Non-OOP related:

- Access restrictions
  - Memory (segmentation faults)
- Underflows and overflows
  - Integers
  - Arrays
  - Buffers
  - Stacks
- Infinite execution paths
- Synchronization issues
  - Deadlock
  - Livelock
  - Starvation
- Resource leaks
  - Memory leak
- Logical errors
  - Violated contracts

### OOP related:

- Nulls
  - Null pointer exception
  - Null pointer dereferencing
- Type mismatches
  - Upcast-downcast problems
  - Missing methods/fields
- Uncaught exceptions

### Common design antipatterns

> TBD

## Reasoning

### OOP errors

OOP can be viewed as the way to structure the imperative or procedural code. Generally, all collisions that this structure may produce are found on the stage of compilation if the code is pure object-oriented. We may assume two general categories of problems related to OOP:
- Anti-patterns and bad design. Poorly designed code may work completely fine, however, it will have more weak spots that may produce errors with future modifications.
- Violations of OOP principles. They may produce errors that cannot be caught during compilation.

## What defects are not considered:

Some defects are not going to be included in this list because they might be ambiguous and dependant on the context.

- Security
- Maintainability
- Performance

## Structure of this repository

Main requirements:
- Ability to run static analysis on each of the code sample
- Each code sample should have corresponding tags according to its place in taxonomy
- Several samples of a similar bug can be provided

> The exact structure to be defined later
