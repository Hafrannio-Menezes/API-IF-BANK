from pathlib import Path

from django.core.management.base import BaseCommand

from apps.users.services.presentation_data_service import load_presentation_data


class Command(BaseCommand):
    help = "Carrega dados de apresentacao no banco para demonstrar o projeto."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            dest="file_path",
            help="Caminho opcional para um arquivo JSON com os dados de apresentacao.",
        )

    def handle(self, *args, **options):
        file_path = options.get("file_path")
        summary = load_presentation_data(
            data_file=Path(file_path).resolve() if file_path else None,
            reset_existing=True,
        )
        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Dados de apresentacao carregados com sucesso. "
                    f"Usuarios: {summary['users']}. "
                    f"Contas: {summary['accounts']}. "
                    f"Metas: {summary['goals']}. "
                    f"Transferencias: {summary['transfers']}. "
                    f"Investimentos: {summary['investments']}."
                )
            )
        )
