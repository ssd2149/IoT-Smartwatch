package h.iot;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Iterator;

import javax.net.ssl.HttpsURLConnection;

public class MainActivity extends AppCompatActivity {


    protected static final int RESULT_SPEECH = 1;

    private ImageButton btnSpeak;
    private TextView txtText;
    private Button btnHTTP;
    String STT_output = new String();
    String respmsg = new String();
    int responseCode2;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        txtText = (TextView) findViewById(R.id.txtText);
        btnSpeak = (ImageButton) findViewById(R.id.btnSpeak);
        btnHTTP = (Button) findViewById(R.id.btnHTTP);
/////////////////STT part
        btnSpeak.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                Intent intent = new Intent(
                        RecognizerIntent.ACTION_RECOGNIZE_SPEECH);

                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, "en-US");

                try {
                    startActivityForResult(intent, RESULT_SPEECH);
                    txtText.setText("");
                } catch (ActivityNotFoundException a) {
                    Toast t = Toast.makeText(getApplicationContext(),
                            "Oops! Your device doesn't support Speech to Text",
                            Toast.LENGTH_SHORT);
                    t.show();
                }
            }
        });



        //new SendPostRequest().execute();

        View.OnClickListener oclbtnHTTP = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Change text of TextView (tvOut)
                new SendPostRequest().execute();
                txtText.setText("HTTP Button Pressed");
            }
        };

        btnHTTP.setOnClickListener(oclbtnHTTP);







        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }

//////HTTP Thread
    public class SendPostRequest extends AsyncTask<String, Void, String> {

        protected void onPreExecute(){}

        protected String doInBackground(String... arg0) {

            try{
                URL url = new URL("http://209.2.232.94");
                //URL url = new URL("http://d5f932f4.ngrok.io");
                JSONObject postDataParams = new JSONObject();

                if(STT_output.compareTo("display time")==0)
                {
                    postDataParams.put("DisplayTime", "email");
                }

                else if(STT_output.compareTo("display on")==0)
                {
                    postDataParams.put("DisplayON", "email");
                }

                else if(STT_output.compareTo("display off")==0)
                {
                    postDataParams.put("DisplayOFF", "email");
                }

                else if(STT_output.indexOf("display message")!=-1)
                {
                    String delimeter = "display message ";
                    String STT_output2;
                    STT_output2=STT_output.split(delimeter)[1];
                    postDataParams.put("message", STT_output2.toUpperCase());
                }

                else
                {
                    postDataParams.put("email", "nothing worthwhile");
                }


                //postDataParams.put("message", STT_output);
                //postDataParams.put("count", "3");
                //postDataParams.put(str345,"email1");
                //postDataParams.put("email1",STT_output);
                Log.e("params",postDataParams.toString());


                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setReadTimeout(3000 /* milliseconds */);
                conn.setConnectTimeout(3000 /* milliseconds */);
                conn.setRequestMethod("POST");
                conn.setDoInput(true);
                conn.setDoOutput(true);
                OutputStream os = conn.getOutputStream();
                BufferedWriter writer = new BufferedWriter(
                        new OutputStreamWriter(os, "UTF-8"));
                writer.write(getPostDataString(postDataParams));

                writer.flush();
                writer.close();
                os.close();

                respmsg = conn.getResponseMessage();
                //clen=conn.getContentLength();

                int responseCode=conn.getResponseCode();
                responseCode2=responseCode;

                if (responseCode == HttpsURLConnection.HTTP_OK) {

                    BufferedReader in=new BufferedReader(new
                            InputStreamReader(
                            conn.getInputStream()));

                    BufferedReader er=new BufferedReader(new
                            InputStreamReader(
                            conn.getErrorStream()));

                    StringBuffer sb = new StringBuffer("");
                    String line="";
                    StringBuffer sb2 = new StringBuffer("");
                    String line2="";

                    while((line = in.readLine()) != null) {

                        sb.append(line);
                        break;
                    }


                    while((line = er.readLine()) != null) {

                    sb2.append(line);
                    break;
                    }



                    in.close();
                    er.close();
                    return sb.toString();
                    //return sb2.toString();
                    //return respmsg;

                }
                else {
                    return new String("false : "+responseCode);
                }

            }
            catch(Exception e){
                return new String("Exception: " + e.getMessage());
            }

        }

        @Override
        protected void onPostExecute(String result) {

           // Toast.makeText(getApplicationContext(), result,
            //        Toast.LENGTH_LONG).show();
            //txtText.setText(Integer.toString(responseCode2));
            //txtText.setText(Integer.toString(clen));
            //if(result==null) {
            //txtText.setText(result);
            //}
            txtText.setText(respmsg);
        }


        public String getPostDataString(JSONObject params) throws Exception {

            StringBuilder result = new StringBuilder();
            boolean first = true;

            Iterator<String> itr = params.keys();

            while(itr.hasNext()){

                String key= itr.next();
                Object value = params.get(key);

                if (first)
                    first = false;
                else
                    result.append("&");

                result.append(URLEncoder.encode(key, "UTF-8"));
                result.append("=");
                result.append(URLEncoder.encode(value.toString(), "UTF-8"));

            }
            return result.toString();
        }

    }








    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

//////////String part
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode) {
            case RESULT_SPEECH: {
                if (resultCode == RESULT_OK && null != data) {

                    ArrayList<String> text = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                    STT_output=text.get(0);
                    txtText.setText(STT_output);
                }
                break;
            }

        }
    }



}
