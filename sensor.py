import psutil

def octetsvershumain(n):
    symboles = ('K', 'M', 'G', 'T', 'P')
    prefixe = {}
    for i, s in enumerate(symboles):
        prefixe[s] = 1 << (i + 1) * 10
    for s in reversed(symboles):
        if n >= prefixe[s]:
            value = float(n) / prefixe[s]
            return '%.1f%s' % (value, s)
    return "%so" % n

def cpu():
    stats=[]
    cpu_core_percent = psutil.cpu_percent(interval=2,percpu=True)

    for y in range(0,4):
        stats.append(cpu_core_percent[y])
    return stats

def mem():
    virtmem = psutil.virtual_memory()
    for name in virtmem._fields:
        value = getattr(virtmem, name)
        if name != 'percent':
            value = octetsvershumain(value)
        print('%-10s : %7s' % (name.capitalize(), value))
    print('')



def main():
    print("CPU -----------------")
    print(cpu())
    print("\nMEMORY --------------")
    mem()

main()
