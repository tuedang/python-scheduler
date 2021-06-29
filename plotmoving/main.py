"""Top-level implementation of the plotmoving program."""

import argparse
import logging
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--src')
parser.add_argument('-d', '--dest')
parser.add_argument('-l', '--limit', default=-1, type=int)

EXT = 'pmoving'
SRC_STOP_EXTS = ['.' + EXT, '.tmp']
DEST_STOP_EXTS = ['.' + EXT]


def main():
    args = parser.parse_args()
    print('Move file from {} ---> {}'.format(args.src, args.dest))
    move_file(args.src, args.dest, args.limit)

    return 0


def move_file(source, destination, limit):
    stop_src = list_files(source, SRC_STOP_EXTS)
    if stop_src:
        print('1. Do not execute moving file, stop source extensions={}'.format(stop_src))
        return None

    dest_src = list_files(destination, DEST_STOP_EXTS)
    if stop_src:
        print('2. Do not execute moving file, stop target extensions={}'.format(dest_src))
        return None

    if limit > 0:
        num_plots_dest = len(list_files(destination, ['.plot']))
        if num_plots_dest >= limit:
            print('3. Do not execute moving file, excess limit plots')
            return None

    plot_files = Path(source).glob("*.plot")
    target_files = Path(destination).glob("*." + EXT)

    if len(list(target_files)):
        print('Moving file existing, stop!')
        return None

    pfiles = list(plot_files)
    if len(pfiles):
        plot = pfiles[0]
        print('Moving file: ' + plot.name)

        moving_plot = str(plot) + ".{}".format(EXT)
        logging.info('renaming')
        os.rename(plot, moving_plot)

        move_command_fastcopy = 'fastcopy /cmd=move /auto_close /open_window /bufsize=2048 /speed=autoslow {} /to={}'.format(
            moving_plot, destination)
        # os.system(move_command_fastcopy)
        copy_output = os.popen(move_command_fastcopy).read()

        fmoving_plot = Path(destination).joinpath(plot.name + ".{}".format(EXT))
        os.rename(fmoving_plot, str(fmoving_plot)[:-(len(EXT) + 1)])

        print('Moved file: {}/output: {}'.format(plot.name, copy_output))


def list_files(dir, extensions):
    return [f for f in os.listdir(dir) if os.path.splitext(f)[1] in extensions]


if __name__ == "__main__":
    main()
