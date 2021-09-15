package com.example.testapp;

import android.util.Log;

public class SampleClass {
    private final static int staticField = 1002;

    private final short instanceField = 67;
    private String s = "empty";
    private int sum = 0;

    public SampleClass f() {// so it will not remove private ctor SampleClass()
        return new SampleClass();
    }

    // constructors
    private SampleClass(){
        sum = -1;
    }
    public SampleClass(int x) {
        this.s = "i1";
    }
    public SampleClass(Integer x) {
        this.s = "i2";
    }
    private SampleClass(Integer[][] arr){
        for(Integer[] i : arr){
            for(Integer j : i){
                sum -= j;
            }
        }
    }
    private SampleClass(int[][] arr){
        for(int[] i : arr){
            for(int j : i){
                sum += j;
            }
        }
    }
    private SampleClass(int[] arr){
        for(int i : arr){
            sum += i;
        }
    }

    private SampleClass(Integer[] arr){
        for(int i : arr){
            sum -= i;
        }
    }



    public SampleClass(String s){
        this.s=s;
    }
    public SampleClass(SampleClass sc){
        this.s="sc";
    }

    public SampleClass(int a, double d, char c, String s, boolean b, byte bb, long l, float f) {
        this.s = "s1";
    }

    public SampleClass(Integer a, Double d, Character c, String s, Boolean b, Byte bb, Long l, Float f) {
        this.s = "s2";
    }

    @Override
    public String toString() {
        return s;
    }

}
