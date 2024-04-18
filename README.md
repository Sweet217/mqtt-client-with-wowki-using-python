Wokwi code=
#include<DHT.h>
#include<WiFi.h>
#include <PubSubClient.h>

#define DHTPIN 13
#define DHTTYPE DHT22

const char* ssid="Wokwi-GUEST";
const char* password="";

const char* mqtt_broker = "broker.hivemq.com";
const char* mqtt_topic = "ucol/iot/gabriel";
const char* mqtt_client_id = "cliente_gabriel";

const char* mqtt_username = "gabriel";
const char* mqtt_password = "root";

const int mqtt_port = 1883;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

DHT dht(DHTPIN, DHTTYPE);

void reconnect(){
  while (!mqttClient.connected()) {
    Serial.println("Conectando con el broker MQTT...");

    if (mqttClient.connect(mqtt_client_id)) {
      Serial.println("Conectando al broker MQTT.");
    } else {
      Serial.print("Error: ");
      Serial.println(mqttClient.state());
      Serial.println("Reintentando en 5 segundos...");
      delay(5000);
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  dht.begin();

  Serial.println("Conectando a wi-fi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println(".");
  }

  Serial.print("Conectando con la IP:");
  Serial.println(WiFi.localIP());

  mqttClient.setServer(mqtt_broker, mqtt_port);
}

void loop() {
  if (!mqttClient.connected()) {
    reconnect();
  }
  mqttClient.loop();

  delay(5000);
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  Serial.printf("Temperatura %f C, humedad: %f %\n", t, h);

  char json[200];
  sprintf(json, "{\"temperature\": %f, \"humidity\": %f}", t, h);
  Serial.println(json);

  mqttClient.publish(mqtt_topic, json);
}


