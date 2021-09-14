/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// package codetoanalyze.java.infer;

#include "string"

class DivideByZero {

public:
    int divByZeroLocal(std::string s) {
        int denominator = 0;
        int nominator = 10;
        int result = nominator / denominator;
        return result;
    }

    int divideByZeroInterProc(int denominator) {
        return 10 / denominator;
    }

    int callDivideByZeroInterProc() {
        return divideByZeroInterProc(0);
    }

    void setXToZero() {
        x = 0;
    }

    int divideByZeroWithStaticField() {
        setXToZero();
        return divideByZeroInterProc(x);
    }


    // divide by zero with static fields
private:
    int x;

}

int main(int argc, std::string* argv) {
    DivideByZero divBy0;
    divBy0.divByZeroLocal("stuff")
}