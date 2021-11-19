class A {
    protected int value;

    public int getValue (){
        return value;
    }
}

class B extends A{
    
    public int devideByValue (int x){
        return x/value; 
    }
}

class InheritedDefaultZeroDivision {
    public static void main(String args[]){  
        B b = new B();
        System.out.println(b.devideByValue(10));
    }

}