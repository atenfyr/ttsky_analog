from os import listdir
from os.path import isfile, join

target_gmId = float(input("Enter target gm/Id: ").strip())
target_L = 0
target_transistor = input("Transistor (nfet/pfet): ").strip()
target_L = float(input("Size (in nm; 150/180/300/450): ").strip())

parent_path = "."
csv_files = [join(parent_path, f) for f in listdir(parent_path) if isfile(join(parent_path, f)) and target_transistor in f]

stats = {}
for csv_file in csv_files:
    with open(csv_file, 'r') as f:
        header = f.readline().strip().split(",")
        target_len = len(header)
        L_col = header.index('L')
        gm_Id_col = header.index('gm/Id')

        target_cols = list(header)
        target_cols.remove('gm/Id')
        target_cols.remove('L')

        closest_gm_Id = 99999
        closest_gm_Id_distance = 99999
        while line := f.readline():
            line_split = line.strip().split(",")
            if len(line_split) != target_len: continue

            this_L = float(line_split[L_col]) * 1e9
            if abs(this_L - target_L) > 10: continue

            this_gm_Id = float(line_split[gm_Id_col])
            this_distance = abs(target_gmId - this_gm_Id)
            if this_distance < closest_gm_Id_distance:
                closest_gm_Id_distance = this_distance
                closest_gm_Id = this_gm_Id
                for target_col in target_cols:
                    stats[target_col] = float(line_split[header.index(target_col)])

if "Vds_sat" in stats:
    stats["Vds_sat (pessimistic)"] = 1.5 * stats["Vds_sat"]

units = {"Ai": "V/V = gm*rds", "Id/W": "uA/um", "Vds_sat": "V", "Vds_sat (pessimistic)": "V", "Vgs": "V"}
print()
for stat, _ in sorted(stats.items()):
    print(f"{stat} = {stats[stat]:.3f} {units[stat] if stat in units else ""}")

