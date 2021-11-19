enum EnumWithValues {
    A(0),
    B(1),
    C(2);

    private int value;

    EnumWithValues(int value) {
        this.value = value;
    }
	
	public int value() {
        return this.value;
    }
}
class EnumWithValuesZeroDevision {
    public static void main(String args[]){
        EnumWithValues a = EnumWithValues.A;
        System.out.println(10/a.value());
    }
}