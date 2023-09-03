import maya.cmds as cmds

def remove_existing_expression(attribute, lights):
    # Parcourir les lumières sélectionnées et supprimer l'expression existante sur l'attribut spécifié
    to_delete = []
    for light in lights:
        existing_expressions = cmds.listConnections("{}.{}".format(light, attribute), type="expression") or []
        to_delete.extend(existing_expressions)

    if to_delete:
        cmds.delete(to_delete)

def apply_expression_to_lights(attribute, expression, lights):
    if not lights:
        cmds.warning("Aucune lumière sélectionnée.")
        return

    remove_existing_expression(attribute, lights)  # Supprimer les expressions existantes sur l'attribut

    # Parcourir les lumières sélectionnées et appliquer l'expression à l'attribut spécifié
    for light in lights:
        light_name = light.split("|")[-1]  # Obtenir le nom de la lumière sans le chemin
        light_number = ''.join([c for c in light_name if c.isdigit()])  # Extraire les chiffres du nom de la lumière
        full_expression = "{}.{} = {}".format(light, attribute, expression)
        cmds.expression(
            name="{}_{}_expression".format(light, attribute),
            string=full_expression,
            object=light,
            attribute=attribute,
            unitConversion="none",
            alwaysEvaluate=True
        )

def show_persistent_dialog():
    if cmds.window("lightExpressionDialog", exists=True):
        cmds.deleteUI("lightExpressionDialog")

    cmds.window("lightExpressionDialog", title="Appliquer une Expression aux Lumières")
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.separator(height=10)
    cmds.text(label="Attribut à modifier:")
    attribute_field = cmds.textField()

    cmds.separator(height=10)
    cmds.text(label="Expression à appliquer:")
    expression_field = cmds.textField()

    cmds.separator(height=10)
    cmds.checkBox("allLightsCheckbox", label="Appliquer sur toutes les lumières")

    cmds.separator(height=10)
    cmds.button(label="Appliquer", command=lambda *args: on_apply_button_pressed(attribute_field, expression_field))
    
    cmds.showWindow("lightExpressionDialog")

def on_apply_button_pressed(attribute_field, expression_field):
    attribute = cmds.textField(attribute_field, query=True, text=True)
    expression = cmds.textField(expression_field, query=True, text=True)
    all_lights = cmds.checkBox("allLightsCheckbox", query=True, value=True)

    lights_types = ["light"]
    if all_lights:
        lights = cmds.ls(type=lights_types)
    else:
        selected =mc.ls(sl=True)
        lights = mc.ls(
            selected + (mc.listRelatives(selected, allDescendents=True, path=True) or []),
            type=lights_types
        )


    apply_expression_to_lights(attribute, expression, lights)

show_persistent_dialog()

