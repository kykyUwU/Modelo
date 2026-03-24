coords = []
with open('2AM9_clean.pdb', 'r') as f:
    for line in f:
        if line.startswith('ATOM'):
            coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])

x_coords, y_coords, z_coords = zip(*coords)
min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)
min_z, max_z = min(z_coords), max(z_coords)

center = [(min_x + max_x)/2, (min_y + max_y)/2, (min_z + max_z)/2]
size = [max_x - min_x + 5, max_y - min_y + 5, max_z - min_z + 5] # +5A de marge

print(f'center_x = {center[0]:.3f}')
print(f'center_y = {center[1]:.3f}')
print(f'center_z = {center[2]:.3f}')
print(f'size_x = {size[0]:.0f}')
print(f'size_y = {size[1]:.0f}')
print(f'size_z = {size[2]:.0f}')