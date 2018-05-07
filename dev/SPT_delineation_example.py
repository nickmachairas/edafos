import matplotlib.pyplot as plt

# page 24 from FHWA-NHI-16-064

depth = [1,6,11,16,21,26,31,36,41,46,51,56,61,66,71,76,81,86,91,96]
N = [4,4,6,6,8,13,15,11,15,18,40,39,41,43,41,44,45,48,46,47]

plt.figure(figsize=(4,6))
plt.scatter(N,depth)
plt.gca().invert_yaxis()
plt.title('Subsurface Exploration Results', weight='bold')
plt.xlabel('Field N Values')
plt.ylabel('Depth (ft)')
plt.grid()
plt.tight_layout()
plt.show()
