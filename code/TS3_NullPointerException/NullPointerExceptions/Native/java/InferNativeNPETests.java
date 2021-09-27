import javax.annotation.Nullable;
import javax.annotation.Nonnull;

public class InferNativeNPETests{

    native boolean test();

    Object getObj() {
        if (test()) {
        return new Object();
        } else {
        return null;
        }
    }

    Boolean getBool() {
        if (test()) {
        return new Boolean(true);
        } else {
        return null;
        }
    }

    void badCheckShouldCauseNPE() {
        if (getBool() != null) getObj().toString();
    }

    public native @Nullable Object undefNullableRet();

    public void derefUndefNullableRet() {
        Object ret = undefNullableRet();
        ret.toString();
    }

    public void derefUndefNullableRetOK() {
        Object ret = undefNullableRet();
        if (ret != null) {
        ret.toString();
        }
    }

    void assumeUndefNullableIdempotentOk() {
        if (undefNullableRet() != null) {
        undefNullableRet().toString();
        }
    }

    public Object undefNullableWrapper() {
        return undefNullableRet();
    }

    public void derefUndefNullableRetWrapper() {
        undefNullableWrapper().toString();
    }
    private int returnsThreeOnlyIfRetNotNull(Object obj) {
        if (obj == null) {
        return 2;
        }
        return 3;
    }

    public void testNullablePrecision() {
        Object ret = undefNullableRet();
        if (returnsThreeOnlyIfRetNotNull(ret) == 3) {
        ret.toString(); // shouldn't warn here
        }
    }

    native Object unknownFunc();

    void nullDerefernceReturnOfSkippedFunctionBad() {
        Object object = unknownFunc();
        if (object == null) {
        object.toString();
        }
    }

    native @Nonnull Object doesNotReturnNull();

    void noNPEWhenCallingSkippedNonnullAnnotatedMethodGood() {
        Object object = doesNotReturnNull();
        if (object == null) {
        object.toString();
        }
    }

    Object callUnknownFunc() {
        return unknownFunc();
    }

}