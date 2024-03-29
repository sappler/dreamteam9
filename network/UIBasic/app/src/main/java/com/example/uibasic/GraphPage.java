package com.example.uibasic;


import android.app.Activity;
import android.content.Context;
import android.content.Intent;

import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.jjoe64.graphview.DefaultLabelFormatter;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import static android.graphics.Color.WHITE;


public class GraphPage  extends Activity {
    private static final String TAG ="GraphPage";
    String startTime="";
    String endTime;
    TextView result;
    LineGraphSeries<DataPoint> series;
    LineGraphSeries<DataPoint> series2;

    Context mContext;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_graph_page);
        mContext=getApplicationContext();

        GraphView graph =(GraphView) findViewById(R.id.graph);
        //graph.setBackgroundColor(Color.WHITE);
        //graph.set

        //GraphView graph2 =(GraphView) findViewById(R.id.graph2);
        series = new LineGraphSeries<DataPoint>();
        series2 = new LineGraphSeries<DataPoint>();

        series.setThickness(4);
        series.setTitle("Stage");
        series2.setTitle("Movement");

        File outputDir = mContext.getCacheDir();
        String dataFile = outputDir + "/" + File.separator + "state_output.txt";
        String dataFile2 = outputDir + "/" + File.separator + "accel_output.txt";
        double x=0,y=0;
        String[] data= {"0","0"};
        String[] time;
        try {
            BufferedReader br = new BufferedReader(new FileReader(dataFile));
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
                data=line.split(";");
                if(data[0].equals("DEEP")) {
                    y=0;
                }else{
                    y=1;
                }
                time=data[1].split(":");
                x=Double.parseDouble(time[0])*60+Double.parseDouble(time[1]);
                if(startTime.equals("")){
                    startTime=data[1];
                }
                series.appendData(new DataPoint(x,y),true,500);
            }
            endTime=data[1];
            double d=Double.parseDouble(startTime.split(":")[0])*60+Double.parseDouble(startTime.split(":")[1]);
            setGraphProps(graph,d,x,1,2);
            graph.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
                @Override
                public String formatLabel(double value, boolean isValueX) {
                    if (isValueX) {
                        // show normal x values
                        double timeH=0;
                        double timeM;
                        timeM=value % 60;
                        if(value>timeM){
                            timeH=(value-timeM)/60;
                        }
                        if(timeM > 9) {
                            return super.formatLabel(timeH, isValueX) + ":" + super.formatLabel(timeM, isValueX);
                        }else{
                            return super.formatLabel(timeH, isValueX) + ":0" + super.formatLabel(timeM, isValueX);
                        }
                    } else {
                        // show currency for y values
                        return  (value == 0) ? "DEEP" : "LIGHT";
                    }
                }
            });
            graph.addSeries(series);
            Log.d(TAG, "graphed first");

            br=new BufferedReader(new FileReader(dataFile2));
            while ((line = br.readLine()) != null) {
                data=line.split(";");
                System.out.println(line);
                x=Double.parseDouble(data[0]);
                y=Double.parseDouble(data[1])-.7;
                series2.appendData(new DataPoint(d+x/60,y),true,3000);
            }
            Log.d(TAG, "wrote second");
            series2.setColor(Color.RED);

            //setGraphProps(graph2,d,((int)(x/60))+d,1.8,8);
            /*
            graph2.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
                @Override
                public String formatLabel(double value, boolean isValueX) {
                    if (isValueX) {
                        // show normal x values
                        double timeH=0;
                        double timeM=value%60;
                        if(value>timeM){
                            timeH=(value-timeM)/60;
                        }
                        if(timeM > 9) {
                            return super.formatLabel(timeH, isValueX) + ":" + super.formatLabel(timeM, isValueX);
                        }else{
                            return super.formatLabel(timeH, isValueX) + ":0" + super.formatLabel(timeM, isValueX);
                        }
                    } else {
                        // show currency for y values
                        return super.formatLabel(value, isValueX);
                    }
                }
            });

             */
            graph.addSeries(series2);
            Log.d(TAG, "graphed second");
        } catch (IOException e) {
            Toast.makeText(GraphPage.this,"No datafile to parse :(",Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }

        result=(TextView) findViewById(R.id.textViewRes);
        String disp;
        if(Double.parseDouble(startTime.split(":")[1]) <10){
            startTime=startTime.split(":")[0]+":0"+startTime.split(":")[1];
        }
        disp="Sleep start: "+startTime+". "+"Sleep end: "+endTime;
        result.setText(disp);
    }

    public void setGraphProps(GraphView graph, double xMin,double xMax, double yMax, int vertLabels){
        graph.getViewport().setMinX(xMin);
        graph.getViewport().setMaxX(xMax);
        graph.getViewport().setXAxisBoundsManual(true);
        graph.getViewport().setScalable(true);
        graph.getViewport().setMinY(0.0);
        graph.getViewport().setMaxY(yMax);

        graph.getViewport().setYAxisBoundsManual(true);
        graph.getViewport().setXAxisBoundsManual(true);
        graph.getGridLabelRenderer().setNumHorizontalLabels(5);
        graph.getGridLabelRenderer().setNumVerticalLabels(vertLabels);
    }

}