#include <iostream>
#include <memory>

class InferNullableTests {

private:
    std::shared_ptr<int> mFld = nullptr;

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

    void nullableParamNPE(const std::shared_ptr<int>& param) {
        std::cout << param.get();
    }

    void guardedNullableParamDeref(const std::shared_ptr<int>& param) {
        if (param) std::cout << param.get();
    }

    void allocNullableParamDeref(std::shared_ptr<int> param) {
        param = std::make_shared<int>(12);
        std::cout << param.get();
    }

private:
    std::shared_ptr<int> mOkObj = std::make_shared<int>(12);

    public void nullableParamReassign1(@Nullable Object o) {
        if (o == null) {
        o = mOkObj;
        }
        o.toString();
    }

    public void nullableParamReassign2(@Nullable Object o, Object okObj) {
        if (o == null) {
        o = okObj;
        }
        o.toString();
    }

    private @Nullable Object mNullableField;

    public void nullableFieldReassign1() {
        if (mNullableField == null) {
        mNullableField = mOkObj;
        }
        mNullableField.toString();
    }

    public void nullableFieldReassign2(Object okObj) {
        if (mNullableField == null) {
        mNullableField = okObj;
        }
        mNullableField.toString();
    }

    public void nullableFieldReassign3(Object param) {
        mNullableField = param;
        mNullableField.toString();
    }

    public Object nullableGetter() {
        return mNullableField;
    }

    public void derefNullableGetter() {
        Object o = nullableGetter();
        o.toString();
    }

    public @Nullable Object nullableRet(boolean b) {
        if (b) {
        return null;
        }
        return new Object();
    }

    public void derefNullableRet(boolean b) {
        Object ret = nullableRet(b);
        ret.toString();
    }

    public void derefNullableRetOK(boolean b) {
        Object ret = nullableRet(b);
        if (ret != null) {
        ret.toString();
        }
    }

    interface I {
        @Nullable Object mObject = null;
    }

    class E implements I {

        void dereferenceNullableInterfaceFieldBad() {
        mObject.toString();
        }
    }


    public @Nullable String testSystemGetPropertyArgument() {
        String s = System.getProperty(null);
        return s;
    }
}