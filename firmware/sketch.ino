#include <Arduino.h>

// Edge-AI Mosquito Call Classifier
// Wokwi demonstration using synthetic test data.
// This is NOT a trained CNN or real microphone input.

const int ledPin = 2;
const float threshold = 0.65;

// Synthetic mosquito-likelihood scores.
// These are demonstration values, not model predictions.
float testScores[] = {0.12, 0.24, 0.81, 0.93, 0.31, 0.76};
const int testCount = sizeof(testScores) / sizeof(testScores[0]);

int currentSample = 0;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.println("================================");
  Serial.println("EDGE-AI MOSQUITO CLASSIFIER");
  Serial.println("ESP32 / Wokwi Simulation");
  Serial.println("Mode: SYNTHETIC TEST DATA");
  Serial.println("No microphone or CNN is connected");
  Serial.println("================================");
}

void loop() {
  float score = testScores[currentSample];
  bool mosquitoDetected = score >= threshold;

  Serial.print("Sample ");
  Serial.print(currentSample + 1);
  Serial.print(" | Synthetic score: ");
  Serial.print(score, 2);

  if (mosquitoDetected) {
    Serial.println(" | MOSQUITO DETECTED");
    digitalWrite(ledPin, HIGH);
  } else {
    Serial.println(" | BACKGROUND");
    digitalWrite(ledPin, LOW);
  }

  currentSample = (currentSample + 1) % testCount;
  delay(2000);
}
