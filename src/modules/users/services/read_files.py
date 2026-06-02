import os
import sys
from src.modules.users.services.deployment_service import DeploymentService
from src.modules.clients.repositories.aws_repository import AwsRepository
from src.modules.clients.models.http.deploy_stack_request import DeployRequest
from src.config import ENVIRONMENT

#
# Esta funcion se usa para seleccionar un folder mediante cli
#
def select_folder_cli(directory):
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    while True:
        print("\n📂 Selecciona el stack a desplegar:")
        for i, folder in enumerate(folders):
            print(f"  [{i+1}] {folder}")
        print("  [0] ❌ Cancelar")
        try:
            choice = int(input("Tu selección: "))
            if choice == 0:
                print("🚪 Saliendo del programa...")
                sys.exit(0)
            elif 1 <= choice <= len(folders):
                return folders[choice-1]
            else:
                print("❌ Selección inválida, intenta de nuevo.")
        except ValueError:
            print("❌ Entrada inválida, por favor ingresa un número.")

def deploy_templates_cli(template_dir, stack_folder):
    stack_path = os.path.join(template_dir, stack_folder)
    templates = [f for f in os.listdir(stack_path) if f.endswith(".yml")]

    deployment_service = DeploymentService(AwsRepository())

    if not templates:
        print(f"❌ No hay archivos YAML en '{stack_folder}'.")
        sys.exit(1)
        
    while True:
        print(f"\n📜 Archivos YAML disponibles en '{stack_folder}':")
        print("  [1] Todos")
        for i, template in enumerate(templates):
            print(f"  [{i+2}] {template}")
        print("  [0] ❌ Cancelar")
        try:
            choice = int(input("Tu selección: "))
            if choice == 0:
                print("🚪 Cancelando despliegue...")
                sys.exit(0)
            elif choice == 1:
                for file_name in templates:
                    stack_name = os.path.splitext(file_name)[0]
                    deploy_request = DeployRequest(
                        stack_name=stack_name,
                        template_file=file_name,
                        environment=ENVIRONMENT,
                        base_path=stack_folder,
                        deploy_version="1.0.1"
                    )
                    deployment_service.deploy_local_stack(deploy_request)
                return
            elif 2 <= choice <= len(templates) + 1:
                file_name = templates[choice-2]
                stack_name = os.path.splitext(file_name)[0]
                deploy_request = DeployRequest(
                    stack_name=stack_name,
                    template_file=file_name,
                    environment=ENVIRONMENT,
                    base_path=stack_folder,
                    deploy_version="1.0.1"
                )
                deployment_service.deploy_local_stack(deploy_request)
                return
            else:
                print("❌ Selección inválida, intenta de nuevo.")
        except ValueError as e:
            print(f"❌ Entrada inválida, por favor ingresa un número. Detalles: {e}")
