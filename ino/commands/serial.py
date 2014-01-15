# -*- coding: utf-8; -*-

import subprocess

from ino.commands.base import Command


class Serial(Command):
    """
    Open a serial monitor to communicate with the device.

    At the moment `picocom' is used as a program started by this command.
    Use Ctrl+A Ctrl+X to exit.
    """

    name = 'serial'
    help_line = "Open a serial monitor"

    def setup_arg_parser(self, parser):
        super(Serial, self).setup_arg_parser(parser)
        parser.add_argument('-p', '--serial-port', metavar='PORT',
                            help='Serial port to communicate with\nTry to guess if not specified')
        parser.add_argument('-b', '--baud-rate', metavar='RATE', type=int, default=9600,
                            help='Communication baud rate, should match value set in Serial.begin() on Arduino')
        parser.add_argument('remainder', nargs='*', metavar='ARGS',
                            help='Extra picocom args that are passed as is')

        parser.usage = "%(prog)s [-h] [-p PORT] [-b RATE] [-- ARGS]"

    def run(self, args):
        """
        Shtucer: 15.01.2014
        Do you have picocom?
        """
        serial_port = args.serial_port or self.e.guess_serial_port()
        try:
            serial_monitor = self.e.find_tool('serial', ['picocom'], human_name='Serial monitor (picocom)')
            subprocess.call([
                serial_monitor,
                serial_port,
                '-b', str(args.baud_rate),
                '-l'
            ] + args.remainder)
        except Exception:
            """
            Shtucer: 15.01.2014
            Who's care? We are have PySerial alredy
            Try subprocess serial.tools.miniterm
            looks ugly, but keyboard interrupt works fine

            Use Ctrl+] to exit
            """
            subprocess.call([
                'python',
                '-m', 'serial.tools.miniterm',
                serial_port,
                str(args.baud_rate),
            ] + args.remainder)
