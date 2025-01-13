from objects import read_lammps_output as rd
import matplotlib.pyplot as plt

inDir = 'C:/Users/asmon/mol_dyn/research/Phenolic_Resin/TP_Reax/4k/H2O/pyro/rep1'
outDir = inDir + '/analysis/'
df = rd.read_o_file(inDir, outDir)

df = df.iloc[:291]

print(df.columns)
print(df.Step)
fig, ax1 = plt.subplots()
time = []
for step in df.Step:
    time.append(step * 0.1 / 1000)

finalCharYield = df.v_char_yield[df.v_char_yield.__len__() - 1]

ax1.plot(time, df.v_char_yield, color='black')
ax1.annotate('Char Yield', xy=(110, 89),
            font='Arial', color='black', rotation=325)
ax1.annotate(str(round(finalCharYield)) + '%', xy=(290.1, finalCharYield), xytext=(250, 70),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.00', color='k'),
            font='Arial', color='black',
            )
ax1.set_xlabel('Time (ps)')
ax1.set_ylabel('Char Yield (%)')
ax2 = ax1.twinx()

ax2.plot(time, df.v_ramp_temp, color='red')

ax2.spines['right'].set_color('red')
ax2.tick_params(axis='y', colors='red')
ax2.annotate('3200 K', xy=(290.2, 3200), xytext=(250, 3150),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.00', color='r'),
            font='Arial', color='red',
            )
ax2.annotate('Temp', xy=(95, 1335),
            font='Arial', color='red', rotation=45
            )
ax2.set_ylabel('Temperature (K)', color='red')
fig.tight_layout()
#plt.show()

plt.savefig(outDir + 'char_yield.png', dpi=300)

