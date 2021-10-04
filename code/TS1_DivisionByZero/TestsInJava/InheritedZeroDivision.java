class A {
    protected int value = 0;

    public int getValue (){
        return value;
    }
}

class B extends A{
    
    public int devideByValue (int x){
        return x/value; 
    }
}

class InheritedZeroDivision {
    public static void main(String args[]){  
        B b = new B();
        System.out.println(b.devideByValue(10));
    }

}