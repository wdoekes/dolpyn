#!/usr/bin/env python3
"""
Convert signal.ir files from the Flipper Zero from "raw" data to "parsed/RC5"

This script was tailored for use with Marantz raw data, but it could be used
elsewhere as well.

Usage:

    ./rc5marantz_raw2parsed.py remote_control.ir

Output:

    <the same as input, but type: raw will be parsed>
"""
import sys
from warnings import warn

from dolpyn_ir_signals import RawIrSignal, Rc5MarantzIrSignal, IrFile


# Take SR-7000.ir from github.com/Lucaslhm/Flipper-IRDB:
with open(sys.argv[1]) as fp:
    just_wrote_comment = False

    for signal, source_lines in IrFile.parse(fp):
        if isinstance(signal, RawIrSignal):
            try:
                signal = Rc5MarantzIrSignal.from_raw(signal)
            except AssertionError as exc:
                # shrug.. lets skip this one
                warn('skipping parse errors in {!r}'.format(sys.argv[1]))
                signal = None
            else:
                # If this is a now unsupported signal, we'll return it to raw.
                if isinstance(signal, Rc5MarantzIrSignal):
                    signal = signal.as_raw()
                    # idempotent, from now on?
                    signal2 = Rc5MarantzIrSignal.from_raw(signal)
                    signal2 = signal2.as_raw()
                    assert signal.data == signal2.data

        if signal is None or isinstance(signal, Exception):
            sys.stdout.write(''.join(source_lines))
            just_wrote_comment = source_lines[-1].startswith('#')
        else:
            if signal.comment and not just_wrote_comment:
                sys.stdout.write('#\n')
            sys.stdout.write(str(signal) + '\n')
