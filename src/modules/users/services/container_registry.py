from logger_tracker import logg_info, logg_error
from src.config import CAPABILITIES

def deploy_stack(cf_client, stack_name, template_file_path):
    """Despliega un stack de CloudFormation, creando o actualizando según sea necesario."""
    logg_info(f"🚀 Desplegando {stack_name}...")
    
    try:
        with open(template_file_path, "r") as template_file:
            template_body = template_file.read()
        stack_exists = False
        try:
            cf_client.describe_stacks(StackName=stack_name)
            stack_exists = True
        except cf_client.exceptions.ClientError as e:
            if "does not exist" not in str(e):
                raise
        if stack_exists:
            logg_info(f"🔄 Intentando actualizar stack existente: {stack_name}...")
            try:
                cf_client.update_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Capabilities=CAPABILITIES
                )
                waiter = cf_client.get_waiter('stack_update_complete')
            except cf_client.exceptions.ClientError as e:
                if "No updates are to be performed" in str(e):
                    logg_info(f"✅ Stack {stack_name} ya está actualizado. No se requiere acción.")
                    return
                else:
                    raise
        else:
            logg_info(f"✨ Creando nuevo stack: {stack_name}...")
            cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=CAPABILITIES
            )
            waiter = cf_client.get_waiter('stack_create_complete')
        logg_info("⏳ Esperando a que el despliegue finalice...")
        waiter.wait(StackName=stack_name)
        logg_info(f"✅ {stack_name} desplegado con éxito.")
    except Exception as e:
        logg_error(f"❌ Error al desplegar {stack_name}: {e}")

