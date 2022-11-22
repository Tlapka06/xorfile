import hashlib, mmap, os, sys

### XOR FILE
## HEADER
# b"XOR1"
# md5 checksum (16b)
## DATA
# encrypted data
# 4 byte end integer


class XorFile():
    Signature = b"XOR1"
    SizeofMd5 = 16
    HeaderSize = len(Signature) + SizeofMd5

    def __init__(self, xorPath: str, mode: str, chunk = 1310720, progress=False):
        """Opens existing XOR file or creates new"""
        self.mode = mode
        self.chunk = chunk
        self.progress = progress
        
        if mode == "r":
            if os.path.getsize(xorPath) <= XorFile.HeaderSize:
                raise FileExistsError("File isn't a XOR file")
            
            self.file = open(xorPath, "rb")
            if self.file.read(len(XorFile.Signature)) != XorFile.Signature:
                raise FileExistsError("File isn't a XOR file")
            self.checksum = self.file.read(XorFile.SizeofMd5)
        elif mode == "w":
            self.file = open(xorPath, "w+b")
        elif mode == "x":
            self.file = open(xorPath, "xb")
        else:
            raise ValueError("mode must be r, x or w")
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
        
    def write(self, key: bytes, dataPath: str) -> None:
        if self.mode != "r":
            with open(dataPath, "rb") as data_f:
                with mmap.mmap(data_f.fileno(), length=0, access=mmap.ACCESS_READ) as data_map:
                    self.file.write(XorFile.Signature)
                    self.file.seek(XorFile.HeaderSize)
                    self.checksum = hashlib.md5()
                    counter = 0
                    while True:
                        buffer = data_f.read(self.chunk)
                        if not buffer:
                            break
                        self.checksum.update(buffer)
                        output_buffer = bytearray()
                        for i in range(len(buffer)):
                            output_buffer.append(buffer[i] ^ key[i % len(key)])
                        self.file.write(output_buffer)
                        counter += len(buffer)
                        if self.progress:
                            print(f"\r{counter} B", file=sys.stderr, end="")
                    self.file.seek(len(XorFile.Signature))
                    self.file.write(self.checksum.digest())
        else:
            raise PermissionError("File not opened for writing")
    
    def decrypt(self, key: bytes, savePath: str, overwrite = False) -> None:
        """Decrypt XOR file and saves its content to savePath"""
        if self.mode == "r":
            save_mode = "xb"
            if overwrite:
                save_mode = "w+b"
            with open(savePath, save_mode) as save_f:
                self.file.seek(XorFile.HeaderSize)
                new_checksum = hashlib.md5()
                counter = 0
                while True:
                    buffer = self.file.read(self.chunk)
                    if not buffer:
                        break
                    output_buffer = bytearray()
                    for i in range(len(buffer)):
                        output_buffer.append(buffer[i] ^ key[i % len(key)])
                    new_checksum.update(output_buffer)
                    save_f.write(output_buffer)
                    counter += len(buffer)
                    if self.progress:
                        print(f"\r{counter} B", file=sys.stderr, end="")
            if self.checksum != new_checksum.digest():
                os.unlink(savePath)
                raise RuntimeError("Checksum failed!")
        else:
           raise PermissionError("File not opened for reading") 

    def close(self):
        self.file.close()