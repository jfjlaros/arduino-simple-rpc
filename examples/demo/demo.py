from sys import stdout

from simple_rpc import Interface


device = '/dev/ttyUSB0'
cycles = 20


stdout.write('Initialising... ')
stdout.flush()
interface = Interface(device)
stdout.write('done.\n\n')

i = 0
while i < 10:
    stdout.write('Ping: sent {}, received {}.\n'.format(i, interface.ping(i)))
    i = interface.inc(i)

stdout.write('\nStarting speed test ({} cycles) '.format(cycles))
stdout.flush()

start_time = interface.milli_time()
for _ in range(cycles):
    for i in range(256):
        interface.set_led(i)
    for i in range(256)[::-1]:
        interface.set_led(i)
    stdout.write('.')
    stdout.flush()

calls = 512 * cycles
duration = (interface.milli_time() - start_time) / 1000
stdout.write('\n{} calls in {:.02f} seconds ({} calls/sec)\n'.format(
    calls, duration, int(calls // duration)))
