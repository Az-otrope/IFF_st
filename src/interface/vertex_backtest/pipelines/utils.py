from kfp import components


def build_task_from_component(task_yml_spec: str, task_kwargs: dict):
    """
    The build_task_from_component function is a helper function that takes in the path to a task
    component YAML file and some keyword arguments, and returns an instantiated Task object.


    :param task_yml_spec: str: Specify the path to the task yaml file
    :param task_kwargs: dict: Pass in the parameters that are used to create a task
    :return: A task object
    """
    task_factory = components.load_component_from_file(filename=task_yml_spec)
    task = task_factory(**task_kwargs)

    return task
