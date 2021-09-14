cmake_minimum_required(VERSION 3.20)
project(AwesomeBugs)

set(CMAKE_CXX_STANDARD 14)

add_executable(AwesomeBugs
        code/Infer/DivideByZero/c++/TODO_in_c++_DivideByZero.cpp
        code/Infer/DivideByZero/c++/TODO_in_c++_InferNullableTests.cpp
        code/Infer/NullPointerExceptions/Native/c++/TODO_in_c++_InferNativeNPETests.cpp
        code/Infer/NullPointerExceptions/Nullable/c++/TODO_in_c++_InferNullableTests.cpp
        code/Infer/NullPointerExceptions/Trivial/c++/TODO_in_c++_InferTrivialNPETests.cpp
        code/Infer/NullPointerExceptions/WithStandardLib/c++/TODO_in_c++_InferSTDLibNPETests.cpp
        code/JavaRecursionExamples/mutualrec/non_term/derived_again/c++/TODO_in_c++_DerivedAgainExample.cpp
        code/JavaRecursionExamples/mutualrec/non_term/example/c++/TODO_in_c++_MutualRecursionExample.cpp
        code/JavaRecursionExamples/mutualrec/non_term/factory/c++/TODO_in_c++_Factory.cpp
        code/JavaRecursionExamples/mutualrec/non_term/long_chain/c++/TODO_in_c++_LongChain.cpp
        code/JavaRecursionExamples/mutualrec/non_term/two_derived/c++/TODO_in_c++_TwoDerived.cpp
        code/JavaRecursionExamples/mutualrec/non_term/two_derived_explicit_decoration/c++/TwoDerivedExplicitDecoration.cpp
        code/test/c++/hello_world.cpp)
