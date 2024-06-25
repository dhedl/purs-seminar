#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Keypad.h>

const char* ssid = "osciloskop";
const char* password = "osciloskop23";

const byte ROW_NUM = 4; 
const byte COLUMN_NUM = 4; 

char keys[ROW_NUM][COLUMN_NUM] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte pin_rows[ROW_NUM] = {13, 12, 14, 27}; 
byte pin_column[COLUMN_NUM] = {26, 25, 33, 32}; 

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM);

#define GREEN_LED 23
#define RED_LED 22

HTTPClient http;

void setup() {
  Serial.begin(9600); 
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");

  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  digitalWrite(GREEN_LED, LOW); 
  digitalWrite(RED_LED, LOW); 
}

void provjeriSifru(String sifra) {
  if (WiFi.status() == WL_CONNECTED) {
    
    http.begin("http://192.168.8.100/provjera_sifre"); 
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["sifra"] = sifra;

    String unesenaSifra;
    serializeJson(doc, unesenaSifra);
    Serial.println(unesenaSifra);

    int httpResponseCode = http.POST(unesenaSifra);

    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(response);

      StaticJsonDocument<200> responseDoc;
      deserializeJson(responseDoc, response);

      bool ormaric_sifra = responseDoc["ormaric_sifra"];

      if (ormaric_sifra) {
        Serial.println("Ormarić otvoren");
        digitalWrite(GREEN_LED, HIGH);
        delay(10000);
        digitalWrite(GREEN_LED, LOW);
      } else {
        Serial.println("Pristup odbijen. Nepostojeća šifra!");
        digitalWrite(RED_LED, HIGH);
        delay(5000);
        digitalWrite(RED_LED, LOW);
      }
    } else {
      Serial.print("Greška httpResponseCode: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}

void loop() {
  static String unos_sifre = "";

  char key = keypad.getKey();

  if (key) {
    Serial.print("Unos znaka: ");
    Serial.println(key);

    unos_sifre += key;

    if (unos_sifre.length() == 4) {
      Serial.print("Unesena šifra: ");
      Serial.println(unos_sifre);
      provjeriSifru(unos_sifre);
      unos_sifre = ""; 
    }
  }
}
