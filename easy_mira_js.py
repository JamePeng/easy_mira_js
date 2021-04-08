import os.path
import struct

PLATFORM_VERSION = 755

exist_miraloader = False
exist_mirapayload = False

SUCCESS = 1
FAILED = 0

MIRA_LOADER = f"MiraLoader_Orbis_MIRA_PLATFORM_ORBIS_BSD_{PLATFORM_VERSION}.bin"
MIRA_PAYLOAD = f"Mira_Orbis_MIRA_PLATFORM_ORBIS_BSD_{PLATFORM_VERSION}.elf"

LOADER_JS = f"loader-{PLATFORM_VERSION}.js"
PAYLOAD_JS = f"mira-{PLATFORM_VERSION}.js"


# Return File Size
def getFileSize(path):
    fileSize = 0
    fileSize = os.path.getsize(path)
    return fileSize


# Generate loader-[version].js
def gen_loader_js(loader_path):
    try:
        loader_size = getFileSize(loader_path)
        print("loader_size: 0x%x" % loader_size)

        loader_bin = open(MIRA_LOADER, mode='rb')

        loaderjs = open(LOADER_JS, mode='w')
        loaderjs.write(f"window.mira_blob = malloc({hex(loader_size)});\n")
        loaderjs.write("write_mem(window.mira_blob, [")

        for index in range(loader_size - 1):
            data = loader_bin.read(1)
            number = struct.unpack("B", data)
            loaderjs.write(str(number[0]))
            loaderjs.write(',')
        data = loader_bin.read(1)
        number = struct.unpack("B", data)
        loaderjs.write(str(number[0]))
        loaderjs.write("]);")

    except:
        return FAILED

    loaderjs.close()
    loader_bin.close()

    return SUCCESS


# Generate mira-[version].js
def gen_payload_js(payload_path):
    try:
        payload_size = getFileSize(payload_path)
        print("payload_size: 0x%x" % payload_size)

        payload_elf = open(MIRA_PAYLOAD, mode='rb')

        payload_js = open(PAYLOAD_JS, mode='w')
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


def startProcess(loader_path, payload_path):
    print("Creating %s ..." % LOADER_JS)

    if gen_loader_js(loader_path):
        print(f"{LOADER_JS} was created succeed!")
    else:
        print(f"{LOADER_JS} was created failed!")

    print("Creating %s ..." % PAYLOAD_JS)

    if gen_payload_js(payload_path):
        print(f"{PAYLOAD_JS} was created succeed!")
    else:
        print(f"{PAYLOAD_JS} was created failed!")


print("Searching... %s" % MIRA_LOADER)

if os.path.exists(MIRA_LOADER):
    exist_miraloader = True
    print("Found %s" % MIRA_LOADER)
else:
    print("%s file not found" % MIRA_LOADER)

print("Searching... %s" % MIRA_PAYLOAD)
if os.path.exists(MIRA_PAYLOAD):
    exist_mirapayload = True
    print("Found %s" % MIRA_PAYLOAD)
else:
    print("%s file not found" % MIRA_PAYLOAD)

if exist_mirapayload and exist_miraloader:
    print("Start Processing.....")
    startProcess(MIRA_LOADER, MIRA_PAYLOAD)
else:
    print("Error: Could Not Found MIRA_LOADER or MIRA_PAYLOAD")
