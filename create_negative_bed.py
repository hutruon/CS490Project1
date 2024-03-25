import sys
import os

def create_negative_bed(bed_file, output_file):
    last_chrom = None
    last_end = 0

    with open(bed_file, 'r') as f, open(output_file, 'w') as out:
        for line in f:
            parts = line.strip().split()
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])

            if chrom == last_chrom and start > last_end:
                out.write(f"{last_chrom}\t{last_end}\t{start}\n")
            elif chrom != last_chrom:
                last_chrom = chrom
                last_end = 0

            last_end = max(last_end, end)

def process_all_bed_files(input_directory, output_directory):
    for file in os.listdir(input_directory):
        if file.endswith(".bed") and not file.startswith("negative_"):  # Avoid reprocessing already created negative files
            bed_file = os.path.join(input_directory, file)
            output_file = os.path.join(output_directory, f"negative_{file}")
            print(f"Processing {bed_file}...")
            create_negative_bed(bed_file, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_negative_bed.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # Create the output directory if it doesn't exist
    process_all_bed_files(input_directory, output_directory)
