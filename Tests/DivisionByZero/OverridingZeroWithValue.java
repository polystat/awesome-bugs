//Nevative test

class A {
    public int getValue (){
        return 0;
    }
}

class B extends A{
    public int getValue (){
        return 10; 
    }
}

class OverridingZeroWithValue {
    public static void main(String args[]){  
        B b = new B();
        System.out.println(10/b.getValue());
    }
}