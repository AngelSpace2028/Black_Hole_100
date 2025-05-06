import os
import time

class SimpleCompressionSystem:
    def __init__(self):
        self.last_byte = 0

    def _apply_delta_encoding(self, data):
        """Apply delta encoding to the input data."""
        return [(data[i] - data[i - 1]) & 0xFF if i > 0 else data[i] for i in range(len(data))]

    def _apply_rle(self, data):
        """Apply Run-Length Encoding (RLE) to the input data."""
        compressed = bytearray()
        i = 0
        while i < len(data):
            run_length = 1
            while i + run_length < len(data) and data[i] == data[i + run_length] and run_length < 255:
                run_length += 1
            compressed.append(data[i])
            compressed.append(run_length)
            i += run_length
        return compressed

    def compress(self, data, method):
        """Compress data using specified method (01: Delta + RLE, 02: RLE, 03: Delta)."""
        if method == '01':  # Delta + RLE
            delta_encoded = self._apply_delta_encoding(data)
            compressed = self._apply_rle(delta_encoded)
        elif method == '02':  # RLE only
            compressed = self._apply_rle(data)
        elif method == '03':  # Delta only
            compressed = self._apply_delta_encoding(data)
        else:
            raise ValueError("Invalid method. Use '01', '02', or '03'.")
        
        return bytes(compressed)

    def decompress(self, data, method):
        """Decompress data using the specified method."""
        if method == '01':  # Delta + RLE
            # Reverse RLE
            decompressed = bytearray()
            i = 0
            while i < len(data):
                byte = data[i]
                run_length = data[i + 1]
                decompressed.extend([byte] * run_length)
                i += 2

            # Reverse Delta Encoding
            for i in range(1, len(decompressed)):
                decompressed[i] = (decompressed[i] + decompressed[i - 1]) & 0xFF

        elif method == '02':  # RLE only
            # Reverse RLE
            decompressed = bytearray()
            i = 0
            while i < len(data):
                byte = data[i]
                run_length = data[i + 1]
                decompressed.extend([byte] * run_length)
                i += 2

        elif method == '03':  # Delta only
            # Reverse Delta Encoding
            decompressed = bytearray(data)
            for i in range(1, len(decompressed)):
                decompressed[i] = (decompressed[i] + decompressed[i - 1]) & 0xFF

        else:
            raise ValueError("Invalid method. Use '01', '02', or '03'.")
        
        return bytes(decompressed)

def benchmark(file_path, method):
    """Test compression on a file with the specified method."""
    compressor = SimpleCompressionSystem()
    
    with open(file_path, 'rb') as f:
        original = f.read()
    
    print(f"\nTesting {file_path} ({len(original):,} bytes)")
    
    # Compress the data
    compressed = compressor.compress(original, method)
    ratio = len(compressed) / len(original)
    print(f"Compressed: {len(compressed):,} bytes ({ratio:.1%})")

    # Decompress the data
    decompressed = compressor.decompress(compressed, method)
    print(f"Decompressed: {len(decompressed):,} bytes")

def main():
    print("Simple Compression System")
    print("Supports RLE and Delta Encoding")
    
    while True:
        print("\nMenu:")
        print("1. Compress file")
        print("2. Decompress file")
        print("3. Benchmark file")
        print("4. Exit")
        
        try:
            choice = input("Select: ").strip()
            
            if choice == "1":
                input_file = input("Input file: ").strip()
                if not os.path.exists(input_file):
                    print("File not found!")
                    continue
                
                output_file = input("Output file (.cmp): ").strip()
                if not output_file.endswith('.cmp'):
                    output_file += '.cmp'

                print("Select compression method:")
                print("01 - Delta + RLE")
                print("02 - RLE only")
                print("03 - Delta only")
                method = input("Choose method (01/02/03): ").strip()
                if method not in ['01', '02', '03']:
                    print("Invalid method selected.")
                    continue
                
                compressor = SimpleCompressionSystem()
                
                with open(input_file, 'rb') as f:
                    original = f.read()
                
                compressed = compressor.compress(original, method)
                
                with open(output_file, 'wb') as f:
                    f.write(compressed)
                
                print(f"Compressed {len(original):,} → {len(compressed):,} bytes ({len(compressed)/len(original):.1%})")
                
            elif choice == "2":
                input_file = input("Input file (.cmp): ").strip()
                if not input_file.endswith('.cmp'):
                    print("Must be a .cmp file!")
                    continue
                    
                output_file = input("Output file: ").strip()
                
                print("Select decompression method:")
                print("01 - Delta + RLE")
                print("02 - RLE only")
                print("03 - Delta only")
                method = input("Choose method (01/02/03): ").strip()
                if method not in ['01', '02', '03']:
                    print("Invalid method selected.")
                    continue
                
                compressor = SimpleCompressionSystem()
                
                with open(input_file, 'rb') as f:
                    compressed = f.read()
                
                decompressed = compressor.decompress(compressed, method)
                
                with open(output_file, 'wb') as f:
                    f.write(decompressed)
                
                print(f"Successfully decompressed {len(compressed):,} → {len(decompressed):,} bytes")
                
            elif choice == "3":
                file_to_test = input("File to benchmark: ").strip()
                if os.path.exists(file_to_test):
                    print("Select compression method:")
                    print("01 - Delta + RLE")
                    print("02 - RLE only")
                    print("03 - Delta only")
                    method = input("Choose method (01/02/03): ").strip()
                    if method not in ['01', '02', '03']:
                        print("Invalid method selected.")
                        continue
                    benchmark(file_to_test, method)
                else:
                    print("File not found!")
            
            elif choice == "4":
                break
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()