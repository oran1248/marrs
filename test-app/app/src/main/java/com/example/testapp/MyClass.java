package com.example.testapp;

import android.util.Log;

public class MyClass{
    // static field
    private final static int si = 100;
    private final static Integer sI = 101;
    private final static SampleClass sSample = new SampleClass("ToString2");
    private final static SampleClass sSampleNull = null;

    // instance fields
    private final String[] as = {"a","bb","ccc"};
    private final String[] ass = {"33","33","33"};
    private final int[][] ai = {{1},{2},{3}};
    private final int[] aii = {1,2,3};
    private final Integer[][][] aI = {{{1}}};

    private final SampleClass someNullValue = null;
    private final SampleClass sampleClassInstance = new SampleClass(1, 1.1, 'c', "sss", true, (byte)33, 5555, (float)22.33);
    private final SampleClass sampleClassIstance2 = new SampleClass(new Integer(1), new Double(1.1), new Character('c'), "sss", new Boolean(true), new Byte((byte)33), new Long(5555), new Float(22.33));

    private final byte b = 1;
    private final Byte B = 2;

    private final int i = 3;
    private final Integer I = 4;

    private final short s = 5;
    private final Short S = 6;

    private final double d = 7.7;
    private final Double D = 8.8;

    private final float f = (float)7.7;
    private final Float F = (float)8.8;

    private final char c = 'c';
    private final Character C = 'C';

    private final boolean bool = true;
    private final Boolean Bool = false;

    private final String Str = "sample-string...";


    static class A {
        private static int a = 9;
        private int b;
        public A(){
            b=1;
        }
        public A(int x){
            b=x;
        }
        @Override
        public String toString() {
            return "Ainstance";
        }

        private static int f(){
            return -2;
        }
        private int g(){
            return -3;
        }
        public int gg(){
            return a;
        }
    }
    static class B extends A {
        @Override
        public String toString() {
            return "Binstance";
        }
    }
    private A itsb = new B();

    // constructors
    public MyClass(){

    }

    private int tmp = -7;
    private MyClass (MyClass c){
        this.tmp = 120;
    }

    // static methods
    private static int overload(String s){ return 1; }
    private static void overload(int x, Double y){ return; }
    private static void voidFunc(){  }
    private static double f(int x, double y){
        Log.d("MyAppTag", "private static int f(int x, double y)");
        return x*y;
    }
    private static String  sarrayFunc(int [] arr){
        return "1";
    }
    private static String  sarrayFunc(Integer[] arr){
        return "2";
    }
    private static String sarrayFunc(SampleClass[] arr){
        return "3";
    }

    // instance methods
    private String sampleString(SampleClass s1, SampleClass s2, String s, int x){
        return s1.toString()+s2.toString()+s+String.valueOf(x);
    }

    private void overload(){

    }
    private SampleClass getSample () {
        return sampleClassInstance;
    }
    private int a1(int[] y){
        return y[0];
    }
    private int a2(int[][] y){
        return y[1][0];
    }
    private int a3(int[][][] y){
        return y[1][1][0];
    }

    private int overload(int y){
        return y;
    }


    private static A[] sgetArr(String s) {
        return new A[]{new A(), new B()};
    }
    private static B[][] sgetArr2(char s) {
        return new B[][]{{new B()},{new B(), new B()},{new B()}};
    }
    private static String[][][] sgetArr3(short s) {
        return new String[][][]{{{"1","2"}},{{"3","4"}}};
    }

    private double arrayFunc(int [] arr, double d){
        int s = 0;
        for (int x : arr){
            s+=x;
        }
        return s*d;
    }
    private int arrayFunc(Integer[] arr, Double d){
        return 2;
    }
    private int arrayFunc(SampleClass[] arr, Character c){
        return 3;
    }

    private String darrayFunc(String[][] arr){
        String s ="";
        for(int i=0;i<arr.length;i++){
            for(int j=0;j<arr[i].length; j++){
                s+=arr[i][j];
            }
        }
        return s;
    }

    private int gg(String s, Object o, byte b){
        return -1;
    }

    private int[] getArr(String s) {
        return new int[]{1,2,3};
    }
    private int[][] getArr2(char s) {
        return new int[][]{{1},{2,3},{3}};
    }
    private Integer[][][] getArr3(short s) {
        return new Integer[][][]{{{1,2}},{{3,4}}};
    }

    private int uu(int x){
        return 11;
    }
    private int uu(Integer x){
        return 22;
    }

    @Override
    public String toString() {
        return "ToString1";
    }
}
