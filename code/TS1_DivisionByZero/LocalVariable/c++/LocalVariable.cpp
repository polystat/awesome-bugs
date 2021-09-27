/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// package codetoanalyze.java.infer;

class DivideByZero {

public:
    DivideByZero() = default;
    int divByZeroLocal() {
        int denominator = 0;
        int nominator = 10;
        int result = nominator / denominator;
        return result;
    }

};

//int main() {
//    auto* divBy0 = new DivideByZero();
//    divBy0->divByZeroLocal("stuff");
//    return 0;
//}