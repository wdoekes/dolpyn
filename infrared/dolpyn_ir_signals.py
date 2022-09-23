#!/usr/bin/env python3
"""
dolpyn/infrared/ir_signals -- process Flipper Zero infrared files

Author: Walter Doekes, 2022
Useful info here: https://blog.flipperzero.one/infrared/
"""


class RawIrSignal:
    """
    Create a RAW infrared signal with a name, freq, duty_cycle and durations

    The data (durations) denote the signal and gap duration:
    [889, 1778] means 889us on and then 1778us OFF.

    The ON signal itself is a wave with the specified frequency and
    duty_cycle ON time.

    ___   ___   ___   ___
    | |   | |   | |   | |
    | |   | |   | |   | |
    | |___| |___| |___| |___________________________
    0     1     2     3     4     5     6     7

    For example, these three peaks shown could be a 33% duty_cycle over the
    course of 4 time units.

    A receiver will pick up these signals and record 4 time units as ON
    and 4 time units as OFF. From there on, it will be processed into bits.

    The flipper signal file might look like this:

        name: Power
        type: raw
        frequency: 36000
        duty_cycle: 0.25
        data: 889 889 1778 1778 1778 889 889 889 ... 889 889 90664

    This particular example uses manchester encoding:
    - where OFF-ON means 1 and ON-OFF means 0;
    - all semi-bits have the same duration (889us in this case);
    - this first 889 means ON, so it will be read as the *second* half
      bit of OFF-ON;
    - so, for the first 4 numbers, we get:
      OFF-(889)ON (889)OFF-(1778)ON ON-(1778)-OFF OFF-..;
    - that translates to: 1 1 0.
    """
    def __init__(self, name, frequency, duty_cycle, data, comment=''):
        assert 10000 <= frequency <= 56000, frequency
        assert 0.0 <= duty_cycle <= 1.0, duty_cycle
        self.name = name
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.data = data
        self.comment = comment

    def __str__(self):
        data = ' '.join(str(i) for i in self.data)
        buf = ['#']
        if self.comment:
            buf.append(f'# {self.name} {self.comment}')
        buf.extend([
            f'name: {self.name}',
            'type: raw',
            f'frequency: {self.frequency}',
            f'duty_cycle: {self.duty_cycle:.2f}',
            f'data: {data}',
        ])
        return '\n'.join(buf)


