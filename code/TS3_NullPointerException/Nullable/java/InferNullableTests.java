import javax.annotation.Nullable;

public class InferNullableTests {

    private @Nullable Object mFld;

    void nullableFieldNPE() {
        mFld.toString();
    }

    void guardedNullableFieldDeref() {
        if (mFld != null) mFld.toString();
    }

    void allocNullableFieldDeref() {
        mFld = new Object();
        mFld.toString();
    }

    void nullableParamNPE(@Nullable Object param) {
        param.toString();
    }

    void guardedNullableParamDeref(@Nullable Object param) {
        if (param != null) param.toString();
    }

    void allocNullableParamDeref(@Nullable Object param) {
        param = new Object();
        param.toString();
    }

    private Object mOkObj = new Object();

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