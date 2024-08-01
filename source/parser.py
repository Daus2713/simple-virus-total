import argparse
import os

from source.scan import start_url


def write_temp(text):
    with open('saved/.temp/target_url.txt', 'w') as file:
        file.write(text)


def show_saved_output():
    # Specify the directory
    directory = 'saved'

    # List all files in the specified directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Display the file names
    for file_name in files:
        print(file_name)


args_error = None


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        global args_error
        # Custom error message
        print(f'Error: {message}')
        args_error = True
        # Display help message and exit
        return


def parse_url(command, flag=None):
    # Split the command into arguments
    args_list = command.split()

    parser = CustomArgumentParser(description="URL parser")

    # Define arguments
    group_scan = parser.add_mutually_exclusive_group()
    if flag:
        group_scan.add_argument('-s', '--scan', nargs='*', metavar='[Target URL]', type=str, help='Scan Target URL')
    else:
        group_scan.add_argument('-s', '--scan', metavar='[Target URL]', type=str, help='Scan Target URL')
    # group_scan.add_argument('-sl', '--select', metavar='[Target URL]', type=str, help='Select and Analyse URL w/o display result')
    # Exclusive argument
    group_scan.add_argument('-do', '--display-output', action='store_true', help='Display saved output')

    group_options = parser.add_mutually_exclusive_group()
    group_options.add_argument('-c', '--category', nargs="*", metavar='Result Category[S,AV]', type=str,
                               help='Display only category(Information, Statistics and AntiVirus')
    group_options.add_argument('-AV', '--antivirus', nargs="*", metavar='[AV name]', type=str,
                               help='Display AV with selected name')
    group_options.add_argument('-AVm', '--avmethod', nargs="*", metavar='[string]', type=str,
                               help='Search AV with selected methods')
    group_options.add_argument('-AVe', '--avengine', nargs="*", metavar='[string]', type=str,
                               help='Search AV with selected engine name')
    group_options.add_argument('-AVc', '--avcategory', nargs="*", metavar='[string]', type=str,
                               help='Search AV with selected result category')
    group_options.add_argument('-AVr', '--avresult', nargs="*", metavar='[string]', type=str,
                               help='Search AV with selected result')

    parser.add_argument('-o', '--output', metavar='[output_name]', type=str,
                        help='Save output to /saved/[output_name]')

    # Parse arguments from the given command list
    # args = parser.parse_args(args_list)
    try:
        global args_error
        args_error = False
        # Parse arguments from the given command list
        args = parser.parse_args(args_list)
        mode = []
        keylist = []
        output_name = ""

        # not args.scan and not args.select and not args.display_output
        if not args.scan and not args.display_output:
            print("Valid command should have -s/-sl with values OR only -do")

        elif not args_error:
            if len(args_list) == 1 and args.display_output:
                show_saved_output()
                return

            elif args.scan:
                mode.append("scan")
                if flag:
                    mode.append("file")
                    args.scan = ' '.join(args.scan)
                if args.category:
                    print("nscan with category")
                    mode.append("category")
                    keylist = args.category
                    if "AV" in keylist:
                        mode.append("av")

                elif args.antivirus:
                    print("nscan with av")
                    mode.extend(["antivirus", "av"])
                    keylist = args.antivirus
                    print(keylist)
                elif args.avmethod:
                    print("avm")
                    mode.extend(["avmethod", "av"])
                    keylist = args.avmethod
                elif args.avcategory:
                    print("avc")
                    mode.extend(["avcategory", "av"])
                    keylist = args.avcategory
                elif args.avengine:
                    print("aveg")
                    mode.extend(["avengine", "av"])
                    keylist = args.avengine
                elif args.avresult:
                    print("avr")
                    mode.extend(["avresult", "av"])
                    keylist = args.avresult
                else:
                    mode.append("all")

            if args.output:
                print("and save output")
                output_name = args.output
                mode.append("output")
            else:
                mode.append("normal")
            print(mode)
            start_url(args.scan, mode, keylist, output_name)

    except SystemExit:
        # Catch SystemExit to handle help explicitly
        return None

    return