class Rc5IrSignal:
    """
    Create an RC-5 infrared signal with a name, an address and a command

    The flipper signal file might look like this:

        name: Power
        type: parsed
        protocol: RC5
        address: 10 00 00 00
        command: 0C 00 00 00

    Where for the RC5 protocol, the address must be in 0x00..0x3F and
    command must be in 0x00..0x7F.

    Description here: https://en.wikipedia.org/wiki/RC-5
    """
    REPEAT_DURATION = 113778    # 4096*36kHz: 113777.8us
    HALF_BIT_DURATION = 889     # 32*36kHz: 888.9us

    protocol = 'RC5'

    @classmethod
    def from_raw(cls, raw_ir_signal):
        bitstream = cls._durations_to_bitstream(
            raw_ir_signal.data, cls.HALF_BIT_DURATION)

        half_bits_28, rest = bitstream[0:28], bitstream[28:]
        assert sum(rest) == 0 and len(rest) == 101, (len(rest), rest)

        numeric = cls._manchester_decode(half_bits_28)
        return cls.from_numeric(raw_ir_signal.name, numeric)

    @classmethod
    def from_numeric(cls, name, numeric):
        assert numeric & 0x2000, bin(numeric)
        first_press = numeric & 0x800
        del first_press  # unused
        address = (numeric & 0x7C0) >> 6
        command = (((numeric & 0x1000) >> 6) ^ 0x40) | numeric & 0x3F
        return cls(
            name, address, command, comment=cls._numeric_to_comment(numeric))

    def __init__(self, name, address, command, comment=''):
        assert 0x00 <= address < 0x20, address
        assert 0x00 <= command < 0x80, command
        self.name = name        # Power
        self.address = address  # 0x10
        self.command = command  # 0x0C
        self.comment = comment

    def as_comment(self):
        numeric = self.to_numeric()
        assert numeric < 0x4000, hex(numeric)
        b = bin(numeric)[2:]
        return f'[{self.address} {self.command}] {{{b[0:3]}-{b[3:8]}-{b[8:]}}}'

    def as_raw(self):
        return RawIrSignal(
            self.name + '-raw',
            36000,  # 36kHz
            0.25,   # 25% on, when on: ^___^___^___^___
            self._make_durations(),
            comment=self.as_comment(),
        )

    def to_numeric(self):
        assert self.protocol == 'RC5', self.protocol
        numeric = (
            # SCFAAAAACCCCCC
            # edcba987654321 (14-numeric)
            0b10000000000000 |  # start
            (0b1000000000000 if self.command < 0x40 else 0) |
            (0b0100000000000 if False else 0) |  # first press
            self.address << 6 |
            self.command & 0x3F)
        return numeric

    def _make_durations(self):
        numeric = self.to_numeric()

        manchester = self._manchester_encoded(numeric)
        if not manchester[0]:
            manchester.pop(0)  # data must start with ON signal
        assert manchester[0], (numeric, manchester)
        if not manchester[-1]:
            manchester.pop()  # data must end with ON signal

        ret = self._manchester_to_durations(manchester, self.HALF_BIT_DURATION)

        # Add OFF time to fill up the repeat duration
        assert len(ret) % 2 == 1, (len(ret), ret)
        ret.append(self.REPEAT_DURATION - sum(ret))

        return ret

    @staticmethod
    def _numeric_to_comment(numeric):
        # Represent 0x1234 into {10010001-10100}
        b = bin(numeric)[2:]
        comment = '[raw] {{{}}}'.format(
            '-'.join(b[i:i+8] for i in range(0, len(b), 8)))
        return comment

    @staticmethod
    def _durations_to_bitstream(durations, half_bit_duration):
        half_half_bit_duration = half_bit_duration // 2
        bitstream = [0]  # assume [0, 1] start when manchester encoded
        cur = 1
        for idx, duration in enumerate(durations):
            count = (duration + half_half_bit_duration) // half_bit_duration
            assert count != 0, (count, duration, durations)
            bitstream.extend([cur] * count)
            cur ^= 1
        return bitstream

    @staticmethod
    def _manchester_decode(bitstream):
        numeric = 0
        for code in zip(bitstream[0::2], bitstream[1::2]):
            numeric <<= 1
            assert code in ((0, 1), (1, 0)), (code, bitstream)
            if code == (0, 1):
                numeric |= 1
        return numeric

    @staticmethod
    def _manchester_encoded(numeric):
        bitstream = []
        while numeric:
            bitstream.extend([1, 0] if numeric & 0x1 else [0, 1])  # reversed!
            numeric >>= 1
        bitstream.reverse()  # because we reverse it here
        return bitstream

    def _manchester_to_durations(self, manchester, half_bit_duration):
        assert self.protocol == 'RC5', self.protocol
        ret = [half_bit_duration]  # ON
        last = 1
        for idx, value in enumerate(manchester[1:]):
            if value == last:
                ret[-1] += self.HALF_BIT_DURATION
            else:
                ret.append(self.HALF_BIT_DURATION)
                last = value
        return ret

    def __str__(self):
        assert self.protocol == 'RC5', self.protocol
        buf = ['#']
        if self.comment:
            buf.append(f'# {self.name} {self.comment}')
        buf.extend([
            f'name: {self.name}',
            'type: parsed',
            f'protocol: {self.protocol}',
            f'address: {self.address:02X} 00 00 00',
            f'command: {self.command:02X} 00 00 00',
        ])
        return '\n'.join(buf)


