class A {
	
	public int getValue (String value){
        return value.trim().length();
    }
}

class StringTrim {
    public static void main(String args[]){  
        A a = new A();
        System.out.println(10/a.getValue("   "));
    }

}