class A {

    public int getValue (int value){
        return value;
    }
	
	public int getValue (String value){
        return 0;
    }
}

class Overloading {
    public static void main(String args[]){  
        A a = new A();
		System.out.println(a.getValue());
        System.out.println(a.getValue("Hello"));
    }

}