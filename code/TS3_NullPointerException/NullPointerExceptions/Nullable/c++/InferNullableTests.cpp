#include <iostream>
#include <memory>

class InferNullableTests {

private:
    std::shared_ptr<int> mFld = nullptr;
    std::shared_ptr<int> mOkObj = std::make_shared<int>(12);
    std::shared_ptr<int> mNullableField;


public:
    InferNullableTests() = default;

    void nullableFieldNPE() {
        std::cout << mFld.get();
    }

    void guardedNullableFieldDeref() {
        if (mFld) {
            std::cout << mFld.get();
        }
    }

    void allocNullableFieldDeref() {
        mFld = std::make_shared<int>(12);
        std::cout << mFld.get();
    }

    void nullableParamNPE(const std::shared_ptr<int> &param) {
        std::cout << param.get();
    }

    void guardedNullableParamDeref(const std::shared_ptr<int> &param) {
        if (param) std::cout << param.get();
    }

    void allocNullableParamDeref(std::shared_ptr<int> param) {
        param = std::make_shared<int>(12);
        std::cout << param.get();
    }

    void nullableParamReassign1(std::shared_ptr<int> o) {
        if (o == nullptr) {
            o = mOkObj;
        }
        std::cout << o.get();
    }


    void nullableParamReassign2(std::shared_ptr<int> o, std::shared_ptr<int> okObj) {
        if (o == nullptr) {
            o = okObj;
        }
        std::cout << o.get();
    }

    void nullableFieldReassign1() {
        if (mNullableField == nullptr) {
            mNullableField = mOkObj;
        }
        std::cout << mNullableField.get();
    }


    void nullableFieldReassign2(std::shared_ptr<int> okObj) {
        if (mNullableField == nullptr) {
            mNullableField = okObj;
        }
        std::cout << mNullableField.get();;
    }

    void nullableFieldReassign3(std::shared_ptr<int> param) {
        mNullableField = param;
        std::cout << mNullableField.get();;
    }

    std::shared_ptr<int> nullableGetter() {
        return mNullableField;
    }

    void derefNullableGetter() {
        std::shared_ptr<int> o = nullableGetter();
        std::cout << o.get();
    }

    std::shared_ptr<int> nullableRet(bool b) {
        if (b) {
            return nullptr;
        }
        return std::make_shared<int>(12);
    }

    void derefNullableRet(bool b) {
        std::shared_ptr<int> ret = nullableRet(b);
        std::cout << ret.get();
    }

    void derefNullableRetOK(bool b) {
        std::shared_ptr<int> ret = nullableRet(b);
        if (ret != nullptr) {
            std::cout << ret.get();
        }
    }

    class I {
    public:
        std::shared_ptr<int> mObject = nullptr;
    };

    class E : public I {
        void dereferenceNullableInterfaceFieldBad() {
            std::cout << mObject.get();
        }
    };

// Don't know the C++ equivalent of this check

//public @Nullable String testSystemGetPropertyArgument() {
//        String s = System.getProperty(null);
//        return s;
//    }

};

int main() {
    auto *nullableTests = new InferNullableTests();
    return 0;
}