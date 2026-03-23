from pathlib import Path

from django.core.management.base import BaseCommand

from apps.investments.services import sync_investment_products


class Command(BaseCommand):
    help = "Sincroniza o catalogo de produtos de investimento a partir de um arquivo JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            dest="file_path",
            help="Caminho opcional para um arquivo JSON com o catalogo de produtos.",
        )

    def handle(self, *args, **options):
        file_path = options.get("file_path")
        summary = sync_investment_products(
            data_file=Path(file_path).resolve() if file_path else None,
        )
        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Catalogo sincronizado com sucesso. "
                    f"Criados: {summary['created']}. "
                    f"Atualizados: {summary['updated']}."
                )
            )
        )
