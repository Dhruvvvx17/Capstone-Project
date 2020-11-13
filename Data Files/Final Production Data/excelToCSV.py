import os

sub_dir = input("Enter sub-directory name: ")
if not os.path.exists(sub_dir):
    print(f"Directory {sub_dir} does not exist.")
    print("0 files converted.\nExiting\n")


out_dir = input("Enter output directory name: ")
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    print(f"Directory {out_dir} Created.")
else:    
    print(f"Directory {out_dir} already exists.")


# List of files to convert
files = os.listdir(path=sub_dir)

count = 0
for file in files:
    file_path = f"{sub_dir}/{file}"
    cmd = f"soffice --invisible --convert-to csv {file_path} --outdir {out_dir}"
    os.system(cmd)
    count += 1

print(f"{count} files converted successfully.\nExiting\n")