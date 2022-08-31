import os
import importlib
from flask import Flask, Blueprint


class NoEntryPointException(AttributeError):
    pass


def dynamic_blueprint_loader(application: Flask):
    """
    Dynamically loads blueprints from the ./modules/ directory
    :param application: A Flask app to attach blueprints to
    :return: A dict detailing the result of the module loading
    :raises TypeError: When the module's setup function does not return a flask.Blueprint object
    :raises NoEntryPointException: The module didn't have a setup function
    """
    result_const = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    try:
        for file in os.listdir("modules"):
            if not file.endswith(".py") or file in ["__init__.py", "__pycache__"]:
                result_const["skipped"].append(file)
                continue
            else:
                module = importlib.import_module(f"modules.{file.strip('.py')}")
                try:
                    blueprint = module.setup()
                    if not isinstance(blueprint, Blueprint):
                        result_const["failed"].append((file, TypeError()))
                        raise TypeError(f"Module {module.__name__}'s setup func should return a Blueprint, returned a {str(type(blueprint))} instead")
                    application.register_blueprint(blueprint)
                    result_const["success"].append(file)
                except AttributeError as e:
                    result_const["failed"].append((file, e))
                    raise NoEntryPointException(f"Module '{module.__name__}' does not have a setup func") from e
    except Exception as e:
        raise


app = Flask(__name__)
dynamic_blueprint_loader(app)
if __name__ == "__main__":
    app.run("0.0.0.0", 8080, True)