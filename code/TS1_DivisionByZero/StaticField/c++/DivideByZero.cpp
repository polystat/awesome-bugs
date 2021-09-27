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
    void setXToZero() {
        x = 0;
    }

    int divideByZeroWithStaticField() {
        setXToZero();
        return divideByZeroInterProc(x);
    }

    // divide by zero with static fields
private:
    static int x;

};

//int main() {
//    auto* divBy0 = new DivideByZero();
//    divBy0->divByZeroLocal("stuff");
//    return 0;
//}