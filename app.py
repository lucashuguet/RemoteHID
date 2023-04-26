import logging
import asyncio
import platform
import time
import ast

from bleak import BleakClient
from bleak import BleakScanner

from modules.hidparse import *

KEY_UUID = "b6bcb398-e8c6-4bb9-b38c-7d92387e37d2"
SHIFT_UUID = "9625c08c-4c1a-4205-b0b3-eb0abd30e555"
ALTGR_UUID = "617948dd-e606-4cda-bead-54f256e7e847"

ENTER_BYTE = bytearray([0x28])

SLEEP = 1

async def sendText(client, keymap):
    val = input("Enter some text:")
    time.sleep(SLEEP)

    for char in val:
        keys = getcompbytes(char, keymap)
        for key in keys:
            if key[0] == "None":
                await client.write_gatt_char(KEY_UUID, key[1])
            elif key[0] == "Shift":
                await client.write_gatt_char(SHIFT_UUID, key[1])
            elif key[0] == "AltGr":
                await client.write_gatt_char(ALTGR_UUID, key[1])


async def sendFunc(client, keymap):
    val = input("Enter the name of a function key: ")
    time.sleep(SLEEP)

    key = getfuncbytes(val, keymap)
    if key:
        await client.write_gatt_char(KEY_UUID, bytearray.fromhex(key[2:]))

        
async def returnEnter(client):
    time.sleep(SLEEP)

    await client.write_gatt_char(KEY_UUID, ENTER_BYTE)


async def run():
    print("Looking for Arduino Nano 33 BLE Sense Peripheral Device...")

    found = False
    devices = await BleakScanner.discover()
    for d in devices:       
        if "Arduino Nano 33 BLE Sense" in d.name:
            print("Found Arduino Nano 33 BLE Sense Peripheral")
            found = True

            keymap = input("keymap (azerty/qwerty): ")
            if keymap != "azerty" and keymap != "qwerty":
                print("this keymap isn't available")
                exit(1)

            async with BleakClient(d.address) as client:
                print(f"Connected to {d.address}")

                while True:
                    print("1 => send text")
                    print("2 => send function key")
                    print("3 => print function keys")
                    print("4 => exit")
                    print("_ => send enter")

                    r = input("=> ").strip()

                    if r == "1":
                        await sendText(client, keymap)
                    elif r == "2":
                        await sendFunc(client, keymap)
                    elif r == "3":
                        print(printFunc(keymap))
                    elif r == "4":
                        exit(0)
                    else:
                        await returnEnter(client)

    if not found:
        print("Could not find Arduino Nano 33 BLE Sense Peripheral")

                    
loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print("\nReceived Keyboard Interrupt")
finally:
    print("Program finished")
