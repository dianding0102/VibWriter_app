package com.example.test2;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.accessibility.AccessibilityViewCommand;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.ExecutorService;


public class MainActivity extends AppCompatActivity {

    private SensorManager sensorManager;
    private Sensor sensor;
    private TextView AccView;
    private Button button;
    private Button button2;

    float[] acc_x = new float[5000];
    float[] acc_y = new float[5000];
    float[] acc_z = new float[5000];
    long[] time = new long[5000];
    int index = 0;

    Socket socket = null;
    String letter;

    boolean StartRecord = false;
    boolean EndRecord = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        AccView = findViewById(R.id.AccView);
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);

        button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                sensorManager.registerListener(listener, sensor, SensorManager.SENSOR_DELAY_FASTEST);
                StartRecord = true;
                index = 0;
            }
        });

        button2 = findViewById(R.id.button2);
        button2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                EndRecord = true;
            }
        });
    }

    private SensorEventListener listener = new SensorEventListener() {
        public void onSensorChanged(SensorEvent event) {
            if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER & StartRecord) {
                getAccelerometer(event, index);
                index ++;
                //AccView.setText(index);
            }
            if (EndRecord){
//                LetterSent();
                LetterReg();
                AccView.setText(letter);
                Log.d("activity_main", "showing done.........");
                StartRecord = false;
                EndRecord = false;
            }
//            if(!letter.equals("")) {
//                AccView.setText(letter);
//                Log.d("activity_main", "showing done.........");
//            }
        }

        private void getAccelerometer(SensorEvent event, int index) {
            float[] values = event.values;
            // Movement
            float x = values[0];
            float y = values[1];
            float z = values[2];
            Log.d("activity_main", "================");
            Log.d("activity_main", "getAccelerometer: data " + String.valueOf(index));

            acc_x[index] = x;
            acc_y[index] = y;
            acc_z[index] = z;
            time[index] = System.currentTimeMillis();
        }

//        private void LetterSent(){
//            //接收1500的数据传输给服务器
//            //关闭传感器
//            //sensorManager.unregisterListener(listener);
//            //发送数据
//            Log.d("activity_main", "================");
//            Log.d("activity_main", "sending.........");
//            new Thread(){
//                @Override
//                public void run() {
//                    try {
//                        //创建Socket
//                        socket = new Socket("192.168.31.130", 9000); //IP
//                        //向服务器发送消息
//                        //String str = "test success!";
//                        PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
//                        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
//                        int i = 0;
//                        do {
//                            out.println(String.valueOf(time[i]));
//                            out.println(String.valueOf(acc_x[i]));
//                            out.println(String.valueOf(acc_y[i]));
//                            out.println(String.valueOf(acc_z[i]));
//                            i++;
//                        } while (i < index);
//                        //传输结束指令
//                        out.println("end");
//                        Log.d("activity_main", "================");
//                        Log.d("activity_main", String.valueOf(index));
//
//
//                        //接收结果
//                        String str = String.valueOf(in.readLine());
//                        //System.out.println("收到：" + str);
//                        Log.d("activity_main", "================");
//                        Log.d("activity_main", "reading " + str + ".........");
//                        letter = str;
//
//                        //关闭流
//                        out.close();
//                        in.close();
//
//
//                    } catch (Exception e) {
//                        // TODO: handle exception
//                        Log.e("client_test", e.toString());
//                    } finally {
//                        //关闭Socket
//                        try {
//                            if (socket != null) {
//                                socket.close();
//                                //FlagThread = false;
//                                Log.d("activity_main", "close socket.........");
//                            }
//                        } catch (Exception e) {
//
//                        }
//                    }
//                }
//            }.start();
//            Log.d("activity_main", "thread sent close.........");
//        }

        private void LetterReg(){
            //接收1500的数据传输给服务器
            //关闭传感器
            //sensorManager.unregisterListener(listener);
            //发送数据
            Log.d("activity_main", "================");
            Log.d("activity_main", "receiving.........");
            new Thread(){
                @Override
                public void run() {
                    try {
                        //创建Socket
                        socket = new Socket("192.168.31.130", 9000); //IP
                        //向服务器发送消息
                        //String str = "test success!";
                        PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
                        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                        int i = 0;
                        do {
                            out.println(String.valueOf(time[i]));
                            out.println(String.valueOf(acc_x[i]));
                            out.println(String.valueOf(acc_y[i]));
                            out.println(String.valueOf(acc_z[i]));
                            i++;
                        } while (i < index);
                        //传输结束指令
                        out.println("end");
                        Log.d("activity_main", "================");
                        Log.d("activity_main", String.valueOf(index));


                        //接收结果
                        String str = "";
                        while(str.equals("")){
                            str = String.valueOf(in.readLine());
                            Log.d("activity_main", "waiting...");
                        }
                        //System.out.println("收到：" + str);
                        Log.d("activity_main", "================");
                        Log.d("activity_main", "reading " + str + ".........");
                        letter = str;

                        //关闭流
                        out.close();
                        in.close();


                    } catch (Exception e) {
                        // TODO: handle exception
                        Log.e("client_test", e.toString());
                    } finally {
                        //关闭Socket
                        try {
                            if (socket != null) {
                                socket.close();
                                //FlagThread = false;
                                Log.d("activity_main", "close socket.........");
                            }
                        } catch (Exception e) {

                        }
                    }
                }
            }.start();
            Log.d("activity_main", "thread receive close.........");
        }


        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
        }
    };

        @Override
    protected void onResume() {
        super.onResume();
        // register this class as a listener for the orientation and
        // accelerometer sensor
        sensorManager.registerListener(listener, sensor, SensorManager.SENSOR_DELAY_FASTEST);
    }

    @Override
    protected void onPause() {
        // unregister listener
        super.onPause();
        sensorManager.unregisterListener(listener);
    }
}