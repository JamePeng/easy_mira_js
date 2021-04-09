import os.path
import struct

GOLDHEN_VERSION = 1.1
PLATFORM_VERSION = 755

exist_goldhen_payload = False

SUCCESS = 1
FAILED = 0

GOLDHEN_PAYLOAD = f"goldhen_{GOLDHEN_VERSION}_{PLATFORM_VERSION}.bin"

GOLDHEN_JS = f"goldhen_{PLATFORM_VERSION}.js"


# Return File Size
def getFileSize(path):
    fileSize = 0
    fileSize = os.path.getsize(path)
    return fileSize


# Generate mira-[version].js
def gen_payload_js(payload_path):
    try:
        payload_size = getFileSize(payload_path)
        print("payload_size: 0x%x" % payload_size)

        payload_elf = open(GOLDHEN_PAYLOAD, mode='rb')

        payload_js = open(GOLDHEN_JS, mode='w')
        payload_js.write(f"window.mira_blob_2_len = {hex(payload_size)};\n")
        payload_js.write("window.mira_blob_2 = malloc(window.mira_blob_2_len);\n")
        payload_js.write("write_mem(window.mira_blob_2, [")
        for index in range(payload_size - 1):
            data = payload_elf.read(1)
            number = struct.unpack("B", data)
            payload_js.write(str(number[0]))
            payload_js.write(',')
        data = payload_elf.read(1)
        number = struct.unpack("B", data)
        payload_js.write(str(number[0]))

        payload_js.write("]);")
    except:
        return FAILED

    payload_elf.close()
    payload_js.close()

    return SUCCESS


def startProcess(payload_path):
    print("Creating %s ..." % GOLDHEN_JS)

    if gen_payload_js(payload_path):
        print(f"{GOLDHEN_JS} was created succeed!")
    else:
        print(f"{GOLDHEN_JS} was created failed!")



print("Searching... %s" % GOLDHEN_PAYLOAD)
if os.path.exists(GOLDHEN_PAYLOAD):
    exist_goldhen_payload = True
    print("Found %s" % GOLDHEN_PAYLOAD)
else:
    print("%s file not found" % GOLDHEN_PAYLOAD)

if exist_goldhen_payload:
    print("Start Processing.....")
    startProcess(GOLDHEN_PAYLOAD)
else:
    print("Error: Could Not Found GOLDHEN_PAYLOAD")
