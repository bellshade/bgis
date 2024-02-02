import sys
import click


@click.command()
def main(args=None):
    click.echo("ganti pesan ini dengan menambahkan kode kamu ke bgis.console.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())
