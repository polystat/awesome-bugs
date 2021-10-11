cmake_minimum_required(VERSION 3.20)
project(AwesomeBugs)

set(CMAKE_CXX_STANDARD 14)

add_executable(AwesomeBugs
        code/CITest/c++/HelloWorld.cpp
        code/TS1_DivisionByZero/FunctionCall/c++/FunctionCall.cpp
        code/TS1_DivisionByZero/LocalVariable/c++/LocalVariable.cpp
        code/TS1_DivisionByZero/StaticField/c++/StaticField.cpp
        code/TS2_RecursiveCall/derived_again/c++/DerivedAgainExample.cpp
        code/TS2_RecursiveCall/example/c++/MutualRecursionExample.cpp
        code/TS2_RecursiveCall/factory/c++/Factory.cpp
        code/TS2_RecursiveCall/long_chain/c++/LongChain.cpp
        code/TS2_RecursiveCall/two_derived/c++/TwoDerived.cpp
        code/TS2_RecursiveCall/two_derived_explicit_decoration/c++/TwoDerivedExplicitDecoration.cpp
        code/TS3_NullPointerException/Nullable/c++/InferNullableTests.cpp
        code/TS4_NumericConversions/FloatToInt/c++/FloatToInt.cpp
        code/TS4_NumericConversions/NumericToBoolean/c++/NumericToBoolean.cpp)
