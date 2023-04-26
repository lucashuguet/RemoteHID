#include "PluggableUSBHID.h"
#include "USBKeyboard.h"
#include <ArduinoBLE.h>
/* #include "usb_hid_keys.h" */

USBKeyboard Keyboard;

/* Keyboard.key_code_raw(KEY_A); */

BLEService nanoService("96cf60a1-ec3f-4eba-8974-e0bc1fae0cc3"); 
BLEByteCharacteristic KeyCharacteristic("b6bcb398-e8c6-4bb9-b38c-7d92387e37d2", BLERead | BLEWrite);
BLEByteCharacteristic ShiftCharacteristic("9625c08c-4c1a-4205-b0b3-eb0abd30e555", BLERead | BLEWrite);
BLEByteCharacteristic AltGrCharacteristic("617948dd-e606-4cda-bead-54f256e7e847", BLERead | BLEWrite);

void setup() {
  if (!BLE.begin()) {
    while (1);
  }

  BLE.setLocalName("Arduino Nano 33 BLE Sense");
  BLE.setAdvertisedService(nanoService);

  nanoService.addCharacteristic(KeyCharacteristic);
  nanoService.addCharacteristic(ShiftCharacteristic);
  nanoService.addCharacteristic(AltGrCharacteristic);

  BLE.addService(nanoService);

  KeyCharacteristic.writeValue(0);
  ShiftCharacteristic.writeValue(0);
  AltGrCharacteristic.writeValue(0);

  BLE.advertise();
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    while (central.connected()) {
			if (KeyCharacteristic.written()) {
				if (KeyCharacteristic.value()) {
					Keyboard.key_code_raw(KeyCharacteristic.value());
					KeyCharacteristic.writeValue(0);
				}
			} else if (ShiftCharacteristic.written()) {
				if (ShiftCharacteristic.value()) {
					Keyboard.key_code_raw(ShiftCharacteristic.value(), KEY_SHIFT);
					ShiftCharacteristic.writeValue(0);
				}
			} else if (AltGrCharacteristic.written()) {
				if (AltGrCharacteristic.value()) {
					Keyboard.key_code_raw(AltGrCharacteristic.value(), KEY_RALT);
					AltGrCharacteristic.writeValue(0);
				}
			}
		}
  }
}