class Rc5MarantzIrSignal(Rc5IrSignal):
    """
    Create an RC-5 infrared signal with a name, an address and a command

    The flipper signal file might look like this:

        # BEWARE: As of 2022-09, this is NOT recognised by the Flipper Zero
        name: Power
        type: parsed
        protocol: RC5marantz
        address: 10 00 00 00
        command: 0C 00 00 00

    Where for the RC5 protocol, the address must be in 0x00..0x3F and
    command must be in 0x00..0x7F. For the Marantz extension the
    extension code must be in 0x00..0x3F.

    The Marantz extension to RC5 consists of:
    - instead of 14 consecutive bits;
    - after the first 8 bits, there is a 2 bit duration gap (which would
      be invalid manchester encoding);
    - after that, there are the (last) 6 command bits;
    - and then 6 extension bits.

    Because the Flipper Zero does not grok this format, one can convert
    it to a RawIrSignal, which *can* be read.

    Example:

        Rc5MarantzIrSignal('Direct volume 50%', 0x10, 0x6F, 0x20).as_raw()
    """
    protocol = 'RC5marantz'

    @classmethod
    def from_raw(cls, raw_ir_signal):
        "Allow both RC5marantz and RC5 signals to be picked up here"
        bitstream = cls._durations_to_bitstream(
            raw_ir_signal.data, cls.HALF_BIT_DURATION)

        if bitstream[16:20] == [0, 0, 0, 0]:
            half_bits_16, half_bits_24, rest = (
                bitstream[0:16], bitstream[20:44], bitstream[44:])
            assert sum(rest) == 0 and len(rest) == 85, (len(rest), rest)
            numeric = (
                cls._manchester_decode(half_bits_16) << 12 |
                cls._manchester_decode(half_bits_24))
            return cls.from_numeric(raw_ir_signal.name, numeric)
        else:
            half_bits_28, rest = bitstream[0:28], bitstream[28:]
            assert sum(rest) == 0 and len(rest) == 101, (len(rest), rest)
            numeric = cls._manchester_decode(half_bits_28)
            return Rc5IrSignal.from_numeric(raw_ir_signal.name, numeric)

    @classmethod
    def from_numeric(cls, name, numeric):
        assert numeric & 0x80000, bin(numeric)
        first_press = numeric & 0x20000
        del first_press  # unused
        address = (numeric & 0x1F000) >> 12
        command = (
            (((numeric & 0x40000) >> 6) ^ 0x1000) | numeric & 0xFC0) >> 6
        ext = numeric & 0x3F
        return cls(
            name, address, command, ext,
            comment=cls._numeric_to_comment(numeric))

    def __init__(self, name, address, command, ext, comment=''):
        super().__init__(name, address, command, comment)
        assert 0x00 <= ext < 0x40, ext
        self.ext = ext

    def as_comment(self):
        numeric = self.to_numeric()
        assert numeric < 0x100000, hex(numeric)
        b = bin(numeric)[2:]
        return (
            f'[{self.address} {self.command} {self.ext}] '
            f'{{{b[0:3]}-{b[3:8]}--{b[8:14]}-{b[14:]}}}')

    def to_numeric(self):
        assert self.protocol == 'RC5marantz', self.protocol
        numeric = (
            # SCFAAAAACCCCCCEEEEEE (with two wait bits afte bit 8)
            # 43210fedcba987654321 (20-bits)
            0b10000000000000000000 |  # start
            (0b1000000000000000000 if self.command < 0x40 else 0) |
            (0b0100000000000000000 if False else 0) |  # first press
            self.address << 12 |
            (self.command & 0x3F) << 6 |
            self.ext)
        return numeric

    def _manchester_to_durations(self, manchester, half_bit_duration):
        assert self.protocol == 'RC5marantz', self.protocol
        ret = [half_bit_duration]  # ON
        last = 1
        for idx, value in enumerate(manchester[1:]):
            # For RC5marantz we add 4 half bits of silence after half-bit 16.
            if idx == 15:
                if last == 0:
                    ret[-1] += 4 * self.HALF_BIT_DURATION
                else:
                    ret.append(4 * self.HALF_BIT_DURATION)
                    last = 0

            # Add to existing value if same or add new value if different.
            if value == last:
                ret[-1] += self.HALF_BIT_DURATION
            else:
                ret.append(self.HALF_BIT_DURATION)
                last = value

        return ret

    def __str__(self):
        assert self.protocol == 'RC5marantz', self.protocol
        buf = ['#']
        if self.comment:
            buf.append(f'# {self.name} {self.comment}')
        buf.extend([
            f'name: {self.name}',
            'type: parsed',
            f'protocol: {self.protocol}',
            f'address: {self.address:02X} 00 00 00',
            f'command: {self.command:02X} {self.ext:02X} 00 00',
        ])
        return '\n'.join(buf)


if __name__ == '__main__':
    print('Filetype: IR signals file\nVersion: 1')

    # Example:
    # - take this raw RC5marantz signal
    auto1raw = RawIrSignal('AUTO/1', 36000, 0.25, [
        888, 888, 1803, 1803, 1803, 888, 888, 888, 888, 888, 888, 5354,
        1803, 888, 888, 1803, 1803, 1803, 888, 888, 1803, 1803, 888,
        888, 1803, 1803, 888, 75573])
    # name: AUTO/1
    # type: raw
    # frequency: 36000
    # duty_cycle: 0.25
    # data: 888 888 1803 1803 1803 888 888 888 888 888 888 5354 1803 ...
    print(auto1raw)

    # - decode it
    auto1decoded = Rc5MarantzIrSignal.from_raw(auto1raw)
    # name: AUTO/1
    # type: parsed
    # protocol: RC5marantz
    # address: 10 00 00 00
    # command: 25 2D 00 00
    print(auto1decoded)

    # - turn it back into a raw signal, because the Flipper does not do
    #   protocol RC5marantz
    auto1clean = auto1decoded.as_raw()
    # name: AUTO/1-raw
    # type: raw
    # frequency: 36000
    # duty_cycle: 0.25
    # data: 889 889 1778 1778 1778 889 889 889 889 889 889 5334 1778 ...
    print(auto1clean)