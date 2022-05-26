package com.example.android_app_boat_project.utils;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import androidx.annotation.Nullable;

public class DatabaseUtils extends SQLiteOpenHelper {
    public DatabaseUtils(@Nullable Context context, @Nullable String name, @Nullable SQLiteDatabase.CursorFactory factory, int version) {
        super(context, name, factory, version);
    }

    /**
     * @Param sql
     * Truy vấn ko trả kết quả
     * CREATE, INSERT, UPDATE, DELETE
     * */
    public void QueryNotReturnData(String sql) {
        SQLiteDatabase database = getWritableDatabase();
        database.execSQL(sql);
    }

    /**
     * @Param sql
     * Chuỗi truy vân có trả kết quả (SELECT)
     * */
    public Cursor GetALlRecord(String sql) {
        SQLiteDatabase database = getReadableDatabase();
        return database.rawQuery(sql, null);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {

    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }
}
