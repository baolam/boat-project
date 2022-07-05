package com.example.android_app_boat_project.activity;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.SwitchCompat;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.ActivityManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;

import com.example.android_app_boat_project.R;
import com.example.android_app_boat_project.utils.SocketUtilService;
import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.google.android.material.snackbar.Snackbar;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;
import java.security.Permission;
import java.util.ArrayList;
import java.util.List;

import io.socket.client.IO;
import io.socket.client.Manager;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private static String SERVER_ADDRESS = "http://boat-project.herokuapp.com";

    private TextView tv_speed, tv_lat, tv_lng, tv_compass, tv_battery, tv_time, tv_motor_speed;
    private SwitchCompat swb_auto, swb_ctrl, swb_free;
    private SeekBar sb_set_speed;
    private ImageView iv_left, iv_right;
    private BarChart bc_water_information;

    private final GetResponseData recv = new GetResponseData();
    private class GetResponseData extends BroadcastReceiver {

        @Override
        public void onReceive(Context context, Intent intent) {
            if (intent.getAction().equals(SocketUtilService.ACTION_NEW_RECORD)) {
                runOnUiThread(new Runnable() {
                    @SuppressLint("SetTextI18n")
                    @Override
                    public void run() {
                        String time = intent.getStringExtra(SocketUtilService.PARAM_TIME_RECORD);
                        float turbidity = (float) intent.getDoubleExtra(SocketUtilService.PARAM_TURBIDITY_RECORD, 0);
                        float dissolved_solid = (float) intent.getDoubleExtra(SocketUtilService.PARAM_DISSOLVED_SOLID_RECORD, 0);
                        double speed = intent.getDoubleExtra(SocketUtilService.PARAM_SPEED_RECORD, 0);
                        double battery = intent.getDoubleExtra(SocketUtilService.PARAM_BATTERY_RECORD, 100);
                        Integer motor_speed = intent.getIntExtra(SocketUtilService.PARAM_MOTOR_SPEED_RECORD, 0);

                        tv_speed.setText(Double.toString(speed) + "km/h");
                        tv_battery.setText(Double.toString(battery) + '%');

                        tv_motor_speed.setText(motor_speed.toString() + '%');
                        if (motor_speed == 100) {
                            tv_motor_speed.setTextSize(20);
                        }

                        sb_set_speed.setProgress(motor_speed);
                        water_information_chart(dissolved_solid, turbidity);
                    }
                });
            }

            if (intent.getAction().equals(SocketUtilService.ACTION_GET_LAT_LNG)) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        double lat = intent.getDoubleExtra("lat", -1.0000);
                        double lng = intent.getDoubleExtra("lng", -1.0000);

//                        Log.d("GET_DATA", intent.getDataString());
                        runOnUiThread(new Runnable() {
                            @SuppressLint("SetTextI18n")
                            @Override
                            public void run() {
                                tv_lat.setText("Lat:" + lat);
                                tv_lng.setText("Lng:" + lng);
                            }
                        });
                    }
                });
            }
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tv_speed = findViewById(R.id.tv_speed);
        tv_lat = findViewById(R.id.tv_lat);
        tv_lng = findViewById(R.id.tv_lng);
        tv_compass = findViewById(R.id.tv_compass);
        tv_battery = findViewById(R.id.tv_battery);
        tv_time = findViewById(R.id.tv_time);
        tv_motor_speed = findViewById(R.id.tv_motor_speed);

        swb_auto = findViewById(R.id.swb_auto);
        swb_ctrl = findViewById(R.id.swb_ctrl);
        swb_free = findViewById(R.id.swb_free);

        sb_set_speed = findViewById(R.id.sb_set_speed);

        iv_left = findViewById(R.id.ib_left);
        iv_right = findViewById(R.id.ib_right);

        bc_water_information = findViewById(R.id.bc_water_information);
        bc_water_information.setNoDataText("Không có dữ liệu :>");

        setColor(swb_auto);
        setColor(swb_ctrl);
        setColor(swb_free);
        setClick();

        requestInternetPermission();

        if (! check_service_socket_running()) {
            Intent socket_service = new Intent(this, SocketUtilService.class);
            socket_service.putExtra("server_address", SERVER_ADDRESS);
            socket_service.setAction(SocketUtilService.ACTION_INIT_SERVICE);
            startService(socket_service);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        registerReceiver(recv, new IntentFilter(SocketUtilService.ACTION_NEW_RECORD));
        registerReceiver(recv, new IntentFilter(SocketUtilService.ACTION_GET_LAT_LNG));

        fillData();
    }

    @Override
    protected void onStop() {
        super.onStop();
        unregisterReceiver(recv);
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    private void requestInternetPermission() {
        List<String> permissions = new ArrayList<String>();
        int checkInternet = checkSelfPermission(Manifest.permission.INTERNET);
        if (checkInternet == PackageManager.PERMISSION_DENIED) {
            permissions.add(Manifest.permission.INTERNET);
        }
        if (! permissions.isEmpty()) {
            requestPermissions(permissions.toArray(new String[permissions.size()]), 2);
        }
    }

    @SuppressLint("NonConstantResourceId")
    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.swb_auto:
                try {
                    sendModeAuto();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                break;
            case R.id.swb_ctrl:
                try {
                    sendModeCtrl();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                break;
            case R.id.swb_free:
                try {
                    sendModeFree();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                break;
            case R.id.ib_left:
                sendLeftClick();
                break;
            case R.id.ib_right:
                sendRightClick();
                break;
        }
    }

    private boolean check_service_socket_running() {
        ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo servi : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (SocketUtilService.class.getName().equals(servi.service.getClassName()))
                return true;
        }
        return false;
    }

    private void fillData() {
        try {
            Cursor resp = SocketUtilService.sensor_database.GetALlRecord("SELECT * FROM " + SocketUtilService.TABLE_SENSOR_NAME);
        } catch (NullPointerException e) {
            e.printStackTrace();
        }
    }

    private void setClick() {
        swb_auto.setOnClickListener(this);
        swb_ctrl.setOnClickListener(this);
        swb_free.setOnClickListener(this);

        iv_left.setOnClickListener(this);
        iv_right.setOnClickListener(this);

        // -------------------------------
        sb_set_speed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            Integer current_progress = 0;

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                Log.d("progess", current_progress.toString());
                current_progress = progress;
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @SuppressLint("SetTextI18n")
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        tv_motor_speed.setText(current_progress.toString() + '%');
                    }
                });

                JSONObject req = new JSONObject();
                try {
                    req.put("speed", current_progress);
                    SocketUtilService.sendEvent("speed", req);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private ArrayList<BarEntry> values(int x, float vl) {
        ArrayList<BarEntry> k = new ArrayList<>();
        k.add(new BarEntry(x, vl));
        return k;
    }

    private void water_information_chart(float ntu_vl, float tds_vl) {
        BarDataSet ntu = new BarDataSet(values(1, ntu_vl), "NTU");
        BarDataSet tds = new BarDataSet(values(3, tds_vl), "TDS");

        ntu.setColor(Color.RED);
        tds.setColor(Color.YELLOW);

        ntu.setDrawValues(false);
        tds.setDrawValues(false);

        BarData barData = new BarData();
        barData.addDataSet(ntu);
        barData.addDataSet(tds);

        bc_water_information.setData(barData);
        bc_water_information.getDescription().setEnabled(false);
        bc_water_information.invalidate();
    }

    // SOCKET IO EVENT
    // ----------------------------------------------
    private void sendModeAuto() throws JSONException {
        JSONObject req = new JSONObject();
        req.put("auto", "");
        SocketUtilService.sendEvent("evt", req);
    }

    private void sendModeCtrl() throws JSONException {
        JSONObject req = new JSONObject();
        req.put("ctrl", "");
        SocketUtilService.sendEvent("evt", req);
    }

    private void sendModeFree() throws JSONException {
        JSONObject req = new JSONObject();
        req.put("free", "");
        SocketUtilService.sendEvent("evt", req);
    }

    private void sendLeftClick() {
        SocketUtilService.sendEventText("direction", "t");
    }

    private void sendRightClick() {
        SocketUtilService.sendEventText("direction", "f");
    }

    // ----------------------------------------------

    @SuppressLint("ResourceAsColor")
    private void setColor(SwitchCompat o) {
        if (o.isChecked()) {
            o.setTextColor(R.color.green);
        } else {
            o.setTextColor(R.color.black);
        }
    }
}