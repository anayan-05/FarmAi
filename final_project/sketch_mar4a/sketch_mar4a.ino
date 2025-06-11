float generatePoisson(float mean) {
  float L = exp(-mean);
  float p = 1.0;
  int k = 0;
  do {
    k++;
    p *= random(1000) / 1000.0;
  } while (p > L);
  return (k - 1) * (mean / 5.0);  
}

struct Counts {
  int healthy = 0;
  int moderate = 0;
  int unhealthy = 0;
};

Counts counts;

bool hasBalancedData() {
  return counts.healthy >= 33 && counts.moderate >= 33 && counts.unhealthy >= 33;
}

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

void generateBalancedData() {
  int condition = random(3);  

  if (counts.healthy >= 33) condition = (condition == 0) ? random(1, 3) : condition;
  if (counts.moderate >= 33) condition = (condition == 1) ? (random(0, 2) == 0 ? 0 : 2) : condition;
  if (counts.unhealthy >= 33) condition = (condition == 2) ? random(2) : condition;

  float temp, humidity, moisture;

  if (condition == 0) {
    temp = constrain(25 + generatePoisson(2.0), 20, 30);
    humidity = constrain(35 + generatePoisson(5.0), 20, 50);
    moisture = constrain(450 + generatePoisson(50.0), 300, 600);
    counts.healthy++;
  } 
  else if (condition == 1) {
    if (random(2) == 0) {
      temp = constrain(17 + generatePoisson(3.0), 15, 19);
      humidity = constrain(17 + generatePoisson(3.0), 15, 19);
      moisture = constrain(250 + generatePoisson(40.0), 200, 290);
    } else {
      temp = constrain(33 + generatePoisson(3.0), 31, 35);
      humidity = constrain(53 + generatePoisson(3.0), 51, 55);
      moisture = constrain(750 + generatePoisson(40.0), 700, 790);
    }
    counts.moderate++;
  } 
  else {
    temp = constrain(10 + generatePoisson(10.0), 0, 14);
    humidity = constrain(10 + generatePoisson(10.0), 0, 14);
    moisture = constrain(100 + generatePoisson(100.0), 0, 199);
    counts.unhealthy++;
  }

  Serial.print(temp);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(moisture);
}

void loop() {
  if (!hasBalancedData()) {
    generateBalancedData();
    delay(1000);  
  }
}
