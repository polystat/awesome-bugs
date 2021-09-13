// From Facebook Infer tests

public class InferTrivialNPETests {

    class A {
        int x;
        
        public void method() {}
    }

    // npe local with field
    public int nullPointerException() {
        A a = null;
        return a.x;
    }

    public A canReturnNullObject(boolean ok) {
        A a = new A();
        if (ok) return a;
        else return null;
    }

    public static void expectNotNullObjectParameter(A a) {
        a.method();
    }

    public static void expectNotNullArrayParameter(A[] array) {
        array.clone();
    }

    // npe with branching, interprocedural
    public int nullPointerExceptionInterProc() {
        A a = canReturnNullObject(false);
        return a.x;
    }

    // npe with exception handling
    public int nullPointerExceptionWithExceptionHandling(boolean ok) {
        A a = null;
        try {
            throw new Exception();
            } catch (Exception e) {
            return a.x;
        }
    }

    class B {
        A a;
        
        void test() {}
    }

    public static int nullPointerExceptionWithArray() {
        A[] array = new A[] {null};
        A t = array[0];
        return t.x;
    }

    // npe with a chain of fields
    class C {
        B b;
    }

    public int nullPointerExceptionWithAChainOfFields(C c) {
        c.b = new B();
        return c.b.a.x;
    }

    // npe with a null object parameter
    public static void nullPointerExceptionWithNullObjectParameter() {
        expectNotNullObjectParameter(null);
    }

    // npe with a null array parameter
    public static void nullPointerExceptionWithNullArrayParameter() {
        expectNotNullArrayParameter(null);
    }


    int x;

    public void nullPointerExceptionFromNotKnowingThatThisIsNotNull() {
        if (this == null) {}
        this.x = 4;
    }

    public <T> T id_generics(T o) {
        o.toString();
        return o;
    }

    public A frame(A x) {
        return id_generics(x);
    }

    public void nullPointerExceptionUnlessFrameFails() {
        String s = null;
        Object a = frame(new A());
        if (a instanceof A) {
            s.length();
            }
    }


    public void genericMethodSomewhereCheckingForNull(String s) {
        if (s == null) {}
    }

    void nullPointerExceptionInArrayLengthLoop(Object[] arr) {
        for (int i = 0; i < arr.length; i++) {
            Object x = null;
            x.toString();
        }
    }
        
    void nullPointerExceptionArrayLength() {
        Object[] arr = null;
        int i = arr.length;
    }

    Object[] arr = new Object[1];

    Object arrayReadShouldNotCauseSymexMemoryError(int i) {
        arr[i].toString();
        return null;
    }

    void nullPointerExceptionCallArrayReadMethod() {
        arr[0] = new Object();
        arrayReadShouldNotCauseSymexMemoryError(0).toString();
    }

    // TODO : Need to find more info about next 3 functions

    Object retUndefined() {
        return "".toString(); // toString is a skip function
    }

    Object derefUndefinedCallee() {
        // if retUndefined() is handled incorrectly, we get a symexec_memory_error here
        retUndefined().toString();
        return null;
    }

    void derefNull() {
        // should be NPE, but will not be reported if we handled retUndefined() incorrectly
        derefUndefinedCallee().toString();
    }


    class L {
        L next;
    }

    Object returnsNullAfterLoopOnList(L l) {
        while (l != null) {
        l = l.next;
        }
        return null;
    }

    void dereferenceAfterLoopOnList(L l) {
        Object obj = returnsNullAfterLoopOnList(l);
        obj.toString();
    }

}