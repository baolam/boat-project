package com.example.android_app_boat_project.utils;

import android.app.IntentService;
import android.content.Intent;
import android.content.Context;
import android.util.Log;

import androidx.annotation.Nullable;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;

import io.socket.client.IO;
import io.socket.client.Manager;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;

/**
 * An {@link IntentService} subclass for handling asynchronous task requests in
 * a service on a separate handler thread.
 * <p>
 * <p>
 * TODO: Customize class - update intent actions, extra parameters and static
 * helper methods.
 */
public class SocketUtilService extends IntentService {
    public static final String ACTION_NEW_RECORD = "com.example.android_app_boat_project.utils.action.ACTION_NEW_RECORD";
    public static final String ACTION_INIT_SERVICE = "com.example.android_app_boat_project.utils.action.ACTION_INIT_SERVICE";
    public static final String ACTION_GET_LAT_LNG = "com.example.android_app_boat_project.utils.action.ACTION_GET_LAT_LNG";

    public static final String DATABASE_SENSOR_NAME = "sensor.sqlite";
    public static final String TABLE_SENSOR_NAME = "SensorRecord";

    public static final String PARAM_TIME_RECORD = "time";
    public static final String PARAM_TURBIDITY_RECORD = "turbidity";
    public static final String PARAM_DISSOLVED_SOLID_RECORD = "dissolved_solid";
    public static final String PARAM_SPEED_RECORD = "speed";
    public static final String PARAM_BATTERY_RECORD = "battery";
    public static final String PARAM_MOTOR_SPEED_RECORD = "motor_speed";

    public static DatabaseUtils sensor_database;
    public static Socket mSocket;

    public SocketUtilService() {
        super("SocketUtilService");
    }

    @Override
    protected void onHandleIntent(@Nullable Intent intent) {
        assert intent != null;
        if (intent.getAction().equals(SocketUtilService.ACTION_INIT_SERVICE)) {
            String server_address = intent.getStringExtra("server_address");
            try {
                intialize(server_address, getApplicationContext());
            } catch (URISyntaxException e) {
                e.printStackTrace();
            }
        }
    }

    public static void sendEvent(String evt, JSONObject d) {
        mSocket.emit(evt, d.toString());
    }
    public static void sendEventText(String evt, String d) {
        mSocket.emit(evt, d.toString());
    }

    private void intialize(String server_address, Context context) throws URISyntaxException {
        mSocket = IO.socket(URI.create(server_address + "/android"));

        mSocket.on(Socket.EVENT_CONNECT, new Emitter.Listener() {
            @Override
            public void call(Object... args) {
                Log.d("SOCKET", String.valueOf(mSocket.connected()));
            }
        });


        mSocket.on(Socket.EVENT_CONNECT_ERROR, new Emitter.Listener() {
            @Override
            public void call(Object... args) {
                for (Object arg : args) {
                    Log.d("SOCKET", arg.toString());
                }
            }
        });

        mSocket.on("record", onGetRecord);
        mSocket.on("gps", onGetGPS);

        mSocket.connect();

        sensor_database = new DatabaseUtils(context, DATABASE_SENSOR_NAME, null, 1);
        sensor_database.QueryNotReturnData("CREATE TABLE IF NOT EXISTS SensorRecord(" +
                "time VARCHAR(100) PRIMARY KEY, turbidity DOUBLE, dissolved_solid DOUBLE, speed DOUBLE, battery DOUBLE, motor_speed INTEGER)");
    }

    private Emitter.Listener onGetRecord = new Emitter.Listener() {
        @Override
        public void call(Object... args) {
            JSONObject rec = (JSONObject) args[0];
            //Log.d("GET_DATA", rec.toString());
            try {
                String time = rec.getString(PARAM_TIME_RECORD);
                Double turbidity = rec.getDouble(PARAM_TURBIDITY_RECORD);
                Double dissolved_solid = rec.getDouble(PARAM_DISSOLVED_SOLID_RECORD);
                Double speed = rec.getDouble(PARAM_SPEED_RECORD);
                Double battery = rec.getDouble(PARAM_BATTERY_RECORD);
                int motor_speed = rec.getInt(PARAM_MOTOR_SPEED_RECORD);

                Log.d("motor_speed", String.valueOf(motor_speed) + '%');

                // Send data to activity
                Intent boardcast_data = new Intent();
                boardcast_data.setAction(ACTION_NEW_RECORD);

                boardcast_data.putExtra(PARAM_TIME_RECORD, time);
                boardcast_data.putExtra(PARAM_TURBIDITY_RECORD, turbidity);
                boardcast_data.putExtra(PARAM_DISSOLVED_SOLID_RECORD, dissolved_solid);
                boardcast_data.putExtra(PARAM_SPEED_RECORD, speed);
                boardcast_data.putExtra(PARAM_BATTERY_RECORD, battery);
                boardcast_data.putExtra(PARAM_MOTOR_SPEED_RECORD, motor_speed);

                sendBroadcast(boardcast_data);

                // Write database (Overwrite --> Need fixing)
//                sensor_database.QueryNotReturnData("INSERT INTO " + TABLE_SENSOR_NAME + " VALUES(" +
//                        time + "," + turbidity.toString() + "," + dissolved_solid.toString() + "," + speed.toString() + "," + battery.toString() + ")");
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    };

    private Emitter.Listener onGetGPS = new Emitter.Listener() {
        @Override
        public void call(Object... args) {
            JSONObject rec = (JSONObject) args[0];

            try {
                Intent boardcast_data = new Intent();

                boardcast_data.setAction(ACTION_GET_LAT_LNG);
                boardcast_data.putExtra("lat", rec.getDouble("lat"));
                boardcast_data.putExtra("lng", rec.getDouble("lng"));

                sendBroadcast(boardcast_data);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    };
}