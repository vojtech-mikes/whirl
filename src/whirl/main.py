import cli

cli = cli.CliParser()

args = cli.parser.parse_args()

args.func(args)
