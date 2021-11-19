class A {

    public int getValue (int value){
        return value;
    }
	
	public int getValue (String value){
        return value.trim().length();
    }
}

class OverloadingAndStringTrim {
    public static void main(String args[]){  
        A a = new A();
		System.out.println(a.getValue(1));
        System.out.println(a.getValue("   "));
    }

}